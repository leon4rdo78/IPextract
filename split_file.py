import os
import math

def split_file(input_file, max_lines=500):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    num_files = math.ceil(total_lines / max_lines)

    for i in range(num_files):
        start = i * max_lines
        end = min((i + 1) * max_lines, total_lines)
        
        output_file = f'proxies_part_{i+1}.txt'
        with open(output_file, 'w') as file:
            file.writelines(lines[start:end])
        
        print(f"Created {output_file} with {end-start} lines")

if __name__ == "__main__":
    split_file('proxies.txt')
