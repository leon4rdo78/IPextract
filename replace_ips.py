import re

def read_unique_ips(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def replace_ip_in_proxy(proxy_string, new_ip):
    # Regular expression to match the IP and port in the VLESS string
    pattern = r'@[^:]+:'
    # Replace the matched part with the new IP, preserving the '@' and ':'
    return re.sub(pattern, f'@{new_ip}:', proxy_string)

def main():
    # Read the unique IPs
    unique_ips = read_unique_ips('unique_ips.txt')

    # Read the original proxy string
    with open('original_proxies.txt', 'r') as file:
        original_proxy = file.read().strip()

    # Create new proxy strings with each unique IP
    new_proxies = [replace_ip_in_proxy(original_proxy, ip) for ip in unique_ips]

    # Write the new proxy strings to a file
    with open('new_proxies.txt', 'w') as file:
        for proxy in new_proxies:
            file.write(f"{proxy}\n")

    print(f"New proxy strings have been saved to new_proxies.txt")

if __name__ == "__main__":
    main()
