import os
import numpy as np

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

# TASK:
# Take a 3x4 array and flatten it, then reshape it to 4x3, then to 2x6. Predict the output before running each reshape — write your prediction as a comment, then check ....

# Create the 3×4 array ....
mat = np.arange(1, 13).reshape(3, 4) # np.arange(1, 13) gives numbers 1 through 12 ....
print("\n 3×4 Dimensional array: \n", mat)
print("\n--------------------------------\n")
# --------------------------------------------------------------------------------------