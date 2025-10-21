# Python Forensic Metadata Scripts 🕵️‍♂️

This repository contains a set of Python scripts that demonstrate basic digital forensic (DFIR) concepts, specifically focusing on metadata extraction and analysis.

It includes scripts for two main workflows:
1.  **Live File System Analysis:** Analyzing "live" file metadata (like MAC times) from your operating system and using `pandas` to filter and sort it.
2.  **Raw Disk Image Analysis:** Analyzing "dead" disk metadata from a raw forensic disk image (`.dd` file) using `pytsk3` (The Sleuth Kit).

---

## File Descriptions

* **`metadata.py`**: Scans a specified directory (e.g., `Images/`) for image files. It extracts their OS-level metadata (MAC times, file size, etc.) and saves the findings into a `image_metadata.csv` file.
* **`Analysis.py`**: Reads the `image_metadata.csv` file using `pandas`. It then demonstrates how to:
    * "Filter" for suspect files based on criteria (e.g., file extension).
    * "Reconstruct a timeline" by sorting all files based on their creation time.
* **`disk_image.py`**: Uses `pytsk3` to perform a low-level analysis on a raw disk image. It parses the partition table and can extract file metadata (MAC times, size) and content directly from the raw filesystem, bypassing the live OS.

---

## Requirements & Installation

It is **highly recommended** to use a Python virtual environment to manage these dependencies.

### Create and Activate Virtual Environment

```bash
# Navigate to your project folder
cd /Users//Desktop/image metadata/

# Create a virtual environment (e.g., named 'myenv')
python -m venv myenv

# Activate the environment
# On macOS/Linux:
source myenv/bin/activate
# On Windows PowerShell:
 .\myenv\Scripts\Activate.ps1


