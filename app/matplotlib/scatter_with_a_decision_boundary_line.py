import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(1)

"""
Understanding loc, scale, and size in np.random.normal():

First 10 values generated: 8.25, 3.78, 3.94, 2.85, 6.73, 0.4, 8.49, 3.48, 5.64, 4.5

Notice: even though you asked for loc=5 (mean 5), none of these individual numbers is exactly 5. That's the key thing to understand — loc and scale don't set a hard rule for every 
single value; they describe the shape of the whole cloud of 50 values, not any one point in it.

Across all 50 generated values: mean ≈ 4.95 (close to the requested 5, but not exact — with only 50 samples, you get some random variation), and standard deviation ≈ 1.94 
(close to the requested 2).

What loc (mean) actually controls —> where the cloud is centered.
Exp:- With loc=0, values cluster around 0 (ranging roughly -4.6 to 3.5). With loc=5, the entire cloud shifts — values now cluster around 5 (roughly 0.9 to 7.9). With loc=15, 
everything shifts again — clustered around 15 (roughly 12.8 to 17.3). loc just slides the whole bell curve left or right along the number line — think of it as "where is the 
center of the cloud."

------------------------------------------------------------------------------------------------------------------------

What scale (standard deviation) actually controls — how spread out the cloud is.
Exp:- All three batches are still centered around 5 — that hasn't changed, since loc=5 in every case. But look at how far values stray from 5:

scale=0.5 (tight): values stay very close to 5 — the widest swing is about ±1.2
scale=2 (medium): values wander further — down to 0.9, up to 7.9
scale=6 (wide): values scatter wildly — from -1.6 all the way to 11.9

So scale controls how loosely or tightly the values cluster around the loc center. A small scale gives you a tight, narrow cloud; a large scale gives you a wide, spread-out cloud. 
This is exactly the standard deviation from statistics — it's a number describing typical distance from the mean.

------------------------------------------------------------------------------------------------------------------------

What size controls — simply how many numbers you generate.
Exp:- size just decides how many random draws you make — size=5 gives you an array with 5 numbers, size=5000 gives you an array with 5000 numbers. Notice something interesting though: 
with only 5 numbers, the actual mean/spread of that tiny batch can look pretty different from 5 and 2. But with 5000 numbers, the actual mean (5.048) and actual std (2.005) 
land almost exactly on the requested loc=5 and scale=2. This is a real statistical property — the more samples you draw, the closer the batch's actual mean/spread matches the 
numbers you requested.

"""
x1 = np.random.normal(5, 2, 50)
x2 = np.random.normal(5, 2, 50)

"""
slope, intercept = -1.0, 10

Plain Python — multiple assignment in one line, equivalent to writing slope = -1.0 then intercept = 10 separately. These two numbers define a straight line using the familiar 
equation y = mx + b, where slope is m and intercept is b. This line is meant to represent a "decision boundary" — in real machine learning, this would be the line a trained 
classifier uses to separate two classes (e.g., everything above the line predicted as class A, everything below as class B). Here, you're just making up the slope and intercept 
by hand rather than training an actual model to find them — the point is practicing how to draw such a line, not how to compute one.
"""
# Made-up decision boundary: x2 = slope * x1 + intercept
slope, intercept = -1.0, 10

fig, ax = plt.subplots()

"""
ax.scatter(x1, x2, color="purple", alpha=0.6, label="Data points")

Draws your 50 data points as dots, using x1 as the x-coordinates and x2 as the y-coordinates for each point. This is a single .scatter() call this time (not looped, 
unlike the survival example), because you're not splitting these points into colored categories here — all 50 dots get the same single color, "purple".

alpha=0.6 — same transparency concept as before; slightly see-through so overlapping points are visually distinguishable as denser purple.
label="Data points" — stores this string on the artist (a PathCollection, same type .scatter() always creates), to be picked up later by ax.legend().

At this point, ax has one artist attached: a PathCollection of 50 purple dots.
"""
ax.scatter(x1, x2, color="purple", alpha=0.6, label="Data points")

"""
x_line = np.linspace(x1.min(), x1.max(), 100)

This is new — np.linspace(start, stop, num) generates num evenly spaced values between start and stop, inclusive of both endpoints. This is different from np.arange, 
which steps by a fixed increment and might not land exactly on your stop value — linspace instead lets you specify exactly how many points you want, and it calculates 
the spacing automatically to fit that count between the two endpoints.

01. x1.min() and x1.max() — .min() and .max() are numpy array methods that find the smallest and largest values inside x1. So this line finds the actual range your data spans 
(e.g., maybe roughly 1.2 to 9.4), rather than using arbitrary hardcoded bounds.

02. 100 — generates 100 points spanning that range.
"""
x_line = np.linspace(x1.min(), x1.max(), 100)


y_line = slope * x_line + intercept
ax.plot(x_line, y_line, color="black", linestyle="--", linewidth=2, label="Decision boundary")

ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.set_title("Scatter Plot with Decision Boundary")
ax.legend()
plt.show()