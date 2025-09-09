import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate synthetic data
np.random.seed(42)
X = np.linspace(0, 10, 200)
Y = 3 * X + 5 + np.random.randn(200)  # Linear relationship with noise

# Reshape X for matrix operations
X_matrix = np.vstack((np.ones(len(X)), X)).T  # Adding intercept term

# OLS Analytical Solution (Normal Equation)
theta_ols = np.linalg.inv(X_matrix.T @ X_matrix) @ X_matrix.T @ Y
b_ols, m_ols = theta_ols  # Extract intercept and slope

# Fit model using Scikit-Learn
model = LinearRegression()
model.fit(X.reshape(-1, 1), Y)

# Fit linear regression using numpy's polyfit
coeffs = np.polyfit(X, Y, 1)  # Slope and intercept

# Print estimated parameters
print(f"OLS Analytical Solution: m = {m_ols:.2f}, b = {b_ols:.2f}")
print(f"Scikit-Learn Estimated Parameters: m = {model.coef_[0]:.2f}, b = {model.intercept_:.2f}")
print(f"Numpy Polyfit Estimated Parameters: m = {coeffs[0]:.2f}, b = {coeffs[1]:.2f}")

# Scatter plot and Regression Lines
plt.figure(figsize=(8, 5))
plt.scatter(X, Y, s=5, color='gray', alpha=0.5, label='Data Points')

plt.scatter(X, m_ols * X + b_ols, color='red', marker=',', s=8,alpha=0.2, label='OLS Analytical Solution')  
plt.scatter(X, model.predict(X.reshape(-1, 1)), color='orange', marker='p', s=6, label='Scikit-Learn Fit')
plt.scatter(X, coeffs[0] * X + coeffs[1], color='blue', marker='*', s=2,alpha=0.4, label='Numpy Polyfit')
plt.xlabel('X', fontsize=12)
plt.ylabel('Y', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
