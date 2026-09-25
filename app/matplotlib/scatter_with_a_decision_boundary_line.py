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

np.random.seed(1)
x1 = np.random.normal(5, 2, 50)
x2 = np.random.normal(5, 2, 50)

# Made-up decision boundary: x2 = slope * x1 + intercept
slope, intercept = -1.0, 10

fig, ax = plt.subplots()
ax.scatter(x1, x2, color="purple", alpha=0.6, label="Data points")

x_line = np.linspace(x1.min(), x1.max(), 100)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, color="black", linestyle="--", linewidth=2, label="Decision boundary")

ax.set_xlabel("Feature 1")
ax.set_ylabel("Feature 2")
ax.set_title("Scatter Plot with Decision Boundary")
ax.legend()
plt.show()