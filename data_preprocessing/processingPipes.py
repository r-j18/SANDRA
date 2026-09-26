import os
import cv2 
import numpy as np
import scipy.ndimage as sc

# Input Directories grouped in a list 
inpt_dirs = [
    "/run/media/artifex/FedoraStorage/rawdataset/Pipes.v1i.yolov8/train/images",
    "/run/media/artifex/FedoraStorage/rawdataset/Pipes.v1i.yolov8/train/labels"
]

# Output Directories
img_out = "/home/artifex/SANDRA/dataset/images"
label_out = "/home/artifex/SANDRA/dataset/labels"

# 1. Loop through each folder path
for current_dir in inpt_dirs:
    # Get the list of filenames in that specific folder
    content = os.listdir(current_dir)
    
    # 2. Loop through each filename in the list
    for filename in content:
        if filename.endswith(".jpg"):
            # Join the folder path and filename to create the full absolute path
            full_img_path = os.path.join(current_dir, filename)
            
            # Read the image, fix the typo, and assign to a variable
            img = cv2.imread(full_img_path, cv2.IMREAD_GRAYSCALE)
            
            img = np.float32(img)

            localMean = sc.uniform_filter(img, size = 5)

            localVar  = sc.uniform_filter(img**2, size=5) - (localMean**2)

            globalVar = np.var(img)

            weights = localVar / (localVar + globalVar + 1e-12)

            lee_float = localMean + weights * (img - localMean)

            lee_8bit = np.clip(lee_float, 0, 255).astype(np.uint8)

            clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize = (8,8))

            final_img = clahe.apply(lee_8bit)

            out_img_path = os.path.join(img_out, filename)
            cv2.imwrite(out_img_path, final_img)

        elif filename.endswith(".txt"):
            
            inpt_txt_path = os.path.join(current_dir, filename)
            out_txt_path = os.path.join(label_out, filename)
            with open(inpt_txt_path, "r") as infile:
                lines = infile.readlines()

            modified_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue # Skips empty lines in your empty files
                    
                if parts[0] == "0":
                    parts[0] = "5"      
                elif parts[0] == "1":
                    parts[0] = "3"            
            
                    
                # Rebuild the line
                modified_lines.append(" ".join(parts) + "\n")
            
            # Save the new labels
            with open(out_txt_path, "w") as outfile:
                outfile.writelines(modified_lines)

            