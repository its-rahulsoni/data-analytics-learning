import os
import numpy as np

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

# TOPIC 3: Matrix Multiplication (Dot Product & ML Use-Cases)

print("TOPIC 3: Matrix Multiplication (Dot Product & ML Use-Cases)")
print("--------------------------------\n")

# -----------------------------------------------------------------------------------------------------------

# ✅ 1️⃣ Dot Product (1D vectors)

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("✅ 1️⃣  Dot Product (1D vectors)")
print(np.dot(a, b))

"""
### ✅ What is Dot Product (for 1D vectors)?

For two 1D vectors, the dot product is:

Multiply each pair of corresponding elements,
then add all products.

Mathematically:
a⋅b = a1b1 + a2b2 + a3b3

"""
print("--------------------------------\n")

# -----------------------------------------------------------------------------------------------------------

# ✅ 2️⃣ Matrix × Matrix Multiplication (2D arrays)

A = np.array([
    [1, 2],
    [3, 4]
])

B = np.array([
    [5, 6],
    [7, 8]
])

print("✅ 2️⃣  Matrix × Matrix Multiplication (2D arrays)")
print(A @ B)

"""
Compute row × column:
Row1⋅Col1 = 15 + 27 = 19
Row1⋅Col2 = 16 + 28 = 22
Row2⋅Col1 = 35 + 47 = 43
Row2⋅Col2 = 36 + 48 = 50

⭐ Important Rules (You MUST remember them)

To multiply A(m × n) with B(n × p):
Inner dimensions (n) must match
Result is shape → (m × p)
"""

print("--------------------------------\n")

# -----------------------------------------------------------------------------------------------------------

# ✅ 3️⃣ Matrix × Vector multiplication

W = np.array([
    [0.2, 0.8, -0.5],
    [1.0, -1.0, 0.3]
])   # shape (2,3)

x = np.array([1, 2, 3])  # shape (3,)

print("✅ 3️⃣  Matrix × Vector multiplication")
print(W @ x)
print("--------------------------------\n")

# -----------------------------------------------------------------------------------------------------------

# ✅ 4️⃣ Inner Product (Dot-like operation)

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

result = np.inner(a, b)
print("✅ 4️⃣  Inner Product (Dot-like operation)")
print("Inner Product: ", result)
print("--------------------------------\n")

"""
For 1D vectors, inner product = sum of elementwise products, same as dot product.
inner(a,b)=a1b1 + a2b2 + a3b3 + ......
Result - Single numerical value.
"""

# -----------------------------------------------------------------------------------------------------------

# ✅ 5️⃣ Outer Product

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

result = np.outer(a, b)
print("✅ 5️⃣  Outer Product")
print("Outer Product: \n", result)
print("--------------------------------\n")

"""
It creates a matrix where:
every element of a multiplies
every element of b

outer(a,b) =
[ a1b1  a1b2  ]
[ a2b1  a2b2  ]

"""
# -----------------------------------------------------------------------------------------------------------

"""
⭐ What are mean / variance / standard deviations ?

Mean (average) — gives the central tendency of data. In ML/data-analysis, you often inspect mean to understand the “typical” value in a feature.

Variance — measures how spread out values are around the mean. High variance → data is spread out. Useful in understanding feature distribution, detecting outliers.

Standard Deviation (std) — square root of variance; in same units as data. Helps gauge “typical deviation” from mean.
"""
print("1D array - mean / variance / standard deviations")
# Example 1D data: ages of students
ages = np.array([18, 20, 22, 19, 21, 20, 23, 22])

# Compute mean
mean_age = np.mean(ages) # computes arithmetic mean: sum of all values divided by number of values.
print("Mean age:", mean_age) 

# Compute variance
var_age = np.var(ages) # computes variance: average of squared deviations from mean.
print("Variance of age:", var_age)

# Compute standard deviation
std_age = np.std(ages) # computes standard deviation: sqrt of variance.
print("Standard deviation of age:", std_age)

print("--------------------------------\n")

data = np.array([
    [18, 50000, 85],
    [20, 55000, 90],
    [22, 60000, 88],
    [19, 52000, 87]
])

print("2D array - mean / variance / standard deviations")

# Mean of each column (feature-wise stats)
feature_means = np.mean(data, axis=0)
print("Feature means:", feature_means)

# Std dev of each column
feature_std = np.std(data, axis=0)
print("Feature std:", feature_std)

# If you want row-wise mean (per sample)
row_means = np.mean(data, axis=1)
print("Row means:", row_means)

print("--------------------------------\n")

# -----------------------------------------------------------------------------------------------------------