# Forensic Metadata Analyzer


Its purpose is to forensically analyze a collection of digital artifacts (files) and discover both common and hidden relationships. It does this by running two models in parallel:

* **Similarity Model (Sp, Sg):** Finds obvious connections by clustering artifacts that share identical metadata field-value pairs (e.g., two photos taken with the same `Camera Model`).
* **Unique Model (UP, UG, UA):** Finds hidden, "sparse" associations by analyzing the metadata that the Similarity Model *ignored*. This can link two artifacts that share the same *value* in different *fields* (e.g., one file with `tag='stolen'` and another with `copyright='stolen'`)

---

## Requirements

This project has a critical system-level dependency.

1.  **Exiftool:** You **must** have Phil Harvey's [Exiftool](https://exiftool.org/) installed on your system. The Python library `pyexiftool` is just a wrapper and *will not work* unless the main `exiftool` command is available.

    * **macOS (using Homebrew):**
        ```bash
        brew install exiftool
        ```
    * **Windows / Linux:**
        [Download from the Exiftool website](https://exiftool.org/)

2.  **Python 3:** This project uses a virtual environment.

---

## How to Use

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/suravi73/python-forensic-scripts.git](https://github.com/suravi73/python-forensic-scripts.git)
    cd python-forensic-scripts
    ```

2.  **Set up the Environment**
    ```bash
    # Create a new virtual environment
    python3 -m venv venv

    # Activate it (macOS/Linux)
    source venv/bin/activate
    # (Windows)
    # .\venv\Scripts\activate

    # Install the required Python packages
    pip install pandas networkx pyexiftool
    ```

3.  **Add Your Artifacts**
    * Place all your files (images, documents, etc.) into the `Images/` folder (or a folder of your choice).

4.  **Configure the Analysis**
    * Open `Artifacts.py` with your code editor.
    * Edit the `artifacts_to_process` list to point to your files.
    * **Important:** Give each artifact a unique `id` and a `source` to simulate a real investigation (e.g., `S1_Mobile`, `S2_Laptop`).

    ```python
    # Example from Artifacts.py
    artifacts_to_process = [
        # Source 1: "Mobile"
        {'path': 'Images/leaves.jpg', 'id': 'M_A1', 'source': 'S1_Mobile'},
        {'path': 'Images/other.jpg',  'id': 'M_A2', 'source': 'S1_Mobile'},
        
        # Source 2: "Laptop" - a copy of leaves.jpg
        {'path': 'Images/leaves.jpg', 'id': 'L_A1', 'source': 'S2_Laptop'}
    ]
    ```

5.  **Run the Analyzer**
    ```bash
    python3 main_analyzer.py
    ```

The script will print the metadata extraction log, followed by the results from the Similarity and Unique models.

