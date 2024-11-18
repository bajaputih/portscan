import socket
from concurrent.futures import ThreadPoolExecutor

# Daftar port umum dengan nama layanan
COMMON_PORTS = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "ssl/https",
    465: "ssl/smtp",
    587: "smtp",
    993: "ssl/imap",
    995: "ssl/pop3",
    3306: "mysql",
    3389: "ms-wbt-server",
    8080: "http-proxy",
}

def scan_port(target, port):
    try:
        # Coba koneksi ke port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((target, port)) == 0:
                try:
                    # Mendeteksi layanan (jika memungkinkan)
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = COMMON_PORTS.get(port, "unknown")
                return f"{port}/tcp   open   {service}"
    except Exception as e:
        pass
    return None

def main():
    target = input("Apa nama web untuk membuka port? ")
    try:
        target_ip = socket.gethostbyname(target)
        print(f"\nScanning {target} ({target_ip})...\n")
        print("PORT     STATE SERVICE")
    except socket.gaierror:
        print("Nama web tidak valid atau tidak dapat ditemukan.")
        return

    # Gunakan ThreadPoolExecutor untuk mempercepat pemindaian
    open_ports = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scan_port, target_ip, port) for port in COMMON_PORTS.keys()]
        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)

    # Cetak hasil
    if open_ports:
        for entry in open_ports:
            print(entry)
    else:
        print("Tidak ada port yang terbuka ditemukan.")

if __name__ == "__main__":
    main()
