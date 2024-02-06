import random

def sample_lines_from_file(file_path, num_samples=30):
    """Randomly sample num_samples lines from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Ensure we don't try to sample more lines than are in the file
    num_samples = min(num_samples, len(lines))
    
    sampled_lines = random.sample(lines, num_samples)
    
    return sampled_lines

# Usage
file_path = 't.txt'  # Replace with your file path
sampled_lines = sample_lines_from_file(file_path)

test = ""

# Optionally, print the sampled lines
for line in sampled_lines:
    test += line.split(".")[1] + '\n'
    
with open("researchtest.txt", 'w')as w :
    w.write(test)