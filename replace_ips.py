import base64
import json
import re

def escape_special_chars(s):
    return re.escape(s).replace('\\', r'\\')

def replace_vless_address(proxy, new_address):
    escaped_address = escape_special_chars(new_address)
    return re.sub(r'@[^:]+', f'@{escaped_address}', proxy)

def replace_vmess_address(proxy, new_address):
    try:
        encoded_part = proxy.split('://')[1]
        decoded_json = json.loads(base64.b64decode(encoded_part).decode('utf-8'))
        decoded_json['add'] = new_address
        new_encoded_part = base64.b64encode(json.dumps(decoded_json).encode('utf-8')).decode('utf-8')
        return f"vmess://{new_encoded_part}"
    except Exception as e:
        print(f"Error processing vmess proxy: {str(e)}")
        return proxy  # Return original proxy if there's an error

def process_proxies(unique_ips_file, original_proxies_file, output_file):
    # Read unique IPs
    with open(unique_ips_file, 'r') as f:
        unique_ips = [line.strip() for line in f]

    # Read and process original proxies
    new_proxies = []
    with open(original_proxies_file, 'r') as f:
        original_proxies = [line.strip() for line in f]

    for proxy in original_proxies:
        for new_ip in unique_ips:
            try:
                if proxy.startswith('vless://'):
                    new_proxy = replace_vless_address(proxy, new_ip)
                elif proxy.startswith('vmess://'):
                    new_proxy = replace_vmess_address(proxy, new_ip)
                else:
                    continue  # Skip unknown proxy types
                new_proxies.append(new_proxy)
            except Exception as e:
                print(f"Error processing proxy: {proxy[:30]}... Error: {str(e)}")

    # Write new proxies to output file
    with open(output_file, 'w') as f:
        for proxy in new_proxies:
            f.write(f"{proxy}\n")

    print(f"Created {len(new_proxies)} new proxies in {output_file}")

# Run the script
process_proxies('unique_ips.txt', 'original_proxies.txt', 'new_proxies.txt')
