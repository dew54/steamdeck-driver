import socket

class PicoW_UDP_Client:
    def __init__(self, ip='192.168.4.1', port=4210):
        self.server_ip = ip
        self.server_port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)  # Optional: Set timeout for response

    def send_message(self, message):
        try:
            self.sock.sendto(message.encode(), (self.server_ip, self.server_port))
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def close(self):
        self.sock.close()
        print("Socket closed.")

# Example usage
if __name__ == "__main__":
    client = PicoW_UDP_Client()
    client.send_message("Hello from Python!")
    client.close()
