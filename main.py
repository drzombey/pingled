import time
import socket

icmp_port = 1
icmp_socket = None


def log_ping_detection():
    global icmp_socket
    try:
        icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        icmp_socket.bind(('', icmp_port))

        packet, address = icmp_socket.recvfrom(1024)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{timestamp} - Ping detected from {address[0]}\n")

    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        if icmp_socket is not None:
            icmp_socket.close()


while True:
    log_ping_detection()
    time.sleep(5)
