import os
import cv2 
import numpy as np
import scipy.ndimage as sc

# Input Directories grouped in a list 
inpt_dirs = [
    "/run/media/artifex/FedoraStorage/rawdataset/zenodo1/Marine_PULSE/train/seabed surface",
    "/run/media/artifex/FedoraStorage/rawdataset/zenodo1/Marine_PULSE/test/seabed surface"
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

            # Save the processed image
            out_img_path = os.path.join(img_out, filename)
            cv2.imwrite(out_img_path, final_img)

            # Instantly create and close an empty text file
            txt_filename = filename.replace(".jpg", ".txt")
            out_txt_path = os.path.join(label_out, txt_filename)
            open(out_txt_path, "w").close()

            