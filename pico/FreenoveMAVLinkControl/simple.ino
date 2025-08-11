#include <WiFi.h>
#include <WiFiUdp.h>
#include "mavlink/minimal/mavlink.h"

const char* ssid     = "YourWiFiSSID";
const char* password = "YourWiFiPassword";

WiFiUDP udp;
const unsigned int localUdpPort = 14550;

uint8_t incomingPacket[512];
mavlink_message_t msg;
mavlink_status_t status;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.println(WiFi.localIP());

  udp.begin(localUdpPort);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, sizeof(incomingPacket));
    for (int i = 0; i < len; i++) {
      if (mavlink_parse_char(MAVLINK_COMM_0, incomingPacket[i], &msg, &status)) {
        handleMavlinkMessage(msg);
      }
    }
  }
}

void handleMavlinkMessage(const mavlink_message_t& msg) {
  switch (msg.msgid) {
    case MAVLINK_MSG_ID_HEARTBEAT:
      Serial.println("Heartbeat received from controller");
      break;
    case MAVLINK_MSG_ID_MANUAL_CONTROL: {
      mavlink_manual_control_t mc;
      mavlink_msg_manual_control_decode(&msg, &mc);
      Serial.printf("Manual control: x=%d, y=%d\n", mc.x, mc.y);
      break;
    }
  }
}
