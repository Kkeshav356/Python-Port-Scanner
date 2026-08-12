import socket

print("=" * 50)
print("TCP Port Scanner v1.0")
print("=" * 50)

target_ip = input("Enter Target IP: ")
start_port = int(input("Enter Start Port: "))
end_port = int(input("Enter End Port: "))

for port in range(start_port, end_port + 1):

    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    scanner.settimeout(1)

    result = scanner.connect_ex((target_ip, port))

    if result == 0:
        print(f"Port {port} is OPEN")

    scanner.close()
