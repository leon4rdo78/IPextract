import base64
import json
import re

def extract_vless_address(proxy):
    match = re.search(r'@([^:]+)', proxy)
    return match.group(1) if match else None

def extract_vmess_address(proxy):
    encoded_part = proxy.split('://')[1]
    decoded_json = json.loads(base64.b64decode(encoded_part).decode('utf-8'))
    return decoded_json.get('add')

def extract_shadowsocks_address(proxy):
    match = re.search(r'@([^:]+)', proxy)
    return match.group(1) if match else None

def process_proxies(input_file, output_file):
    unique_addresses = set()

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('vless://'):
                address = extract_vless_address(line)
            elif line.startswith('vmess://'):
                address = extract_vmess_address(line)
            elif line.startswith('ss://'):
                address = extract_shadowsocks_address(line)
            else:
                continue  # Skip other types of proxies

            if address:
                unique_addresses.add(address)

    with open(output_file, 'w') as f:
        for address in sorted(unique_addresses):
            f.write(f"{address}\n")

    print(f"Extracted {len(unique_addresses)} unique addresses to {output_file}")

# Run the script
process_proxies('proxies.txt', 'unique_ips.txt')
