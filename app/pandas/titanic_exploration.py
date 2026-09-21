"""
Topic 2.1 - Loading and inspecting data (Titanic dataset)
"""

import os
import pandas as pd

# ---------------------------------------------------------------
# 1. LOAD THE CSV
# ---------------------------------------------------------------
# Path of the directory where THIS script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "titanic.csv")

df = pd.read_csv(csv_path)

"""
df.head(): shows the first 5 rows by default — a quick sanity check that the load worked and the columns look right.
Notice NaN in the Cabin column — that's pandas' way of marking "missing value." ....
"""
print("=== HEAD ===")
print(df.head())

"""
.info(): it tells you the total row count (891), then for each column: how many non-null (i.e., non-missing) values it has, 
and its dtype. Compare "Non-Null Count" to 891 (the total) — any gap means missing values.
"""
print("\n=== INFO ===")
df.info()

"""
.describe() only summarizes numeric columns by default (mean, std, min, quartiles, max). Note it shows count for each column too — 
another way to spot missing data: if count is less than 891, that column has gaps. It skips text columns like Name, Sex, Ticket 
unless you tell it otherwise.
"""
print("\n=== DESCRIBE ===")
print(df.describe())

# -----------------------------------------------------------------------
# Columns with missing values (from .info() Non-Null Count vs 891 total,
# confirmed with df.isnull().sum()):
#
#   Age       -> 177 missing (714 of 891 present)  | dtype: float64
#   Cabin     -> 687 missing (204 of 891 present)  | dtype: object (string)
#   Embarked  -> 2 missing   (889 of 891 present)  | dtype: object (string)
#
# All other columns (PassengerId, Survived, Pclass, Name, Sex, SibSp,
# Parch, Ticket, Fare) have 0 missing values.
#
# Data types in this dataset:
#   int64   -> PassengerId, Survived, Pclass, SibSp, Parch
#   float64 -> Age, Fare   (numbers that can have decimals / NaN)
#   object  -> Name, Sex, Ticket, Cabin, Embarked  (text/string columns)
# -----------------------------------------------------------------------

# ---------------------------------------------------------------
# 2. SELECTING DATA
# ---------------------------------------------------------------

# --- a) a single column ---
# Returns a Series (a single labelled column, like one column of Excel)
ages = df["Age"]
print("\n=== single column: Age (first 5) ===")
print(ages.head())

# --- b) multiple columns ---
# Pass a LIST of column names -> returns a DataFrame (not a Series)
subset = df[["Name", "Sex", "Age"]]
print("\n=== multiple columns: Name, Sex, Age (first 5) ===")
print(subset.head())

"""
Line 1: df[df["Age"] > 30]

This actually happens in two steps, inside out:

01. df["Age"] > 30 — this doesn't filter anything yet. It compares the entire Age column to 30 and returns a Series of True/False values,
one per row — True where that row's age is over 30, False otherwise (and False for missing ages too, since NaN > 30 is False). 
It's the same length as the whole DataFrame.

02. df[ ... ] — wrapping that True/False Series in square brackets and passing it back into df is pandas' filtering syntax. 
It keeps only the rows where the value was True, and drops the rest. This is called boolean indexing.

So over_30 = df[df["Age"] > 30] reads as: "make a new DataFrame containing only the rows where Age is greater than 30."

--------------------------------------------------------------------------------------------------------------------------------
Line 3: over_30[["Name", "Age"]].head()

Two more operations chained together:

over_30[["Name", "Age"]] — selecting multiple columns (the double brackets: outer [] is "select from the DataFrame," 
inner [] is a list of the column names you want). This narrows the result down to just those two columns, for all 216 rows.
.head() — trims that down to just the first 5 rows, purely so the printed output isn't 216 lines long.
"""
# --- c) rows where a condition holds ---
# df["Age"] > 30 makes a True/False Series; df[...] keeps only True rows
over_30 = df[df["Age"] > 30]
print(f"\n=== rows where Age > 30 ({len(over_30)} rows) ===")
print(over_30[["Name", "Age"]].head())

# --- d) rows by POSITION using .iloc ---
# .iloc = "integer location". Pure position, 0-indexed, like a numpy array.
# It does NOT care what the row's index label is.
print("\n=== .iloc[0:3] -> first 3 rows by position ===")
print(df.iloc[0:3])

print("\n=== .iloc[0:3, 0:2] -> first 3 rows, first 2 columns by position ===")
print(df.iloc[0:3, 0:2])

# --- e) rows by LABEL using .loc ---
# .loc = "location by label". Uses the actual index/column LABELS.
# Here the index labels happen to be 0,1,2... (same as position) because
# read_csv gave us a default RangeIndex - but that won't always be true.
print("\n=== .loc[0:2] -> rows labelled 0 through 2 (inclusive!) ===")
print(df.loc[0:2])

print("\n=== .loc[0:2, ['Name', 'Age']] -> by label, chosen columns ===")
print(df.loc[0:2, ["Name", "Age"]])

# Demonstrate why .loc and .iloc can differ: filter first, THEN select
filtered = df[df["Age"] > 30]   # this keeps the ORIGINAL index labels,
                                 # e.g. row labels might now be 1, 3, 6, 11...
print("\n=== after filtering, original labels are kept ===")
print(filtered.head())

print("\n=== .loc[1] on filtered -> row LABELLED 1 (Mrs Cumings) ===")
print(filtered.loc[1, ["Name", "Age"]])

print("\n=== .iloc[1] on filtered -> the 2nd row BY POSITION (not label 1) ===")
print(filtered.iloc[1][["Name", "Age"]])

# -----------------------------------------------------------------------
# .loc vs .iloc, in my own words:
#
# .iloc selects by POSITION - "give me the row/column at this numeric
# slot", counting from 0, regardless of what label is attached to it.
# It behaves exactly like numpy/list indexing.
#
# .loc selects by LABEL - "give me the row/column whose index/column
# NAME is this", regardless of where it physically sits in the table.
# Because it works on labels, .loc slices are INCLUSIVE of the end
# point (0:2 gives labels 0,1,2), whereas .iloc slices are EXCLUSIVE
# like normal Python slicing (0:2 gives positions 0,1 only).
#
# The two usually look identical on a freshly loaded DataFrame because
# the default index is 0,1,2,3... (label == position). They diverge as
# soon as the index is no longer a clean range - e.g. after filtering
# rows out (gaps appear in the labels), sorting, or setting a custom
# index (like PassengerId or a date column).
# -----------------------------------------------------------------------