import subprocess
import time
import signal
import sys

from steamdeck import SteamDeck
from mechanumPlatform import MechanumPlatform
from message import Message
from udp_handler import PicoW_UDP_Client


WIFI_SSID = "steamDriver"
WIFI_PASSWORD = "12345678"

previous_ssid = None


def get_current_ssid():
    """Return the currently connected Wi-Fi SSID or None."""
    result = subprocess.run(
        ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
        capture_output=True, text=True
    )
    for line in result.stdout.strip().split("\n"):
        active, ssid = line.split(":", 1)
        if active == "yes":
            return ssid
    return None


def connect_to_wifi(ssid, password):
    print(f"[Wi-Fi] Connecting to '{ssid}'...")
    status = subprocess.run(
        ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
        capture_output=True, text=True
    )
    if f"yes:{ssid}" in status.stdout:
        print(f"[Wi-Fi] Already connected to '{ssid}'.")
        return True

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


def restore_wifi(ssid):
    if ssid is None:
        print("[Wi-Fi] No previous Wi-Fi SSID to restore.")
        return
    print(f"[Wi-Fi] Restoring previous Wi-Fi connection to '{ssid}'...")
    result = subprocess.run(
        ["nmcli", "dev", "wifi", "connect", ssid],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"[Wi-Fi] Restored connection to '{ssid}'.")
    else:
        print(f"[Wi-Fi] Failed to restore Wi-Fi: {result.stderr.strip()}")


# Catch signals to restore Wi-Fi on exit
def signal_handler(sig, frame):
    print("\n[Signal] Caught exit signal, restoring Wi-Fi...")
    restore_wifi(previous_ssid)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # kill command


# Save current Wi-Fi before connecting
previous_ssid = get_current_ssid()
print(f"[Wi-Fi] Previous Wi-Fi SSID: {previous_ssid}")

if not connect_to_wifi(WIFI_SSID, WIFI_PASSWORD):
    print("[Wi-Fi] Could not connect — exiting.")
    exit(1)


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
    print("[Exit] Restoring previous Wi-Fi before closing...")
    restore_wifi(previous_ssid)
    deck.close()
