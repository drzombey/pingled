import random
import time
import socket

icmp_port = 1
icmp_socket = None
udp_client_socket = None
wled_ip = "4.3.2.1"
wled_udp_port = 21324
# Mode: 2 = DRGB
# Timeout: 2 = 2 seconds
config_bytes = [2, 2]
incoming_ping_address_list = []
max_leds = 269



def log_ping(ip):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} - Ping detected from {ip}\n")


def start():
    global incoming_ping_address_list
    _, address = icmp_socket.recvfrom(1024)
    log_ping(address[0])
    random.seed()
    entry = {"ip": address[0], "state": [
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)],
        "position": 0,
    }
    incoming_ping_address_list = add_entry_to_list(entry)
    if len(incoming_ping_address_list) > max_leds:
        del incoming_ping_address_list[-1]
    send_packet_to_stripe_via_udp()


# Example udp packet
# [2, 2, 255, 0, 0]
# First led will be red
# and first byte says DRGB will be used Mode 2
# second byte defines the timeout after returning to normal mode 255 for no return
# next 3 bytes defines R G B Values for the LED with the first index
def send_packet_to_stripe_via_udp():
    values = prepare_udp_packet(incoming_ping_address_list)
    udp_client_socket.sendto(values, (wled_ip, wled_udp_port))


def add_entry_to_list(entry):
    for value in incoming_ping_address_list:
        value["position"] += 1

    incoming_ping_address_list.append(entry)
    return sorted(incoming_ping_address_list, key=lambda k: k["position"])


def prepare_udp_packet(entries):
    led_bytes = config_bytes
    for entry in incoming_ping_address_list:
        led_bytes = led_bytes + entry["state"]

    return bytearray(led_bytes)


if __name__ == "__main__":
    udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.bind(('', icmp_port))
    while True:
        start()
