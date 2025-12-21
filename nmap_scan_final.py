import subprocess
import re

target = input("Enter website to scan: ")

# Ping function to check if host is alive
def is_host_alive(host):
    result = subprocess.run(
        ["ping", "-n", "1", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

# Nmap scan function
def run_nmap(host):
    print("[+] Running Nmap scan...\n")
    cmd = [
        "nmap",
        "-A",
        host
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        shell=True
    )
    output = result.stdout
    
    extract_ip(output)
    extract_ports(output)
    extract_traceroute(output)

# Extract IP Address
def extract_ip(output):
    print("\n[+] Target IP Address:")

    match = re.search(r"\((\d{1,3}(?:\.\d{1,3}){3})\)", output)
    if not match:
        match = re.search(
            r"Nmap scan report for (\d{1,3}(?:\.\d{1,3}){3})",
            output
        )
    print("IP Address:", match.group(1) if match else "Not found")

# Extract Open Ports
def extract_ports(output):
    print("\n[+] Extracted Open Ports:\n")
    pattern = r"(\d+)\/(\w+)\s+open\s+(\S+)\s*(.*)"
    matches = re.findall(pattern, output)
    if not matches:
        print("No open ports found.")
        return
    for port, proto, service, version in matches:
        print(f"Port     : {port}")
        print(f"Protocol : {proto}")
        print(f"Service  : {service}")
        print(f"Version  : {version.strip() if version else 'N/A'}")
        print("-" * 30)

# Extract Traceroute
def extract_traceroute(output):
    print("\n[+] Full Traceroute Information:\n")

    match = re.search(
        r"TRACEROUTE[\s\S]+?(?=\n\n|\Z)",
        output
    )
    if match:
        print(match.group(0))
    else:
        print("Traceroute information not found.")

# if host is alive it runs Nmap scan
if is_host_alive(target):
    print(f"[+] {target} is alive. Starting scan.\n")
    run_nmap(target)
else:
    print(f"[-] {target} is not reachable. Scan skipped.")