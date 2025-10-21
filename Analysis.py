import pandas as pd
import sys

# The CSV file we created in the previous step
csv_file_to_read = 'image_metadata.csv'

# --- 1. Load the data from the CSV file ---
try:
    # This line REPLACES the manual 'data = {...}' dictionary
    df = pd.read_csv(csv_file_to_read)
    
    print(f"--- Successfully loaded '{csv_file_to_read}' ---")
    # print(df.head()) # Uncomment to see the first 5 rows

except FileNotFoundError:
    print(f"Error: The file '{csv_file_to_read}' was not found.")
    print("Please make sure the file is in the same directory.")
    sys.exit() # Exit the script if we can't find the file
except Exception as e:
    print(f"An error occurred reading the file: {e}")
    sys.exit()


# --- 2. Implementation: "Filter... to locate a precise suspect document" ---

# We filter for '.png' files, since our CSV contains images.
# The logic is identical to filtering for '.exe' files.
suspect_extension = '.png'
suspects = df[df['file_extension'] == suspect_extension]

print(f"\n--- Suspect Files (Filtered for '{suspect_extension}') ---")
if suspects.empty:
    print(f"No files found with the extension '{suspect_extension}'.")
else:
    # Print the relevant columns for our "suspects"
    print(suspects[['filename', 'full_path', 'size_bytes']])


# --- 3. Implementation: "Reconstruct the timeline" ---

# This part works exactly the same as your original script.
# We sort all files by their creation time.
timeline = df.sort_values(by='creation_time')

print("\n--- Reconstructed Timeline (Oldest First) ---")
# Print the timeline, showing the time and filename
print(timeline[['creation_time', 'filename']])