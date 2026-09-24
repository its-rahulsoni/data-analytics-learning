import os
import pandas as pd


class TitanicCleaner:
    """
    Cleans the raw Titanic dataset:
      - handles missing values in Age, Cabin, Embarked
      - fixes a conceptually wrong dtype (Pclass -> category)
      - creates derived columns (Title, AgeGroup, HasCabin)
    """

    # __init__ specifically means "run this when an object is created." ....
    # In Python, 'self' is explicit: it's the first parameter of every instance method, and you have to write it yourself ....
    def __init__(self, csv_path):
        """
        There is no prior step where you write something like self.csv_path: str first. This single line simultaneously:

        01. Creates the attribute csv_path on the object
        02. Assigns it the value passed in
        """
        self.csv_path = csv_path
        self.df = None

    def load(self):
        self.df = pd.read_csv(self.csv_path)
        return self.df

    """
    This line -> missing = self.df.isnull().sum()

    This is two chained operations happening left to right.

    Step 1 — self.df.isnull()

    This doesn't touch just one column — it runs across the entire DataFrame and returns a new DataFrame of the exact same shape (891 rows × 12 columns), but every single cell is replaced 
    with True (if that cell was missing/NaN) or False (if it had a real value). Think of it as an X-ray of your table showing only "is this cell empty?"

    Step 2 — .sum()

    Called on that True/False grid, .sum() adds up each column independently, top to bottom. Here's the trick that makes this work: Python (and pandas) treat True as 1 and False as 0 
    when you do arithmetic on them. So summing a column of [False, False, True, False, True, ...] is really summing [0, 0, 1, 0, 1, ...] — the total is simply the count of missing values 
    in that column.

    The result of .sum() on a DataFrame is a Series: one number per column, with the column names as the index labels. That's exactly the shape of your printed output — Age, Cabin, Embarked 
    are index labels, and the numbers next to them (177, 687, 2) are the sums.
    """
    def report_missing(self):
        missing = self.df.isnull().sum()
        print(missing[missing > 0])

    """
    Code:- mode_port = self.df["Embarked"].mode()[0]

    Three things chained together here.

    Step 1 — self.df["Embarked"]

    Single brackets around a single column name → this pulls out the Embarked column as a Series (you already know this pattern from earlier — single [ ] with one column name gives a Series, not a DataFrame).

    Step 2 — .mode()

    The mode is a statistics term for "the most frequently occurring value." Calling .mode() on the Embarked Series scans all 889 non-missing entries (S, C, or Q — the three ports: Southampton, Cherbourg, Queenstown) and returns whichever one appears most often.

    Here's the subtle bit: .mode() doesn't return a single value — it returns a Series, even if there's only one answer. Why a Series and not just a plain string? Because it's technically possible for two or more values to be tied for "most frequent" (e.g. if S and C both appeared exactly 445 times), in which case .mode() would return both of them. Pandas always returns a Series here so it can handle that tie case without changing the return type depending on the data.

    Step 3 — [0]

    Since .mode() gives back a Series (which is indexed like a list, 0, 1, 2...), [0] grabs the first entry out of it — in effect saying "just give me the single most common value, I know there's likely only one." For the Titanic dataset, .mode() returns just ['S'], so [0] extracts the plain string 'S' (Southampton — the vast majority of passengers boarded there).

    So after this line, mode_port is simply the string 'S'.

    -------------------------------------------------------------------------

    Code:- self.df["Embarked"] = self.df["Embarked"].fillna(mode_port)

    This is a read-modify-write pattern, and it's worth seeing it that way explicitly:

    Read: self.df["Embarked"] on the right-hand side — grab the current Embarked column.

    Modify: .fillna(mode_port) — this is the actual fixing operation. fillna() scans the Series and, wherever it finds a NaN (missing value), replaces it with whatever you passed in 
    — here, 'S'. Every non-missing value is left completely untouched. Critically, fillna() doesn't modify the column in place by default — it returns a brand new Series with the 
    fix applied, leaving the original column as it was.

    Write: self.df["Embarked"] = ... on the left-hand side — takes that new, fixed Series and overwrites the old Embarked column with it.
    """
    def handle_missing_embarked(self):
        # Only 2 missing values out of 891 -> fill with the most common port (mode)
        mode_port = self.df["Embarked"].mode()[0]
        self.df["Embarked"] = self.df["Embarked"].fillna(mode_port)

    """
    Code:- median_age = self.df["Age"].median()

    Step 1 — self.df["Age"] — same as before, pulls out the Age column as a Series (single brackets, single column name).

    Step 2 — .median() — the median is "the middle value if you sorted every age from lowest to highest." With 714 known ages, .median() sorts them all and picks the one sitting exactly in the middle (position 357 of 714, roughly — pandas handles the exact tie-breaking for even counts internally by averaging the two middle values).

    Unlike .mode(), .median() returns a single plain number directly — no [0] needed, because there's no ambiguity about ties the way there can be with "most frequent value." 
    There's always exactly one middle position in a sorted list.

    Code:- self.df["Age"] = self.df["Age"].fillna(median_age)

    Identical pattern to the Embarked line: read the Age column, call .fillna(median_age) to produce a new Series where every missing entry is replaced with the median value 
    (all 177 NaN ages become that one number), and reassign it back onto self.df["Age"] to overwrite the column with the fixed version.
    """
    def handle_missing_age(self):
        # Age is skewed (a few much older passengers) -> median is more
        # robust to outliers than mean
        median_age = self.df["Age"].median()
        self.df["Age"] = self.df["Age"].fillna(median_age)

    """
    Code:- self.df["HasCabin"] = self.df["Cabin"].notnull().astype(int)

    Three operations chained on the right-hand side, then an assignment.

    Step 1 — self.df["Cabin"] — pulls out the Cabin column as a Series, same pattern as always.

    Step 2 — .notnull() — this is the exact opposite of .isnull() from report_missing(). It returns a True/False Series: True where the cell has a real cabin value, False where it's NaN. 
    So instead of asking "is this missing?", it asks "is this present?"

    Step 3 — .astype(int) — converts that True/False Series into a 1/0 Series. This is the same True→1, False→0 conversion pandas does automatically during arithmetic (which is how .sum() 
    counted missing values earlier) — but here we're doing it explicitly and keeping the result as actual integer data, rather than just using it internally for a sum. astype() in 
    general converts a Series from one dtype to another; here specifically boolean → int64.

    The assignment — self.df["HasCabin"] = ...

    This is worth pausing on because it's a new pattern you haven't used yet in this class: creating a brand new column. So far you've seen self.df["Age"] = ... 
    and self.df["Embarked"] = ..., which overwrite an existing column with a fixed version of itself. But "HasCabin" doesn't exist yet anywhere in the original CSV — pandas doesn't 
    need a column to already exist to assign to it. The moment you assign to self.df["some_new_name"], if that name isn't already a column, pandas simply creates it and appends it to 
    the DataFrame. Same syntax, but the effect is "add a new column" rather than "replace an old one," purely depending on whether that column name already existed.

    So after this line, your DataFrame has a brand new column called HasCabin, holding 1 for the 204 passengers who had a recorded cabin, and 0 for the 687 who didn't.

    -------------------------------------------------------------------------

    Code:- self.df = self.df.drop(columns=["Cabin"])

    .drop(columns=["Cabin"]) — removes the Cabin column entirely. Notice the argument is a list (["Cabin"]) even though we're only dropping one column — that's because drop(columns=...) 
    s designed to accept multiple column names at once (e.g. ["Cabin", "Ticket"]), so it always expects a list, even a one-item one.

    Just like .fillna(), .drop() does not modify self.df in place by default — it returns a new DataFrame with that column removed, leaving the original untouched. That's exactly why 
    the line reassigns: self.df = self.df.drop(...) — read the current self.df, compute a version without Cabin, then overwrite self.df with that new version. Skip the self.df = part 
    and, same trap as with fillna() earlier, the drop would be silently discarded and Cabin would still be sitting there.

    (Small aside: .drop() does have an inplace=True option that modifies the DataFrame directly without needing reassignment — but it's increasingly discouraged in modern pandas, 
    because it can silently produce different behavior on filtered/sliced data. The reassignment pattern you're using here is the safer, recommended habit.)
    """
    def handle_missing_cabin(self):
        # 687 of 891 missing (77%) -> too sparse to fill meaningfully.
        # Instead of guessing cabin numbers, keep the one useful signal:
        # whether the passenger had a recorded cabin at all.
        self.df["HasCabin"] = self.df["Cabin"].notnull().astype(int)
        self.df = self.df.drop(columns=["Cabin"])

    """
    Code: self.df["Pclass"] = self.df["Pclass"].astype("category")

    self.df["Pclass"] — pulls out the Pclass column, same pattern as always. If you check .info() from earlier, you'll recall it showed Pclass as int64 — the values are literally 
    1, 2, or 3.

    .astype("category") — converts the column from one dtype to another. You've already met .astype(int) in the previous method (bool → int); this is the same mechanism, 
    just converting to pandas' special category dtype instead. Passing the string "category" (rather than a Python type like int or float) tells pandas: 
    "treat this column as a fixed set of discrete labels, not as numbers."

    The reassignment — self.df["Pclass"] = ... — same pattern as every method before this: .astype() returns a new Series with the converted dtype rather than changing the original 
    in place, so it has to be reassigned back onto self.df["Pclass"] to actually take effect.

    Question: Why is int64 "wrong" here, if the values genuinely are 1, 2, 3 ??
    Answer: int64 implies the values are quantities: you can meaningfully add them, average them, compute a standard deviation, say 3 > 1. But Pclass isn't a quantity — it's a label 
    for which travel class a passenger booked (1st, 2nd, 3rd class). Averaging Pclass across passengers and getting 2.31 (which you actually saw earlier in .describe()) 
    is numerically valid but conceptually meaningless — there's no real-world interpretation of "the average class was 2.31." It's a category being accidentally treated as a number 
    because it happens to be represented with digits.
    """
    def fix_dtypes(self):
        # Pclass is stored as int64, but it represents a category
        # (1st/2nd/3rd class), not a quantity you'd ever average.
        # Converting to 'category' fixes that mismatch.
        self.df["Pclass"] = self.df["Pclass"].astype("category")

    """
    self.df["Name"] — nothing new here, pulls out the Name column as a Series of strings, e.g. "Braund, Mr. Owen Harris".
    .str — the string accessor

    Here's a new concept: self.df["Name"] is a whole column (a Series), not a single Python string. You can't directly call .extract() on a Series the way you'd call a string method on one string — a Series doesn't have string methods.

    .str is pandas' bridge for this: it's an "accessor" that lets you apply a string operation to every value in the column at once, without writing a loop. Whatever comes after .str — .extract(), or things like .lower(), .contains(), .split() — gets applied individually to each entry in the column, and the results come back as a new Series, same length, same order. Think of it as "vectorized" string methods — one instruction, applied to all 891 rows simultaneously.

    .extract(r",\s*([^\.]+)\.") — the regex

    .extract() takes a regular expression (regex) — a pattern language for matching pieces of text — and pulls out just the part of each string that matches a specific "capture group" you define. Let's decode the pattern itself, character by character. The r"..." prefix is a raw string, which just tells Python not to interpret backslashes specially (so \. stays as literally backslash-dot, rather than Python trying to treat it as an escape sequence) — this is a Python detail, not a regex detail, but always used with regex patterns for exactly this reason.
    """
    def add_title_column(self):
        # Extract the title (Mr, Mrs, Miss, Master, etc.) from the Name field
        self.df["Title"] = self.df["Name"].str.extract(r",\s*([^\.]+)\.")

    """
    'cut' is a top-level pandas function (you call it as pd.something), not a method that lives on Series/DataFrame objects.

    pd.cut(self.df["Age"], bins=bins, labels=labels)

    This function takes every value in the Age column and checks which bin it falls into, then replaces the raw number with the 
    corresponding label. So a passenger aged 22 becomes "Young Adult", a passenger aged 8 becomes "Child", and so on — for all 
    891 rows at once (this is another vectorized operation, same spirit as .str.extract(), just for numeric bucketing instead
    of string pattern matching).

    One important detail about pd.cut()'s default behavior: the parentheses/brackets notation above — (0, 12] — means the 
    interval is open on the left, closed on the right.
    """
    def add_age_group_column(self):
        # Bucket the continuous Age column into readable ranges
        bins = [0, 12, 18, 35, 60, 100]
        labels = ["Child", "Teen", "Young Adult", "Adult", "Senior"]
        self.df["AgeGroup"] = pd.cut(self.df["Age"], bins=bins, labels=labels)

    def clean(self):
        self.load()
        print("Missing values BEFORE cleaning:")
        self.report_missing()

        self.handle_missing_embarked()
        self.handle_missing_age()
        self.handle_missing_cabin()
        self.fix_dtypes()
        self.add_title_column()
        self.add_age_group_column()

        print("\nMissing values AFTER cleaning:")
        self.report_missing()

        print("\nDtypes AFTER cleaning:")
        print(self.df.dtypes)

        return self.df


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "titanic.csv")

    cleaner = TitanicCleaner(csv_path)
    clean_df = cleaner.clean()

    print("\nSample of cleaned data:")
    print(clean_df[["Name", "Title", "Age", "AgeGroup", "Pclass", "HasCabin", "Embarked"]].head(10))

    output_path = os.path.join(BASE_DIR, "titanic_cleaned.csv")
    clean_df.to_csv(output_path, index=False)
    print(f"\nSaved cleaned dataset to {output_path}")