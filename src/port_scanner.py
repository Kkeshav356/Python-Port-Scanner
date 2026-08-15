import socket
import time
import argparse
import concurrent.futures
import json

def validate_ports(start_port, end_port):
    if not 1 <= start_port <= 65535:
        raise ValueError("Start port must be between 1 and 65535")

    if not 1 <= end_port <= 65535:
        raise ValueError("End port must be between 1 and 65535")

    if start_port > end_port:
        raise ValueError("Start port cannot be greater than end port")
        
def validate_target(target_ip):
    try:
        socket.inet_aton(target_ip)
    except socket.error:
        raise ValueError("Invalid IP address")
        
def grab_banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((ip, port))
            banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner
    except (socket.timeout, ConnectionRefusedError, OSError):
        return ""
        
def scan_port(target_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
            scanner.settimeout(1)

            result = scanner.connect_ex((target_ip, port))

            if result != 0:
                return None

            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "unknown"

            banner = grab_banner(target_ip, port)

            return port, service, banner

    except OSError:
        return None
    
print("=" * 50)
print("TCP Port Scanner v1.0")
print("=" * 50)

parser = argparse.ArgumentParser(description="TCP Port Scanner")
parser.add_argument("--output", help="Save results to a JSON file")
parser.add_argument("target_ip", help="Target IP address")
parser.add_argument("start_port", type=int, help="Starting port")
parser.add_argument("end_port", type=int, help="Ending port")

args = parser.parse_args()

target_ip = args.target_ip
start_port = args.start_port
end_port = args.end_port
try:
    validate_ports(start_port, end_port)
    validate_target(target_ip)
except ValueError as error:
    print(f"[!] Error: {error}")
    exit(1)

open_ports = []
scan_start = time.time()

ports = range(start_port, end_port + 1)

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = executor.map(lambda port: scan_port(target_ip, port), ports)

    for result in results:
        if result:
            port, service, banner = result

            print(f"[+] Port {port} is OPEN | Service: {service}")

            if banner:
                print(f"    Banner: {banner}")

            open_ports.append((port, service, banner))
           
scan_end = time.time()
scan_duration = scan_end - scan_start
scan_results = {
    "target": target_ip,
    "start_port": start_port,
    "end_port": end_port,
    "open_ports": [
        {
            "port": port,
            "service": service,
            "banner": banner
        }
        for port, service, banner in open_ports
    ],
    "total_open_ports": len(open_ports),
    "scan_time": round(scan_duration, 2)
}
if args.output:
    with open(args.output, "w") as file:
        json.dump(scan_results, file, indent=4)

    print(f"\n[+] Results saved to {args.output}")


print("\n" + "=" * 50)
print("SCAN SUMMARY")
print("=" * 50)
print(f"Target: {target_ip}")
print(f"Ports scanned: {start_port}-{end_port}")
print(f"Open ports: {open_ports}")
print(f"Total open ports: {len(open_ports)}")
print(f"Scan time: {scan_duration:.2f} seconds")
print("=" * 50)
