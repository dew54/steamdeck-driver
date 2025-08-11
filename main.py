import time
import pywifi
from pywifi import const

from steamdeck import SteamDeck
from mechanumPlatform import MechanumPlatform
from message import Message
from udp_handler import PicoW_UDP_Client


# ===== CONFIGURE YOUR SSID & PASSWORD HERE =====
WIFI_SSID = "steamDriver"
WIFI_PASSWORD = "12345678"


def connect_to_wifi(ssid, password, timeout=15):
    """Connect to Wi-Fi using pywifi."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # First wireless interface

    print(f"[Wi-Fi] Scanning for '{ssid}'...")
    iface.scan()
    time.sleep(2)  # Allow scan to complete
    scan_results = iface.scan_results()

    found = False
    for network in scan_results:
        if network.ssid == ssid:
            found = True
            break

    if not found:
        print(f"[Wi-Fi] SSID '{ssid}' not found.")
        return False

    # Disconnect if connected to something else
    iface.disconnect()
    time.sleep(1)

    # Create Wi-Fi profile
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    # Remove existing profiles and add new one
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    # Try connecting
    iface.connect(tmp_profile)
    start_time = time.time()

    while time.time() - start_time < timeout:
        if iface.status() == const.IFACE_CONNECTED:
            print(f"[Wi-Fi] Connected to '{ssid}'.")
            return True
        time.sleep(1)

    print(f"[Wi-Fi] Failed to connect to '{ssid}' within {timeout} seconds.")
    return False


# ===== CONNECT BEFORE STARTING UDP LOOP =====
if not connect_to_wifi(WIFI_SSID, WIFI_PASSWORD):
    print("[Wi-Fi] Could not connect — exiting.")
    exit(1)


# ===== ORIGINAL CONTROL SCRIPT =====
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
