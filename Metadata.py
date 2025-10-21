import os
import csv
import datetime

# --- 1. Setup ---

# The directory you want to scan ('.' means the current directory)
directory_to_scan = 'Images' 
csv_output_file = 'image_metadata.csv'

# A list of image extensions to look for
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

# This is where we will store the data we find
collected_data = []

print(f"Scanning {directory_to_scan} for images...")

# --- 2. Data Collection 📂 ---
# os.walk() goes through all folders and subfolders
for root, dirs, files in os.walk(directory_to_scan):
    for filename in files:
        # Check if the file's extension is in our list
        if filename.lower().endswith(image_extensions):
            
            # Recreate the full file path
            file_path = os.path.join(root, filename)
            
            try:
                # Get the file's metadata (stat info)
                stat_info = os.stat(file_path)
                
                # Get the file extension
                extension = os.path.splitext(filename)[1]
                
                
                # Create a dictionary, just like your example data
                file_metadata = {
                    'filename': filename,
                    'creation_time': stat_info.st_ctime,
                    'Modified_time': stat_info.st_mtime,
                    'Accessed_time': stat_info.st_atime,
                    'file_extension': extension,
                    'full_path': file_path, # Good to store this too
                    'size_bytes': stat_info.st_size
                }
                
                # Add this file's data to our main list
                collected_data.append(file_metadata)
                
            except FileNotFoundError:
                print(f"Could not find {file_path}")
            except PermissionError:
                print(f"No permission to read {file_path}")


print(f"Found {len(collected_data)} image files. Now writing to CSV...")

# --- 3. Write to CSV ✍️ ---
# Check if we actually found any data
if collected_data:
    # Define the headers for our CSV file
    # We get these from the keys of the first dictionary in our list
    headers = collected_data[0].keys()

    # Open the CSV file in 'write' mode ('w')
    # newline='' is required for the csv module
    with open(csv_output_file, 'w', newline='', encoding='utf-8') as f:
        
        # Create a DictWriter object, which maps dictionaries to CSV rows
        writer = csv.DictWriter(f, fieldnames=headers)
        
        # Write the first line (the headers)
        writer.writeheader()
        
        # Write all our collected data
        writer.writerows(collected_data)

    print(f"Successfully created {csv_output_file}!")

else:
    print("No image files were found in this directory.")