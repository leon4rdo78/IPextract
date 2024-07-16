import re
import ipaddress
import base64
import json

MAX_ERRORS = 100

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def extract_unique_ips(file_path):
    unique_ips = set()
    error_count = 0
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            try:
                line = line.strip()
                if line.startswith('vless://'):
                    ip = extract_vless_ip(line)
                elif line.startswith('vmess://'):
                    ip = extract_vmess_ip(line)
                else:
                    continue
                
                if ip and is_valid_ip(ip):
                    unique_ips.add(ip)
            except Exception as e:
                print(f"Error processing line: {e}")
                error_count += 1
                if error_count >= MAX_ERRORS:
                    print(f"Too many errors ({MAX_ERRORS}). Stopping.")
                    break
                continue

    return sorted(unique_ips)

def extract_vless_ip(vless_string):
    ip_pattern = r'@(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):'
    match = re.search(ip_pattern, vless_string)
    return match.group(1) if match else None

def extract_vmess_ip(vmess_string):
    try:
        # Remove 'vmess://' prefix and decode base64
        decoded = base64.b64decode(vmess_string[8:], validate=True).decode('utf-8')
        # Parse JSON
        vmess_config = json.loads(decoded)
        return vmess_config.get('add')
    except (base64.binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Error decoding VMess string: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in VMess decoding: {e}")
        return None

# Path to your input file
input_file = 'proxies.txt'

# Extract unique IPs
unique_ip_list = extract_unique_ips(input_file)

# Print the results
print("Unique IP addresses:")
for ip in unique_ip_list:
    print(ip)

# Write the results to a file
output_file = 'unique_ips.txt'
with open(output_file, 'w') as file:
    for ip in unique_ip_list:
        file.write(f"{ip}\n")

print(f"\nUnique IP addresses have been saved to {output_file}")
