import os
import random
import shutil
from collections import defaultdict

# Master paths
base_dir = "/home/artifex/SANDRA/dataset"
img_dir = os.path.join(base_dir, "images")
lbl_dir = os.path.join(base_dir, "labels")

# Create target directories
splits = ['train', 'val', 'test']
for split in splits:
    os.makedirs(os.path.join(base_dir, split, 'images'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, split, 'labels'), exist_ok=True)

# Dictionary to hold images by their primary class (0-5, and 'empty')
class_groups = defaultdict(list)

# Read labels and group images
for txt_name in os.listdir(lbl_dir):
    if not txt_name.endswith('.txt'):
        continue
        
    txt_path = os.path.join(lbl_dir, txt_name)
    img_name = txt_name.replace('.txt', '.jpg')
    
    # Verify the image exists before grouping
    if not os.path.exists(os.path.join(img_dir, img_name)):
        continue

    with open(txt_path, 'r') as f:
        lines = f.readlines()
        
    if len(lines) == 0:
        class_groups['empty'].append(img_name)
    else:
        # Grab the class ID of the first object in the file
        primary_class = lines[0].strip().split()[0]
        class_groups[primary_class].append(img_name)

train_imgs, val_imgs, test_imgs = [], [], []

# Perform the 75/20/5 split on each individual class group
for cls, imgs in class_groups.items():
    random.shuffle(imgs)
    total = len(imgs)
    
    # Calculate exact counts for this specific class
    val_count = int(total * 0.20)
    test_count = int(total * 0.05)
    
    val_end = val_count
    test_end = val_count + test_count
    
    val_imgs.extend(imgs[:val_end])
    test_imgs.extend(imgs[val_end:test_end])
    train_imgs.extend(imgs[test_end:])

def move_files(file_list, split_name):
    for img_name in file_list:
        # Move Image
        src_img = os.path.join(img_dir, img_name)
        dst_img = os.path.join(base_dir, split_name, 'images', img_name)
        if os.path.exists(src_img):
            shutil.move(src_img, dst_img)
        
        # Move Label
        txt_name = img_name.replace('.jpg', '.txt')
        src_lbl = os.path.join(lbl_dir, txt_name)
        dst_lbl = os.path.join(base_dir, split_name, 'labels', txt_name)
        if os.path.exists(src_lbl):
            shutil.move(src_lbl, dst_lbl)

print("Distributing files...")
move_files(train_imgs, 'train')
move_files(val_imgs, 'val')
move_files(test_imgs, 'test')

# Clean up the old master folders if they are empty
if not os.listdir(img_dir): os.rmdir(img_dir)
if not os.listdir(lbl_dir): os.rmdir(lbl_dir)

print("\nStratified Split Complete!")
print(f"Train: {len(train_imgs)} images (~75%)")
print(f"Val:   {len(val_imgs)} images (20% of each class)")
print(f"Test:  {len(test_imgs)} images (5% of each class)")