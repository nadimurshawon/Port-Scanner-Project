
import socket
import threading
from datetime import datetime

# Dictionary for common ports and their names
common_ports = {
    20: "FTP (Data)",
    21: "FTP (Control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Proxy"
}

# Get target info from user
target = input("Enter Target IP or Hostname: ")
start_port = int(input("Enter Starting Port: "))
end_port = int(input("Enter Ending Port: "))

# Output file
output_file = "scan_results.txt"

# Lock for thread-safe file writing
write_lock = threading.Lock()

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            service = common_ports.get(port, "Unknown")
            try:
                sock.send(b"NRS.\r\n")
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "No banner"
            output = f"[+] Port {port} OPEN  | Service: {service} | Banner: {banner}"
            print(output)
            with write_lock:
                with open(output_file, "a") as f:
                    f.write(output + "\n")
        sock.close()
    except:
        pass

def run_scanner():
    print(f"\nStarting scan on {target} from port {start_port} to {end_port}...\n")
    print("Scan started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 50)

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nScan complete.")
    print(f"Results saved in '{output_file}'")

if __name__ == "__main__":
    run_scanner()
