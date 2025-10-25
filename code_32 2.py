import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create figure
plt.figure(figsize=(8, 5))
plt.plot(x, y, label="Sine Wave", color="blue", linewidth=2)
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Sine Wave Example")
plt.legend()

# Save the figure
plt.savefig("sine_wave.png", dpi=300, bbox_inches="tight")

# Show the figure
plt.show()
