#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include "Freenove_4WD_Car_For_Pico_W.h"

const char* ssid = "PicoCar_UDP";
const char* password = "12345678";
WiFiUDP Udp;
const int udpPort = 4210;

const int packetSize = 256;
char packetBuffer[packetSize]; // Now a char array for JSON strings

// Declare the JsonDocument globally with a specific capacity
StaticJsonDocument<256> doc;

const int ledPin = LED_BUILTIN;  // For Pico W, use 25 if LED_BUILTIN is undefined


void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.begin(115200);
  Motor_Setup();


  WiFi.softAP(ssid, password);

  
  while (!Serial) {
    delay(10);  // Wait for serial port to connect
  }
  
  Serial.println(WiFi.softAPIP());

  Udp.begin(udpPort);
  Serial.printf("Listening for UDP on port %d\n", udpPort);
}

void loop() {
  int len = Udp.parsePacket();
  // Serial.printf("PING");
  // digitalWrite(ledPin, HIGH);
  // delay(1000);
  // digitalWrite(ledPin, LOW);
  if (len > 0) {
    Serial.printf("[UDP] Packet received: %d bytes\n", len);
    Serial.printf("[UDP] From IP: %s, Port: %d\n", Udp.remoteIP().toString().c_str(), Udp.remotePort());

    int bytesRead = Udp.read(packetBuffer, packetSize - 1);
    packetBuffer[bytesRead] = '\0';

    Serial.printf("[UDP] Data: %s\n", packetBuffer);

    processKineticMsg(packetBuffer);
    // delay(100);

  }
  else{
    Motor_M_Move(0, 0, 0, 0);
  }
}

void processKineticMsg(const char* json) {
  DeserializationError error = deserializeJson(doc, json);

  if (!error) {
    float vx = doc["VX"] | 0.0;
    float vy = doc["VY"] | 0.0;
    float vyaw = doc["VYaw"] | 0.0;

    int LY = static_cast<int>(vy);
    int LX = static_cast<int>(vx);
    int RX = static_cast<int>(vyaw);

    int FR = LY - LX + RX;
    int FL = LY + LX - RX;
    int BL = LY - LX - RX;
    int BR = LY + LX + RX;

    Motor_M_Move(FL, BL, BR, FR); // Move motors

    Serial.printf("VX: %.2f, VY: %.2f, VYaw: %.2f\n", vx, vy, vyaw);
  } else {
    Serial.println("Error parsing JSON data.");
  }
}
