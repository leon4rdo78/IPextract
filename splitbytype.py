import os

def separate_configs(input_file, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize dictionaries to store configs by type
    config_types = {
        'vless': [],
        'vmess': [],
        'ss': [],
        'hysteria2': [],
        'trojan': []
    }

    # Read the input file and separate configs
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('vless://'):
                config_types['vless'].append(line)
            elif line.startswith('vmess://'):
                config_types['vmess'].append(line)
            elif line.startswith('ss://'):
                config_types['ss'].append(line)
            elif line.startswith(('hysteria2://', 'hy2://')):
                config_types['hysteria2'].append(line)
            elif line.startswith('trojan://'):
                config_types['trojan'].append(line)

    # Write configs to separate files
    for config_type, configs in config_types.items():
        output_file = os.path.join(output_folder, f"{config_type}.txt")
        with open(output_file, 'w') as f:
            for config in configs:
                f.write(f"{config}\n")

    print(f"Config separation complete. Files saved in {output_folder}")

if __name__ == "__main__":
    input_file = "nodup_proxies.txt"
    output_folder = "splitbytype"
    separate_configs(input_file, output_folder)
