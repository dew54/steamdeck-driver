#include <WiFi.h>
#include <WiFiUdp.h>
#include "mavlink/minimal/mavlink.h"
#include "Freenove_4WD_Car_For_Pico_W.h"

const char* ssid     = "YourWiFiSSID";
const char* password = "YourWiFiPassword";

WiFiUDP udp;
const unsigned int localUdpPort = 14550;  // Default MAVLink UDP port

uint8_t incomingPacket[512];
mavlink_message_t msg;
mavlink_status_t status;

// Movement command map
enum MovementCommand {
  STOP = 0,
  FORWARD = 1,
  BACKWARD = 2,
  LEFT = 3,
  RIGHT = 4
};

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Motor init
  Motor_Setup();
  Serial.println("Motors ready.");

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  udp.begin(localUdpPort);
  Serial.printf("Listening on UDP port %d\n", localUdpPort);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 512);
    if (len > 0) {
      for (int i = 0; i < len; i++) {
        if (mavlink_parse_char(MAVLINK_COMM_0, incomingPacket[i], &msg, &status)) {
          handleMAVLinkMessage(msg);
        }
      }
    }
  }
}

void handleMAVLinkMessage(mavlink_message_t& msg) {
  if (msg.msgid == MAVLINK_MSG_ID_COMMAND_LONG) {
    mavlink_command_long_t cmd;
    mavlink_msg_command_long_decode(&msg, &cmd);

    if (cmd.command == 3000) {  // Custom MAV_CMD
      int action = static_cast<int>(cmd.param1);
      Serial.print("Received move command: ");
      Serial.println(action);

      switch (action) {
        case FORWARD:
          Motor_Move(60, 60);
          break;
        case BACKWARD:
          Motor_Move(-60, -60);
          break;
        case LEFT:
          Motor_Move(-50, 50);
          break;
        case RIGHT:
          Motor_Move(50, -50);
          break;
        case STOP:
        default:
          Motor_Move(0, 0);
          break;
      }
    }
  }
}
