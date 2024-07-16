import re
import base64

def read_unique_ips(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def replace_ip_in_proxy(proxy_string, new_ip):
    pattern = r'@[^:]+:'
    return re.sub(pattern, f'@{new_ip}:', proxy_string)

def main():
    unique_ips = read_unique_ips('unique_ips.txt')

    with open('original_proxy.txt', 'r') as file:
        original_proxy = file.read().strip()

    new_proxies = [replace_ip_in_proxy(original_proxy, ip) for ip in unique_ips]

    # Write the new proxy strings to a file (unencrypted)
    with open('new_proxies.txt', 'w') as file:
        for proxy in new_proxies:
            file.write(f"{proxy}\n")

    # Combine all proxies into a single line and encode to base64
    combined_proxies = ''.join(new_proxies)
    encoded_proxies = base64.b64encode(combined_proxies.encode()).decode()

    # Write the base64 encoded proxies to a file
    with open('new_proxies64.txt', 'w') as file:
        file.write(encoded_proxies)

    print("New proxy strings have been saved to new_proxies.txt")
    print("Base64 encoded combined proxies have been saved to new_proxies64.txt")

if __name__ == "__main__":
    main()
