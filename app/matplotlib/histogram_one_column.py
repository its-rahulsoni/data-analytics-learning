import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- Synthetic "Titanic-like" dataset ---

"""
np.random.seed(42)

This fixes the "randomness" so it's reproducible. Computers don't generate truly random numbers — they use a pseudo-random algorithm that needs a starting point (the "seed"). 
If you set the seed to a specific number, you get the exact same sequence of "random" numbers every time you run the code.
"""
np.random.seed(42)

"""
n = 200

Just a plain variable holding the number 200 — the number of rows (passengers) we want in our fake dataset. Defining it once and reusing it below means if you want 500 passengers instead, 
you change one number instead of three.
"""
n = 200

"""
pd.DataFrame({...})

This creates a pandas DataFrame — think of it as a table, like an Excel sheet or SQL table, where each key in the dictionary becomes a column name, and its value (an array of numbers) 
becomes that column's data. We're passing a dictionary with three keys: "age", "fare", "survived" — so we'll end up with a 200-row, 3-column table.
"""
df = pd.DataFrame({
    "age": np.random.normal(loc=30, scale=12, size=n).clip(1, 80),
    "fare": np.random.exponential(scale=30, size=n),
    "survived": np.random.choice([0, 1], size=n, p=[0.6, 0.4])
})

"""
"age": np.random.normal(loc=30, scale=12, size=n).clip(1, 80)

np.random.normal(loc=30, scale=12, size=n) draws 200 random numbers from a normal (bell-curve) distribution. loc=30 is the mean (center of the bell curve — most ages cluster around 30), 
scale=12 is the standard deviation (how spread out the values are — bigger number means wider spread), size=n means generate 200 of these values, one per row.

Problem: a normal distribution technically has no hard limits, so with mean 30 and spread 12, you could randomly get a negative age or a wildly implausible age like 150. 
That's not realistic for a person's age.

.clip(1, 80) fixes that — it's a method that forces every value into the range [1, 80]. Any generated number below 1 gets pushed up to 1, and anything above 80 gets pushed down to 80. 
This keeps the ages realistic.
"""

"""
"fare": np.random.exponential(scale=30, size=n)

np.random.exponential(scale=30, size=n) draws 200 values from an exponential distribution instead of a normal one. This distribution is intentionally lopsided — lots of small values, 
a long tail of rare large values, and it never goes negative. scale=30 roughly controls the average value.

Why exponential and not normal here? Because real-world ticket prices behave this way — most passengers pay a modest fare, a few pay a lot (first class), and fares can never be negative.
A normal distribution would incorrectly allow negative fares and wouldn't capture that "many cheap, few expensive" skew.
"""

"""
"survived": np.random.choice([0, 1], size=n, p=[0.6, 0.4])

np.random.choice([0, 1], size=n, p=[0.6, 0.4]) randomly picks 200 values, each either 0 or 1, simulating a binary outcome (didn't survive / survived).

p=[0.6, 0.4] sets the probability weighting: 60% chance of picking 0, 40% chance of picking 1 for each draw — roughly matching the real Titanic dataset's survival rate, 
where most passengers didn't survive.
"""

# --- Histogram ---
# fig, ax = plt.subplots()
# ax.hist(df["age"], bins=20, color="steelblue", edgecolor="black")
# ax.set_xlabel("Age")
# ax.set_ylabel("Number of Passengers")
# ax.set_title("Distribution of Passenger Age")
# plt.show()


fig, ax = plt.subplots()

"""
Now the buckets are (0 to 10), (10 to 20), (20 to 30) ... (70 to 80).
When a value sits exactly on a shared edge (say, someone is exactly age 30), matplotlib's convention is to put it in the right-hand bucket (30–40), not the left (20–30) — 
bins are half-open like [20, 30), except the very last bin which includes both ends.
"""
age_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80]

"""
.hist(): actually returns three things every time:

counts — a numpy array of how many values landed in each bin (e.g., [12, 34, 45, ...])
bin_edges — the boundary values (same as your age_bins input, echoed back)
patches — a BarContainer object holding references to the actual Rectangle artists that got drawn (the same ones we discussed last time — one per bar)
"""
counts, bin_edges, patches = ax.hist(df["age"], bins=age_bins, color="steelblue", edgecolor="black")

ax.set_xlabel("Age Group")
ax.set_ylabel("Number of Passengers")
ax.set_title("Distribution of Passenger Age (by Decade)")

# A tick is one of those little marks along an axis — the small line perpendicular to the axis, plus the number/label printed next to it. On your x-axis, ticks are what let you 
# look at a bar and know "oh, this one starts at 30."
ax.set_xticks(age_bins)

# It takes a BarContainer (a group of bar/rectangle artists), reads each bar's height, and automatically places a Text artist directly above each bar showing that height as a number.
ax.bar_label(patches)

plt.show()

