import os
import random
import glob

def separate_configs(input_file, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create subfolder for split files
    split_folder = os.path.join(output_folder, "split")
    os.makedirs(split_folder, exist_ok=True)

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

    # Write configs to separate files and split large files
    for config_type, configs in config_types.items():
        # Randomize the order of configs
        random.shuffle(configs)

        # Write to main file
        output_file = os.path.join(output_folder, f"{config_type}.txt")
        with open(output_file, 'w') as f:
            for config in configs:
                f.write(f"{config}\n")

        # Split large files
        if config_type in ['vless', 'vmess']:
            split_configs(configs, config_type, split_folder)

    # Clean up old split files
    cleanup_old_files(split_folder)

    print(f"Config separation complete. Files saved in {output_folder}")

def split_configs(configs, config_type, split_folder):
    max_lines = 250
    for i in range(0, len(configs), max_lines):
        part_num = i // max_lines + 1
        output_file = os.path.join(split_folder, f"{config_type}-part{part_num}.txt")
        with open(output_file, 'w') as f:
            for config in configs[i:i+max_lines]:
                f.write(f"{config}\n")

def cleanup_old_files(folder):
    # Get list of current files
    current_files = set(os.listdir(folder))

    # Get list of all part files
    all_part_files = set(glob.glob(os.path.join(folder, "*-part*.txt")))

    # Files to be deleted
    files_to_delete = all_part_files - current_files

    # Delete old files
    for file in files_to_delete:
        os.remove(file)

if __name__ == "__main__":
    input_file = "nodup_proxies.txt"
    output_folder = "splitbytype"
    separate_configs(input_file, output_folder)
