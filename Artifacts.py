# artifacts.py

import subprocess
import json

def extract_metadata(filepath, artifact_id, source_id):
    """
    Runs exiftool on a file and returns its metadata as a list of
    (field, value) pairs.
    """
    try:
        process = subprocess.run(
            ['exiftool', '-j', '-G', filepath],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error processing {filepath}: {e}")
        return []

    # Exiftool returns a list containing one JSON object
    data = json.loads(process.stdout)[0]
    
    # Flatten the metadata
    flat_metadata = []
    for field, value in data.items():
        flat_metadata.append({
            'artifact_id': artifact_id, # Use the provided ID
            'source_id': source_id,      # Use the provided source
            'filepath': filepath,
            'field': field,
            'value': str(value) # Convert all values to string for easy comparison
        })
    return flat_metadata

# --- NEW ARTIFACTS LIST ---
# Let's create a list of files to process with their unique IDs.
# Make sure you have a few different images in your 'Images/' folder.
# For this example, I'll assume you have 'leaves.jpg' and 'other.jpg'.
# I'll also add a file from a different "source".

artifacts_to_process = [
    # Source 1: "Mobile"
    {'path': 'Images/test123.png', 'id': 'M_A1', 'source': 'S1_Mobile'},
    {'path': 'Images/test.png',  'id': 'M_A2', 'source': 'S1_Mobile'},
    
    # Source 2: "Laptop"
    # Let's re-use 'leaves.jpg' but pretend it's a copy on a laptop
    # This will help us find similarities
    {'path': 'Images/leaves.jpg', 'id': 'L_A1', 'source': 'S2_Laptop'}
]

all_metadata = []
for item in artifacts_to_process:
    all_metadata.extend(
        extract_metadata(item['path'], item['id'], item['source'])
    )
# --- END NEW ---

print(f"Extracted metadata from {len(artifacts_to_process)} artifacts.")
# Optional: a short print to see the metadata
# print(f"metadata entries: {json.dumps(all_metadata, indent=2)}")