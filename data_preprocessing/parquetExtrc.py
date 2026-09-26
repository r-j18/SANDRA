import os
import pandas as pd

# Update this with your actual parquet file path
parquet_path = "/run/media/artifex/FedoraStorage/rawdataset/train-00000-of-00001.parquet"

# Define where you want the raw extracted images to go
output_dir = "/run/media/artifex/FedoraStorage/rawdataset/parquet_extracted/images"
os.makedirs(output_dir, exist_ok=True)

# Load the parquet file
df = pd.read_parquet(parquet_path)

print(f"Extracting {len(df)} images...")

for index, row in df.iterrows():
    img_bytes = row['image.bytes']
    filename = row['image.path']
    
    # Ensure the filename ends with .jpg just in case the path column lacks it
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        filename = f"{filename}.jpg"
        
    out_path = os.path.join(output_dir, filename)
    
    # Write the raw bytes directly to a file
    with open(out_path, "wb") as f:
        f.write(img_bytes)

print(f"Extraction complete. Images saved to {output_dir}")