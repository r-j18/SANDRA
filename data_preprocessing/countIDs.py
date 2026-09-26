import os
from collections import Counter

label_dir = "/home/artifex/SANDRA/dataset/labels"

# Initialize a counter for the IDs
class_counts = Counter()

# Loop through all text files in your master labels folder
for filename in os.listdir(label_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(label_dir, filename)
        
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                
                # Grab the first number (the class ID)
                class_id = parts[0]
                
                # Tally the valid IDs
                if class_id in ['0', '1', '2', '3', '4', '5']:
                    class_counts[class_id] += 1


# Print the final distribution
print("Master Taxonomy Distribution:")
for class_id in sorted(class_counts.keys()):
    print(f"ID {class_id}: {class_counts[class_id]} instances")
