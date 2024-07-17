import re
import ipaddress
import base64
import json

def extract_unique_ips(file_path):
    unique_ips = set()
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('vless://'):
                ip = extract_vless_ip(line)
            elif line.startswith('vmess://'):
                ip = extract_vmess_ip(line)
            else:
                continue
            
            if ip:
                try:
                    ipaddress.ip_address(ip)
                    unique_ips.add(ip)
                except ValueError:
                    print(f"Invalid IP address found: {ip}")

    return sorted(unique_ips)

def extract_vless_ip(vless_string):
    ip_pattern = r'@(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):'
    match = re.search(ip_pattern, vless_string)
    return match.group(1) if match else None

def extract_vmess_ip(vmess_string):
    try:
        # Remove 'vmess://' prefix and decode base64
        decoded = base64.b64decode(vmess_string[8:]).decode('utf-8')
        # Parse JSON
        vmess_config = json.loads(decoded)
        return vmess_config.get('add')
    except Exception as e:
        print(f"Error decoding VMess string: {e}")
        return None

# Path to your input file
input_file = 'proxies.txt'

# Extract unique IPs
unique_ip_list = extract_unique_ips(input_file)

# Print the results
print("Unique IP addresses:")
for ip in unique_ip_list:
    print(ip)

# Optionally, write the results to a file
output_file = 'unique_ips.txt'
with open(output_file, 'w') as file:
    for ip in unique_ip_list:
        file.write(f"{ip}\n")

print(f"\nUnique IP addresses have been saved to {output_file}")
