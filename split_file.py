import os
import math
import random  # Import the random module to shuffle lines

def split_file(input_file, output_dir='split', max_lines=500):
    with open(input_file, 'r') as file:  # Open the input file for reading
        lines = file.readlines()  # Read all lines into a list

    random.shuffle(lines)  # Shuffle the lines to randomize their order

    total_lines = len(lines)  # Get the total number of lines
    num_files = math.ceil(total_lines / max_lines)  # Calculate the number of output files needed

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_files):  # Iterate over the number of files to create
        start = i * max_lines  # Calculate the start index for the current file
        end = min((i + 1) * max_lines, total_lines)  # Calculate the end index

        output_file = os.path.join(output_dir, f'proxies_part_{i+1}.txt')  # Define the output file name
        with open(output_file, 'w') as file:  # Open the output file for writing
            file.writelines(lines[start:end])  # Write the subset of lines to the output file
        
        print(f"Created {output_file} with {end-start} lines")  # Print a confirmation message

if __name__ == "__main__":
    split_file('proxies.txt')  # Call the function with 'proxies.txt' as input if the script is executed directly
