import socket
import threading
import time
import os

PORT = 5000
NEIGHBORS = {}
GOSSIP_INTERVAL = 5
BUFFER_SIZE = 1024
APP = os.getenv("APP", "app")


def send_gossip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    print(f"Sending my IP {ip}")

    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        ) as sock:
            print(f"Send broadcast gossip with my ip: {ip}")
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind(("0.0.0.0", 0))
            sock.sendto(
                bytes(f"{hostname}:{ip}", encoding="utf-8"), ("255.255.255.255", PORT)
            )
            sock.close()
    except Exception as e:
        print(f"Error sending broadcast gossip {e}")


def listen_for_gossip(port, buffer_size):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("0.0.0.0", port))
        print(f"Listening for gossip on port {port}")
        while True:
            data, addr = sock.recvfrom(buffer_size)
            decoded_data = data.decode()
            print(f"Received gossip from {addr}: {decoded_data}")
            hostname, ip = decoded_data.split(":")
            NEIGHBORS[hostname] = ip


def gossip_loop():
    while True:
        send_gossip()
        time.sleep(GOSSIP_INTERVAL)
        print(f"Known neighbors: {NEIGHBORS}")
        time.sleep(GOSSIP_INTERVAL)


def start_gossip_protocol():
    # Start listening for incoming gossip in a separate thread
    listener_thread = threading.Thread(
        target=listen_for_gossip, args=(PORT, BUFFER_SIZE)
    )
    listener_thread.daemon = (
        True  # Allows the thread to be killed when the main thread exits
    )
    listener_thread.start()

    gossip_loop()


if __name__ == "__main__":
    start_gossip_protocol()
