import base64
import json
import re

def extract_vmess_address(proxy):
    try:
        encoded_part = proxy.split('://')[1]
        # Try to decode with padding if necessary
        padding = '=' * (4 - len(encoded_part) % 4)
        decoded_data = base64.b64decode(encoded_part + padding).decode('utf-8', errors='ignore')
        decoded_json = json.loads(decoded_data)
        return decoded_json.get('add')
    except (IndexError, ValueError, json.JSONDecodeError):
        print(f"Failed to extract address from vmess proxy: {proxy[:30]}...")  # Print first 30 chars for debugging
        return None

def process_proxies(input_file, output_file):
    unique_addresses = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            try:
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
            except Exception as e:
                print(f"Error processing line: {line[:30]}... Error: {str(e)}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for address in sorted(unique_addresses):
            f.write(f"{address}\n")

    print(f"Extracted {len(unique_addresses)} unique addresses to {output_file}")

# Run the script
process_proxies('proxies.txt', 'unique_ips.txt')
