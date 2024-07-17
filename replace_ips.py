import re
import base64
import json

def read_unique_ips(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def read_original_proxy(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def replace_vless_address(vless_string, new_address):
    pattern = r'@([^:]+):'
    return re.sub(pattern, f'@{new_address}:', vless_string)

def replace_vmess_address(vmess_string, new_address):
    try:
        decoded = base64.b64decode(vmess_string[8:]).decode('utf-8')
        vmess_config = json.loads(decoded)
        vmess_config['add'] = new_address
        encoded = base64.b64encode(json.dumps(vmess_config).encode('utf-8')).decode('utf-8')
        return f"vmess://{encoded}"
    except Exception as e:
        print(f"Error processing VMess string: {e}")
        return vmess_string

def generate_new_proxies(original_proxy, unique_ips):
    new_proxies = []
    for ip in unique_ips:
        if original_proxy.startswith('vless://'):
            new_proxy = replace_vless_address(original_proxy, ip)
        elif original_proxy.startswith('vmess://'):
            new_proxy = replace_vmess_address(original_proxy, ip)
        else:
            print(f"Unsupported proxy type: {original_proxy[:10]}...")
            continue
        new_proxies.append(new_proxy)
    return new_proxies

def write_new_proxies(file_path, new_proxies):
    with open(file_path, 'w') as file:
        for proxy in new_proxies:
            file.write(f"{proxy}\n")

# File paths
unique_ips_file = 'unique_ips.txt'
original_proxy_file = 'original_proxies.txt'
output_file = 'new_proxies.txt'

# Read input files
unique_ips = read_unique_ips(unique_ips_file)
original_proxy = read_original_proxy(original_proxy_file)

# Generate new proxies
new_proxies = generate_new_proxies(original_proxy, unique_ips)

# Write new proxies to file
write_new_proxies(output_file, new_proxies)

print(f"New proxies have been generated and saved to {output_file}")
