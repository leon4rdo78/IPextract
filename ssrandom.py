import random
import os

def random_line_selector(input_file, output_dir, output_file, num_lines=500):
    # Read all lines from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Get the total number of lines
    total_lines = len(lines)
    
    # If there are fewer than 500 lines, use all of them
    num_lines = min(num_lines, total_lines)
    
    # Randomly select the specified number of lines
    selected_lines = random.sample(lines, num_lines)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the full path for the output file
    output_path = os.path.join(output_dir, output_file)
    
    # Write the selected lines to the output file
    with open(output_path, 'w') as f:
        f.writelines(selected_lines)

# Use the function with your specific file names and directory
input_file = "ss.txt"
output_dir = "splitbytype"
output_file = "ssrandom.txt"

random_line_selector(input_file, output_dir, output_file)

print(f"Randomly selected 500 lines from {input_file} and wrote them to {os.path.join(output_dir, output_file)}")
