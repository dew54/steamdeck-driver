import socket
from pymavlink import mavutil
import time

# ---------------------------
# SETTINGS
# ---------------------------
PICO_IP = "192.168.1.50"  # Pico's IP address
UDP_PORT = 14550

SYSTEM_ID = 1        # Controller system ID
COMPONENT_ID = 1     # Controller component ID

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create MAVLink instance (no file output)
mav = mavutil.mavlink.MAVLink(None)
mav.srcSystem = SYSTEM_ID
mav.srcComponent = COMPONENT_ID

def send_heartbeat():
    msg = mav.heartbeat_encode(
        mavutil.mavlink.MAV_TYPE_GCS,  # Pretend we're a ground station
        mavutil.mavlink.MAV_AUTOPILOT_INVALID,
        0, 0, 0
    )
    packet = msg.pack(mav)
    sock.sendto(packet, (PICO_IP, UDP_PORT))

def send_manual_control(x, y):
    # x, y are joystick positions (-1000..1000)
    msg = mav.manual_control_encode(
        target=2,     # Target system ID for Pico
        x=x,
        y=y,
        z=0,          # throttle
        r=0,          # rotation
        buttons=0
    )
    packet = msg.pack(mav)
    sock.sendto(packet, (PICO_IP, UDP_PORT))

if __name__ == "__main__":
    while True:
        send_heartbeat()
        send_manual_control(500, -500)  # Example: right stick forward-left
        time.sleep(1)
