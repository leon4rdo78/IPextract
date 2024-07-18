import os
import math
import random
import shutil
from datetime import datetime

def archiveorg_and_clear_splitorg_dir(archiveorg_dir='archiveorg', splitorg_dir='splitorg'):
    # Create archiveorg directory if it doesn't exist
    os.makedirs(archiveorg_dir, exist_ok=True)
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a new directory in archiveorg with the timestamp
    archiveorg_path = os.path.join(archiveorg_dir, timestamp)
    os.makedirs(archiveorg_path, exist_ok=True)

    # If splitorg directory exists, archiveorg its contents
    if os.path.exists(splitorg_dir):
        for item in os.listdir(splitorg_dir):
            s = os.path.join(splitorg_dir, item)
            d = os.path.join(archiveorg_path, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
            elif os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
        
        print(f"archiveorgd existing splitorg directory contents to {archiveorg_path}")
    else:
        print("No existing splitorg directory to archiveorg")

    # Clear the splitorg directory by removing and recreating it
    if os.path.exists(splitorg_dir):
        shutil.rmtree(splitorg_dir)
    os.makedirs(splitorg_dir)
    
    print("Cleared and recreated the splitorg directory")

    # Create a .gitkeep file in the empty splitorg directory
    open(os.path.join(splitorg_dir, '.gitkeep'), 'a').close()

def splitorg_file(input_file, output_dir='splitorg', max_lines=500):
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    random.shuffle(lines)

    total_lines = len(lines)
    num_files = math.ceil(total_lines / max_lines)

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
    archiveorg_and_clear_splitorg_dir()
    splitorg_file('proxies.txt')
