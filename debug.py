import socket
import json
import time

# IP and port of the Pico W's access point
PICO_IP = "192.168.42.1"  # Default IP for ESP32/ESP8266 SoftAP mode
UDP_PORT = 4210

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Example JSON message
data = {
    "VX": 1.0,
    "VY": 0.5,
    "VYaw": -0.2
}

# Serialize JSON to string
message = json.dumps(data)

# Send the message
sock.sendto(message.encode(), (PICO_IP, UDP_PORT))
print(f"Sent to {PICO_IP}:{UDP_PORT} -> {message}")

# Optionally keep sending for testing
# time.sleep(1)
# sock.close()
