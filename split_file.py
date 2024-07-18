import os
import math
import random
import shutil
from datetime import datetime

def archive_and_clear_split_dir(archive_dir='archive', split_dir='split'):
    # Create archive directory if it doesn't exist
    os.makedirs(archive_dir, exist_ok=True)
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a new directory in archive with the timestamp
    archive_path = os.path.join(archive_dir, timestamp)
    
    # If split directory exists, move it entirely to the archive
    if os.path.exists(split_dir):
        shutil.move(split_dir, archive_path)
        print(f"Archived existing split directory to {archive_path}")
    else:
        print("No existing split directory to archive")
    
    # Create a new empty split directory
    os.makedirs(split_dir, exist_ok=True)
    print("Created new empty split directory")

def split_file(input_file, output_dir='split', max_lines=500):
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    random.shuffle(lines)

    total_lines = len(lines)
    num_files = math.ceil(total_lines / max_lines)

    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_files):
        start = i * max_lines
        end = min((i + 1) * max_lines, total_lines)

        output_file = os.path.join(output_dir, f'proxies_part_{i+1}.txt')
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.writelines(lines[start:end])
            
            print(f"Created {output_file} with {end-start} lines")
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    archive_and_clear_split_dir()
    split_file('new_proxies.txt')
