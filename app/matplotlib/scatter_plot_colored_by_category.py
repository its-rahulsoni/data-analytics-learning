import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- Synthetic "Titanic-like" dataset ---
np.random.seed(42)
n = 200
df = pd.DataFrame({
    "age": np.random.normal(loc=30, scale=12, size=n).clip(1, 80),
    "fare": np.random.exponential(scale=30, size=n),
    "survived": np.random.choice([0, 1], size=n, p=[0.6, 0.4])
})

fig, ax = plt.subplots()

"""
Plain Python — a dictionary mapping the two possible values of survived (0 or 1) to specific color names.
Why do this manually instead of letting matplotlib auto-color things? Because a single ax.scatter() call normally draws all points in one color. To get two different colors for 
two different groups, you need to make two separate .scatter() calls — one per group — each with its own color. That's exactly what the loop below sets up.
"""
colors = {0: "tomato", 1: "seagreen"}

"""
This is pandas, not matplotlib, but it's the mechanism that makes the coloring possible.

df.groupby("survived") splits your 200-row DataFrame into separate sub-tables based on the values in the survived column. Since survived only contains 0s and 1s, this produces exactly 
two groups: all rows where survived == 0, and all rows where survived == 1.

When you loop over a groupby object, each iteration hands you a tuple: status (the group's key — either 0 or 1) and group (a DataFrame containing only the rows belonging to that group). 
So this loop runs exactly twice:

1st iteration: status = 0, group = the ~120 rows where survived is 0
2nd iteration: status = 1, group = the ~80 rows where survived is 1
"""

"""
This runs once per loop iteration (so twice total), and each call draws one batch of points onto the same ax.

group["age"], group["fare"] — the x and y coordinates. For each row in this group, .scatter() plots one point at (that person's age, that person's fare). Internally, matplotlib 
creates a PathCollection artist — this is the scatter-plot equivalent of the Rectangle artists from the histogram, except instead of 20 bars, it's one artist object representing 
the entire batch of dots from this call (not one artist per point — that's a performance optimization, since you might have thousands of points).

c=colors[status] — looks up the color for this specific group from your dictionary. On the first loop iteration status is 0, so colors[0] gives "tomato" — every point drawn in this 
call is tomato red. On the second iteration, colors[1] gives "seagreen". This is precisely why we needed the dictionary and the loop: two calls, two different fixed colors.

label=f"Survived = {status}" — an f-string that inserts the value of status directly into the text. First call produces the label "Survived = 0", second produces "Survived = 1". 
Critically, this label is stored on the artist itself but not displayed anywhere yet — it's just metadata attached to this batch of points, waiting to be picked up later by ax.legend().

alpha=0.7 — sets transparency, on a scale from 0 (fully invisible) to 1 (fully solid). At 0.7, points are slightly see-through. This matters because scatter points frequently overlap — with full opacity, a point sitting exactly on top of another would completely hide it; with transparency, overlapping regions look visibly darker/denser, giving you a rough sense of "lots of points are clustered here" just from the visual.

After both loop iterations finish, ax now has two PathCollection artists attached to it — one tomato batch, one seagreen batch — each remembering its own label string.
"""
for status, group in df.groupby("survived"):
    ax.scatter(
        group["age"], group["fare"],
        c=colors[status],
        label=f"Survived = {status}",
        alpha=0.7
    )

ax.set_xlabel("Age")
ax.set_ylabel("Fare")
ax.set_title("Age vs Fare, Colored by Survival")

"""
This is the new piece. .legend() walks through every artist currently attached to ax (both PathCollection objects from the loop) and checks each one for a stored label. 
For every artist that has one, it builds a small legend box: a colored swatch (matching that artist's actual color) paired with its label text, and places this box on the plot 
(matplotlib auto-picks a corner that overlaps your data least, by default).

This is why setting label= back in .scatter() mattered even though nothing appeared on screen at the time — the label was silently stored on the artist, and .legend() is the one call 
that later goes and collects all those stored labels into a visible key.
"""
ax.legend()
plt.show()