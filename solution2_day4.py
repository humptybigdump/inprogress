import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score


def generate_data(n, mean_error,std_error):
    np.random.seed(42)
    X = np.linspace(-10, 10, n)
    # Ground truth line: y = 3x + 8
    true_slope = 2
    true_intercept = 8
    y = true_slope * X + true_intercept + np.random.normal(mean_error, std_error, size=n)  # Add noise
    return X, y

X, y = generate_data(n=500, mean_error=0, std_error=1)
plt.scatter(X, y, color='blue', label='Data Points')
plt.title("Generated Data (Univariate)")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.legend()
plt.show()

# Reshape X for matrix operations
X_matrix = np.vstack((np.ones(len(X)), X)).T  # Adding intercept term

# OLS Analytical Solution (Normal Equation)
theta_ols = np.linalg.inv(X_matrix.T @ X_matrix) @ X_matrix.T @ y
b_ols, m_ols = theta_ols  # Extract intercept and slope
print(f"OLS Analytical Solution: m = {m_ols:.2f}, b = {b_ols:.2f}")

# Scatter plot and Regression Lines
plt.figure(figsize=(8, 5))
plt.scatter(X, y, s=5, color='gray', alpha=0.5, label='Data Points')
plt.scatter(X, m_ols * X + b_ols, color='red', marker=',', s=8,alpha=0.2, label='OLS Analytical Solution') 
plt.show()
y_pred=m_ols * X + b_ols
residual=(y-y_pred)

# Compute  MSE, RMSE
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y, y_pred)
# Compute NRMSE (using normalization)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y, y_pred)
# Compute NRMSE (using normalization)
nrmse = rmse / (max(y)-min(y))
# Compute RPD (standard deviation of observed values)
rpd = np.std(y, ddof=1) / rmse
print("MSE:", mse);print("RMSE:", rmse);print("R^2:", r2);print("NRMSE:", nrmse);print("RPD:", rpd)

