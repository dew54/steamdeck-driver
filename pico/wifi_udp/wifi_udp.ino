#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include "Freenove_4WD_Car_For_Pico_W.h"

const char* ssid = "steamDriver";
const char* password = "12345678";
WiFiUDP Udp;
const int udpPort = 4210;

const int packetSize = 256;
char packetBuffer[packetSize];

// Documento JSON con capacità maggiore
StaticJsonDocument<512> doc;

const int ledPin = LED_BUILTIN;  // Su Pico W dovrebbe essere 25
const unsigned long PACKET_TIMEOUT_MS = 500; // Timeout fermata motori (ms)
const int MOTOR_MAX = 255;  // Velocità massima motore

unsigned long lastPacketTime = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.begin(115200);
  Motor_Setup();

  WiFi.softAP(ssid, password);
  while (!Serial) { delay(10); }

  Serial.print("AP IP Address: ");
  Serial.println(WiFi.softAPIP());

  Udp.begin(udpPort);
  Serial.printf("Listening for UDP on port %d\n", udpPort);
}

void loop() {
  int len = Udp.parsePacket();

  if (len > 0) {
    // Se pacchetto più grande del buffer, segnaliamo truncamento
    if (len >= packetSize) {
      Serial.println("[UDP] Warning: packet truncated");
    }

    int bytesRead = Udp.read(packetBuffer, packetSize - 1);
    packetBuffer[bytesRead] = '\0';

    Serial.printf("[UDP] %d bytes from %s:%d\n",
                  bytesRead,
                  Udp.remoteIP().toString().c_str(),
                  Udp.remotePort());

    processKineticMsg(packetBuffer);
    lastPacketTime = millis();

    // LED feedback
    digitalWrite(ledPin, HIGH);
  }

  // Se non arrivano pacchetti entro il timeout, fermiamo i motori
  if (millis() - lastPacketTime > PACKET_TIMEOUT_MS) {
    Motor_M_Move(0, 0, 0, 0);
    digitalWrite(ledPin, LOW);
  }
}

void processKineticMsg(const char* json) {
  DeserializationError error = deserializeJson(doc, json);

  if (error) {
    Serial.printf("[JSON] Parse error: %s\n", error.c_str());
    return;
  }

  // Lettura valori con default
  float vx   = doc["VX"]   | 0.0;
  float vy   = doc["VY"]   | 0.0;
  float vyaw = doc["VYaw"] | 0.0;

  // Scala da [-1.0, 1.0] → [-255, 255]
  int LX = constrain((int)(vx   * MOTOR_MAX), -MOTOR_MAX, MOTOR_MAX);
  int LY = constrain((int)(vy   * MOTOR_MAX), -MOTOR_MAX, MOTOR_MAX);
  int RX = constrain((int)(vyaw * MOTOR_MAX), -MOTOR_MAX, MOTOR_MAX);

  int FR = constrain(LY - LX + RX, -MOTOR_MAX, MOTOR_MAX);
  int FL = constrain(LY + LX - RX, -MOTOR_MAX, MOTOR_MAX);
  int BL = constrain(LY - LX - RX, -MOTOR_MAX, MOTOR_MAX);
  int BR = constrain(LY + LX + RX, -MOTOR_MAX, MOTOR_MAX);

  Motor_M_Move(FL, BL, BR, FR);

  Serial.printf("VX: %.2f, VY: %.2f, VYaw: %.2f | FL:%d BL:%d BR:%d FR:%d\n",
                vx, vy, vyaw, FL, BL, BR, FR);
}
