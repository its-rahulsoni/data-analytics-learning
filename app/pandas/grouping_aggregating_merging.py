import os
import pandas as pd


class TitanicGroupAnalysis:
    """
    Covers Topic 2.3:
      - 5 self-made groupby questions
      - splitting the dataset into two tables and merging them back
      - one multi-column groupby aggregation
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None

    def load(self):
        self.df = pd.read_csv(self.csv_path)
        return self.df

    # -----------------------------------------------------------
    # 5 self-made questions
    # -----------------------------------------------------------

    """
    The core idea: split → apply → combine

    groupby() does exactly what the name says, in three conceptual stages:

    Split — break the DataFrame into multiple smaller groups, based on the values in the column(s) you group by. Every row with Pclass == 1 goes into one bucket, every row with 
    Pclass == 2 into another, Pclass == 3 into a third.
    Apply — run some calculation independently within each bucket (mean, sum, count, etc.)
    Combine — stitch the per-bucket results back together into a single Series/DataFrame, with the group labels as the index.

    This is the key thing to notice: df.groupby("Pclass") by itself does not compute anything. It returns a special intermediate object — a DataFrameGroupBy — which is really 
    just "the DataFrame, pre-sorted into buckets, waiting for you to tell it what to do with each bucket." Nothing gets calculated until you chain something onto it 
    (like .mean() or .sum()). This is sometimes called "lazy" — the grouping itself is cheap and instant; the real work happens at the next step.
    """

    """ 
    Where the "magic" really is, summarized

    There isn't actually hidden magic — it's the same building blocks you've used throughout this whole exercise, just composed in a new order:

    groupby(column) — reorganizes rows into buckets sharing the same value in that column (returns a lazy GroupBy object, computes nothing yet)
    ["column"] — narrows each bucket down to one column of interest (optional — skip it if you're just counting rows, like .size())
    .mean() / .sum() / .size() — an aggregation method that collapses each bucket into a single number
    Pandas automatically reassembles the per-bucket results into one Series, using the group values as the new index
    """

    # -----------------------------------------------------------
    
    """
    Q1: self.df.groupby("Pclass")["Fare"].mean()

    self.df.groupby("Pclass") — split into the 3 Pclass buckets you just saw above.

    ["Fare"] — from each bucket, narrow down to just the Fare column (same single-bracket-single-column pattern you already know, just applied to a GroupBy object instead of a 
    plain DataFrame). Now you have 3 buckets, each holding only a list of fare values.

    .mean() — the apply step: compute the average within each bucket separately. Class 1's fares get averaged together, class 2's separately, class 3's separately.

    Combine happens automatically: the three separate averages get assembled into one Series, with Pclass values (1, 2, 3) as the index labels — which is exactly the shape you 
    saw in your run output.
    """
    def q1_avg_fare_by_class(self):
        # Question: What is the average fare paid, per passenger class?
        return self.df.groupby("Pclass")["Fare"].mean()

    """
    Q2: self.df.groupby("Embarked")["Survived"].sum()

    Same shape, different grouping column and different aggregation. Split by Embarked (S/C/Q buckets), narrow to the Survived column, then .sum() each bucket. 
    Here's a neat detail: Survived is already 0/1 (0 = died, 1 = survived), so summing it within a group doesn't just add numbers abstractly — it directly counts 
    how many 1s (survivors) are in that group, because every survivor contributes exactly 1 to the total and every non-survivor contributes 0. Sum-of-a-0/1-column-as-a-count 
    is a pattern you already met with HasCabin and .isnull().sum().
    """
    def q2_survivors_by_embarked(self):
        # Question: How many passengers survived, per embarkation port?
        return self.df.groupby("Embarked")["Survived"].sum()

    """
    Q3: self.df.groupby("Sex")["Age"].mean()

    Same pattern again: split by Sex (male/female buckets), narrow to Age, average within each bucket.
    """
    def q3_avg_age_by_sex(self):
        # Question: What is the average age, per sex?
        return self.df.groupby("Sex")["Age"].mean()

    """
    Q4: self.df.groupby("Pclass").size()

    This one's slightly different — notice there's no column selection (["something"]) before the aggregation. .size() doesn't need to look at any particular column's values — 
    it just counts how many rows landed in each bucket, period. That's why it's called directly on the GroupBy object rather than on a narrowed-down column. 
    (A related method, .count(), is subtly different — it counts non-missing values per column, so it can give different answers across columns if there's missing data; 
    .size() just counts rows regardless of missingness. For a clean row count like this, .size() is the right one.)
    """
    def q4_passenger_count_by_class(self):
        # Question: How many passengers were in each class?
        return self.df.groupby("Pclass").size()

    """
    Q5: self.df.groupby("Sex")["Survived"].mean()

    Same shape as q1/q2/q3, but the interesting part is what averaging a 0/1 column actually means: the mean of a column containing only 0s and 1s is mathematically identical to 
    "the fraction that are 1." So .mean() on Survived doesn't give you an average survival number — it directly gives you the survival rate (a value between 0 and 1) for each sex. 
    This is a genuinely useful trick worth internalizing: mean-of-binary-column = proportion/rate.
    """
    def q5_survival_rate_by_sex(self):
        # Question: What fraction of passengers survived, per sex?
        return self.df.groupby("Sex")["Survived"].mean()

    def run_all_questions(self):
        print("Q1: Average fare by class")
        print(self.q1_avg_fare_by_class())

        print("\nQ2: Survivors by embarkation port")
        print(self.q2_survivors_by_embarked())

        print("\nQ3: Average age by sex")
        print(self.q3_avg_age_by_sex())

        print("\nQ4: Passenger count by class")
        print(self.q4_passenger_count_by_class())

        print("\nQ5: Survival rate by sex")
        print(self.q5_survival_rate_by_sex())

    # -----------------------------------------------------------
    # Split into two tables, then merge back
    # -----------------------------------------------------------

    """
    The two selections — both are the multiple-column selection pattern you already know (double brackets: outer [ ] selects from the DataFrame, inner [ ] is a list of column names). 
    Each line creates a new, smaller DataFrame containing only the listed columns, for all 891 rows.

    The one thing that makes this "a split" rather than just "two separate selections" is that PassengerId appears in both lists. That's deliberate — it's the shared key that will 
    let you glue these two tables back together later. Without a common column present in both halves, there'd be no way to know which row of ticket_info belongs with which row 
    of passenger_info once they're separate tables.

    return passenger_info, ticket_info — this returns two values at once. In Python, writing return a, b doesn't return two separate things in the way you might expect from 
    Java (which can only return one object, requiring a wrapper class or array for multiple values) — it actually packages them into a single tuple (passenger_info, ticket_info) 
    and returns that one tuple.
    """
    def split_tables(self):
        passenger_info = self.df[["PassengerId", "Name", "Sex", "Age"]]
        ticket_info = self.df[
            ["PassengerId", "Pclass", "Fare", "Ticket", "Embarked", "Survived"]
        ]
        return passenger_info, ticket_info # These are 2 separate tables containing 891 entries but only limited selected columns ....

    def merge_and_verify(self):
        """
        This line does two things in one step. It calls split_tables(), which returns that 2-element tuple — and then immediately unpacks it into two separate 
        variable names, passenger_info and ticket_info, matched by position (first tuple element → first variable name, second → second). This is the same unpacking behavior 
        demonstrated in the code above. It's Python's clean way of "catching" a function's multiple return values without dealing with tuple indexing (result[0], result[1]) by hand.
        """
        passenger_info, ticket_info = self.split_tables()

        """
        'pd.merge()' — another top-level pandas function (same family as pd.cut() and pd.date_range() from before). This is pandas' equivalent of a SQL JOIN, if you've ever used one — 
        it takes two separate tables and combines them into one, matching rows based on a shared key.

        passenger_info, ticket_info — the two tables to combine. Order here matters for column ordering in the result (passenger_info's columns appear first), but not for which rows match.

        on="PassengerId" — tells pandas which column to use as the matching key. For every row in passenger_info, pandas looks for the row in ticket_info that has the same 
        PassengerId value, and glues them together side-by-side into one wider row.

        how="inner" — this controls what happens when a key doesn't have a match on the other side. "inner" means: only keep rows where the key exists in both tables; 
        discard anything that doesn't match on both sides. Since every PassengerId exists in both passenger_info and ticket_info here (you split from the same original DataFrame, 
        so nothing was left out or added), every single row matches — nothing gets dropped. This is actually why your round-trip check works out cleanly.
        """

        """
        'how' has three other common values worth knowing, since "inner" is just one choice:

        "left" — keep every row from the first table, filling with NaN if there's no match in the second
        "right" — keep every row from the second table, same idea reversed
        "outer" — keep every row from both tables, filling NaN wherever a match is missing on either side
        """
        merged = pd.merge(passenger_info, ticket_info, on="PassengerId", how="inner")

        print(f"original row count: {len(self.df)}")
        print(f"passenger_info row count: {len(passenger_info)}")
        print(f"ticket_info row count: {len(ticket_info)}")
        print(f"merged row count: {len(merged)}")
        print(f"row counts match: {len(merged) == len(self.df)}")

        return merged

    # -----------------------------------------------------------
    # Multi-column groupby
    # -----------------------------------------------------------

    """
    This method looks almost identical to your single-column groupby methods from earlier — the only syntax difference is ["Pclass", "Sex"] (a list) instead of "Pclass" (a single string) 
    — but that one change produces a meaningfully different kind of result, which is worth exploring carefully.

    self.df.groupby(["Pclass", "Sex"])

    Passing a list of column names instead of a single string tells pandas to split into buckets based on the combination of both columns together, not each column separately. 
    Instead of 3 buckets (one per Pclass) or 2 buckets (one per Sex), you get up to 3 × 2 = 6 buckets — one for every distinct (Pclass, Sex) pairing that actually occurs in the data: 
    (1, female), (1, male), (2, female), (2, male), (3, female), (3, male).

    ["Survived"] and .mean()

    Same pattern as q5 from before — narrow each of those 6 buckets down to the Survived column, then average the 0/1 values within each bucket, which (as you learned) gives you 
    the survival rate for that specific class-and-sex combination.

    It's still a Series (one column of numbers), but its index is now a MultiIndex — a two-level, hierarchical row label instead of the single flat label you've seen everywhere 
    else (like Pclass alone, or Sex alone). Each row is now identified by a pair of labels — (1, "female"), (1, "male"), (2, "female"), and so on — rather than a single one. 
    That's why the printed output shows Pclass and Sex stacked as two separate label columns on the left, instead of one.
    """
    def survival_rate_by_class_and_sex(self):
        # Group by class AND sex together, get mean survival rate
        # for each combination
        return self.df.groupby(["Pclass", "Sex"])["Survived"].mean()


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "titanic.csv")

    analysis = TitanicGroupAnalysis(csv_path)
    analysis.load()

    print("=" * 60)
    print("5 GROUPBY QUESTIONS")
    print("=" * 60)
    analysis.run_all_questions()

    print("\n" + "=" * 60)
    print("SPLIT + MERGE ROUND TRIP")
    print("=" * 60)
    merged_df = analysis.merge_and_verify()

    print("\n" + "=" * 60)
    print("MULTI-COLUMN GROUPBY: SURVIVAL RATE BY CLASS AND SEX")
    print("=" * 60)
    print(analysis.survival_rate_by_class_and_sex())