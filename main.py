import subprocess
import time

from steamdeck import SteamDeck
from mechanumPlatform import MechanumPlatform
from message import Message
from udp_handler import PicoW_UDP_Client


# ===== CONFIGURE YOUR SSID & PASSWORD =====
WIFI_SSID = "YourNetworkSSID"
WIFI_PASSWORD = "YourPassword123"


def connect_to_wifi(ssid, password):
    """Connect to Wi-Fi using nmcli (NetworkManager)."""
    print(f"[Wi-Fi] Connecting to '{ssid}'...")

    # Check if already connected
    status = subprocess.run(
        ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
        capture_output=True, text=True
    )
    if f"yes:{ssid}" in status.stdout:
        print(f"[Wi-Fi] Already connected to '{ssid}'.")
        return True

    # Try to connect
    result = subprocess.run(
        ["nmcli", "dev", "wifi", "connect", ssid, "password", password],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"[Wi-Fi] Connected to '{ssid}'.")
        return True
    else:
        print(f"[Wi-Fi] Connection failed: {result.stderr.strip()}")
        return False


# ===== CONNECT BEFORE STARTING UDP LOOP =====
if not connect_to_wifi(WIFI_SSID, WIFI_PASSWORD):
    print("[Wi-Fi] Could not connect — exiting.")
    exit(1)


# ===== ORIGINAL UDP CONTROL LOOP =====
deck = SteamDeck()
platform = MechanumPlatform(deck)
msg = Message()

try:
    while True:
        platform.updateKinetic()
        cmd = msg.packKinetic(platform.getKinetic())

        print(cmd)

        udp = PicoW_UDP_Client("192.168.42.1")
        udp.send_message(cmd)

        time.sleep(0.05)

finally:
    deck.close()
