import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    """Scan a single port on a given IP address."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout of 1 second
        result = sock.connect_ex((ip, port))
        if result == 0:
            return port, True
        else:
            return port, False
    except Exception as e:
        return port, False
    finally:
        sock.close()

def scan_ports(ip, port_range):
    """Scan a range of ports on a given IP address."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in port_range]
        for future in futures:
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    target_ip = "80.121.51.65"
    port_range = range(1, 1025)

    print(f"Scanning ports on {target_ip}...")
    open_ports = scan_ports(target_ip, port_range)
    if open_ports:
        print(f"Open ports on {target_ip}: {open_ports}")
    else:
        print(f"No open ports found on {target_ip}.")
