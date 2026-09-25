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

epochs = np.arange(1, 51)                      # steps 1 through 50
loss = 2.5 * np.exp(-0.08 * epochs) + np.random.normal(0, 0.03, size=50)

fig, ax = plt.subplots()
ax.plot(epochs, loss, color="darkorange", linewidth=2)
ax.set_xlabel("Epoch")
ax.set_ylabel("Loss")
ax.set_title("Training Loss Curve")
plt.show()