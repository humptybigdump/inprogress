import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score



# Load the dataset
data = pd.read_excel("model_complexity.xlsx")

# Take 10% random sample
data10 = data.sample(frac=0.1, random_state=0)  # Ensures reproducibility
X = data10['X'].values  # Feature values
y = data10['y'].values  # Observed values

# Define polynomial degrees
degrees = [1, 3, 10]  # Underfitting, Good Fit, Overfitting
titles = ["Underfitting (Degree 1)", "Good Fit (Degree 3)", "Overfitting (Degree 10)"]

# Create smooth X range for plotting
X_fit = np.linspace(-3, 3, 100)  # Smooth range for predictions

plt.figure(figsize=(18, 5))
true_function = lambda x: 2*x**3 - 3*x**2 + x  # True cubic function
true_y_fit = true_function(X_fit)  # True function values

for i, degree in enumerate(degrees):
    coeffs = np.polyfit(X, y, degree)  # Fit polynomial
    y_pred = np.polyval(coeffs, X_fit)  # Predict on smooth range

    # Plot results
    plt.subplot(1, 3, i + 1)
    plt.scatter(X, y, color='black', label="Noisy Data", alpha=0.6)  # Observed data
    plt.plot(X_fit, true_y_fit, color='blue', linestyle="dashed", linewidth=2, label="True Function")  # True function
    plt.plot(X_fit, y_pred, color='red', linewidth=2, label=f"Model Degree {degree}")  # Model prediction
    plt.title(titles[i])
    plt.xlabel("X")
    plt.ylabel("y")
    plt.legend()

plt.show()

