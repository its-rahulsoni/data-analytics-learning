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
