import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


"""
epochs = np.arange(1, 51)

np.arange(start, stop) generates a numpy array of evenly spaced integers, starting at start and going up to (but not including) stop. So np.arange(1, 51) 
produces [1, 2, 3, 4, ..., 50] — 50 values total.
"""
epochs = np.arange(1, 51)    # steps 1 through 50

"""
loss = 2.5 * np.exp(-0.08 * epochs) + np.random.normal(0, 0.03, size=50)

This builds fake but realistic-looking loss values, in two parts added together.

Part 1 — 2.5 * np.exp(-0.08 * epochs): the decay curve

np.exp(x) computes e^x (Euler's number raised to the power x) for every element in the array — this is numpy's element-wise exponential function.

Here, x = -0.08 * epochs, so as epochs grows from 1 to 50, this exponent becomes increasingly negative (-0.08, -0.16, ... down to -4.0). Raising e to an increasingly 
negative power produces a curve that starts near 1 and shrinks rapidly toward 0 — this is the classic "exponential decay" shape.

Multiplying the whole thing by 2.5 just scales the curve up, so it starts around 2.5 instead of 1, and still decays toward 0. This mimics a real training loss: 
high at the start (model knows nothing), dropping fast early on, then flattening out as it approaches its minimum.
"""
"""
Part 2 — np.random.normal(0, 0.03, size=50): the noise

Same function you saw for generating ages earlier, but here loc=0 (mean 0) and scale=0.03 (small spread). This generates 50 small random values centered around 0 — sometimes 
slightly positive, sometimes slightly negative, but always small.

Adding this to the clean decay curve makes it look like a real training run, where loss doesn't drop in a perfectly smooth line — it jitters slightly step to step, even while 
the overall trend goes down.

The + between the two parts is numpy element-wise addition: element 1 of the decay array gets added to element 1 of the noise array, element 2 to element 2, and so on — 
producing one final 50-element loss array. This is your y-axis.
"""
loss = 2.5 * np.exp(-0.08 * epochs) + np.random.normal(0, 0.03, size=50)

fig, ax = plt.subplots()

"""
ax.plot(epochs, loss, color="darkorange", linewidth=2)

This is the core line-drawing method, and it's worth contrasting directly with .scatter() and .hist() since you've now seen all three:

.hist() took one array and did its own binning/counting internally before drawing bars.
.scatter() took x and y arrays and drew independent, unconnected dots at each (x, y) pair.
.plot() also takes x and y arrays — here, epochs (x) and loss (y) — but instead of drawing isolated points, it draws straight line segments connecting each consecutive point 
to the next: (epoch 1, loss 1) connects to (epoch 2, loss 2), which connects to (epoch 3, loss 3), and so on through all 50 points. With 50 points close together, 
these tiny connected segments visually read as one smooth continuous curve.

Internally, .plot() creates a single artist of type Line2D and attaches it to ax — one object representing the entire connected line, analogous to how .scatter() 
created one PathCollection per call and .hist() created a BarContainer of Rectangles.

color="darkorange" sets the line's color — same styling concept as color in .hist(), just applied to a line instead of bar fills.
linewidth=2 controls how thick the line is drawn, in points. Default is usually 1.5; bumping it to 2 makes the curve a bit bolder/easier to see. You could go thinner (e.g., 0.5) 
for a subtle line or thicker (e.g., 4) to make it stand out more.
"""
ax.plot(epochs, loss, color="darkorange", linewidth=2)
ax.set_xlabel("Epoch")
ax.set_ylabel("Loss")
ax.set_title("Training Loss Curve")
plt.show()