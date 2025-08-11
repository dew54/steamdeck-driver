import socket
import json
import time
import math

# IP and port of the Pico W's access point
PICO_IP = "192.168.42.1"
UDP_PORT = 4210

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Starting mock input loop. Press Ctrl+C to stop.")

try:
    t = 0.0
    while True:
        # Create mock values (oscillating between -1 and 1)
        vx = math.sin(t)           # forward/backward
        vy = math.cos(t / 2)       # strafe
        vyaw = math.sin(t / 3)     # rotation

        # Scale to match expected range (-1.0..1.0 in Arduino code)
        data = {
            "VX": vx,
            "VY": vy,
            "VYaw": vyaw
        }

        message = json.dumps(data)
        sock.sendto(message.encode(), (PICO_IP, UDP_PORT))

        print(f"Sent: {message}")

        t += 0.1
        time.sleep(0.1)  # send at ~10 Hz

except KeyboardInterrupt:
    print("\nStopped.")
finally:
    sock.close()
