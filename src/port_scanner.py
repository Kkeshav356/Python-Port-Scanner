import socket
import time
import argparse
def grab_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner
    except (socket.timeout, ConnectionRefusedError, OSError):
        return ""
        
print("=" * 50)
print("TCP Port Scanner v1.0")
print("=" * 50)

parser = argparse.ArgumentParser(description="TCP Port Scanner")
parser.add_argument("target_ip", help="Target IP address")
parser.add_argument("start_port", type=int, help="Starting port")
parser.add_argument("end_port", type=int, help="Ending port")

args = parser.parse_args()

target_ip = args.target_ip
start_port = args.start_port
end_port = args.end_port

open_ports = []
scan_start = time.time()

for port in range(start_port, end_port + 1):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)

    result = scanner.connect_ex((target_ip, port))

    if result == 0:
        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "unknown"

        banner = grab_banner(target_ip, port)

        print(f"[+] Port {port} is OPEN | Service: {service}")

        if banner:
            print(f"    Banner: {banner}")

        open_ports.append((port, service, banner))

    else:
        print(f"[-] Port {port} is CLOSED")

    scanner.close()

scan_end = time.time()
scan_duration = scan_end - scan_start

print("\n" + "=" * 50)
print("SCAN SUMMARY")
print("=" * 50)
print(f"Target: {target_ip}")
print(f"Ports scanned: {start_port}-{end_port}")
print(f"Open ports: {open_ports}")
print(f"Total open ports: {len(open_ports)}")
print(f"Scan time: {scan_duration:.2f} seconds")
print("=" * 50)
