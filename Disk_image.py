import pytsk3
import datetime

# --- Your helper functions (no change) ---
def process_filesystem(fs):
    root_dir = fs.open_dir(path="/")
    print("\n--- Files in root directory ---")
    for entry in root_dir:
        if entry.info.name.name not in [b'.', b'..']:
            print(entry.info.name.name.decode('utf-8'))

def tsk_timestamp_to_str(ts):
    if ts == 0:
        return "N/A"
    return datetime.datetime.fromtimestamp(ts).isoformat()
# ----------------------------------------


# Use the name of the real .dd file you downloaded
DISK_IMAGE_FILE = 'Images/ext-part-test-2.dd' 
# Make sure this file exists at this path!

try:
    # 1. Open the disk image
    img = pytsk3.Img_Info(DISK_IMAGE_FILE)

    # 2. Open the Volume System (Partition Table)
    try:
        vs = pytsk3.Volume_Info(img)
    except IOError:
        print("Could not open Volume System. Trying to open as single filesystem.")
        fs = pytsk3.FS_Info(img, offset=0)
        process_filesystem(fs)
        exit()


    # 3. Iterate over all partitions
    print(f"Found {vs.info.part_count} partition(s):")
    for part in vs:
        print(f"  -> Partition {part.addr}: {part.desc.decode('utf-8')} "
              f"({part.len} sectors, starts at {part.start})")

        # 4. Open the file system for THIS partition
        try:
            fs = pytsk3.FS_Info(img, offset=part.start * vs.info.block_size)
            
            # List files in the root of *this* partition
            print(f"\n--- Files in root of Partition {part.addr} ---")
            root_dir = fs.open_dir(path="/")
            for entry in root_dir:
                if entry.info.name.name in [b'.', b'..']:
                    continue
                
                if entry.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                    status = "DELETED"
                else:
                    status = "Active"

                print(f"{entry.info.name.name.decode('utf-8')} ({status})")

        except IOError:
            print(f"    Could not open filesystem in Partition {part.addr}. Skipping.")
            continue # Go to the next partition

        # --- THIS BLOCK IS NOW INDENTED ---
        # It is *inside* the 'for part in vs:' loop
        # and will run on the partition where fs was just opened
        if part.addr == 2:
            print(f"\n--- Analyzing Partition {part.addr} in detail ---")
            
            try:
                # Try to open the file
                file_obj = fs.open("/primary-1.txt") 
                
            except IOError:
                print("    ERROR: Could not open '/primary-1.txt'. File may be deleted or not exist.")
                continue # Skip to the next partition in the loop
            
            # --- If open was successful, proceed ---
            meta = file_obj.info.meta
            print(f"Successfully opened '/primary-1.txt':")

            # Get its metadata
            print(f"  File Size: {meta.size} bytes")
            print(f"  Last Modified (M): {tsk_timestamp_to_str(meta.mtime)}")
            print(f"  Last Accessed (A): {tsk_timestamp_to_str(meta.atime)}")
            print(f"  Created (C-Unix):  {tsk_timestamp_to_str(meta.ctime)}")
            print(f"  Entry Changed (C-NTFS): {tsk_timestamp_to_str(meta.crtime)}")
            
            # --- New, safer way to read content ---
            if meta.size > 0:
                try:
                    file_content = file_obj.read_random(0, meta.size)
                    print(f"  File Content: {file_content.decode('utf-8')}")
                except IOError as e:
                    print(f"  ERROR: Could not read file content: {e}")
                except UnicodeDecodeError:
                    print("  File Content: (Not plain text, cannot display)")
            else:
                print("  File Content: (File is empty)")
            
            print("------------------------------------------")
        
except IOError as e:
    # This will catch if 'Images/ext-part-test-2.dd' is not found
    print(f"Error opening image file: {e}")
except Exception as e:
    print(f"An error occurred: {e}")