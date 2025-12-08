import os
import numpy as np
import pandas as pd

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

# -----------------------------------------------------------------------------------------------------------

# Creating a Series

print("Creating a Series\n")
sales = pd.Series([100, 200, 150, 300])
print(sales)
print("--------------------------------\n")

# -----------------------------------------------------------------------------------------------------------

### 5. Reading JSON Files

# Path of the directory where THIS script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "students.json")

print("### 5. Reading JSON Files\n")
df = pd.read_json(csv_path)
print("json file content:\n", df)

"""
Explanation:

read_json() converts list of dictionaries → DataFrame
Each dictionary becomes one row
"""
print("--------------------------------\n")

# -----------------------------------------------------------------------------------------------------------

### 6. Writing JSON

# Path of the directory where THIS script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "students_output.json")

print("### 6. Writing JSON\n")
df.to_json(csv_path, orient="records", indent=4)

"""
Explanation:

to_json() converts DataFrame → JSON
orient="records" → list of objects format (best & human-readable)
indent=4 → nicely formatted JSON
"""


