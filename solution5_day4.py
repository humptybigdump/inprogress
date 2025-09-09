import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares, approx_fprime

# ----------------------------------------------
# Task 1: Generate Synthetic Sorption Data
# ----------------------------------------------

# Define the Freundlich isotherm function
def freundlich_model(C_eq, Kf, n):
    """Computes the Freundlich isotherm equation: C_s = Kf * C_eq^(1/n)"""
    return Kf * (C_eq**(1/n))

# Generate synthetic sorption data with noise
np.random.seed(42)
C_eq_data = np.linspace(0.1, 1, 10)  # Equilibrium concentrations
true_Kf, true_n = 7, 2  # True parameters
C_s_data = freundlich_model(C_eq_data, true_Kf, true_n) + np.random.normal(0, 1, size=len(C_eq_data))  # Add Gaussian noise

# Plot experimental data
plt.figure(figsize=(8, 5))
plt.scatter(C_eq_data, C_s_data, color='gray', label="Experimental Data")
plt.xlabel("Equilibrium Concentration [C_eq]", fontsize=12)
plt.ylabel("Solid Concentration [C_s]", fontsize=12)
plt.title("Synthetic Freundlich Isotherm Data", fontsize=14)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# ----------------------------------------------
# Task 2: Estimate Parameters Using Gauss-Newton
# ----------------------------------------------

# Define residual function
def residuals(theta, C_eq, C_s):
    """Computes the residuals: difference between observed and predicted values."""
    Kf, n = theta
    return C_s - freundlich_model(C_eq, Kf, n)

# Compute Jacobian matrix using finite differences
def compute_jacobian(theta, C_eq, C_s, epsilon=1e-6):
    """Approximates the Jacobian matrix using finite differences."""
    return approx_fprime(theta, lambda p: residuals(p, C_eq, C_s), epsilon)

# Gauss-Newton Iterative Solver
def gauss_newton(C_eq, C_s, theta_init, max_iter=500, tol=1e-6):
    """
    Implements the Gauss-Newton optimization method:
    theta_(t+1) = theta_t - (J^T J)^(-1) J^T r
    """
    theta = np.array(theta_init, dtype=float)
    loss_old = np.sum(residuals(theta, C_eq, C_s) ** 2)  # Initial loss function

    for iteration in range(max_iter):
        r = residuals(theta, C_eq, C_s)  # Compute residuals
        J = compute_jacobian(theta, C_eq, C_s)  # Compute Jacobian
        
        # Solve normal equations without damping
        new_theta = theta - np.linalg.inv(J.T @ J) @ (J.T @ r)
        theta = new_theta
        
        # Compute new loss function
        loss_new = np.sum(residuals(theta, C_eq, C_s) ** 2)
        
        # Convergence check
        if np.abs(loss_new - loss_old) < tol:
            print(f"Converged at iteration {iteration}, Loss Improvement: {np.abs(loss_new - loss_old):.6e}")
            break

        loss_old = loss_new
    return theta

# Initial Guess
theta_init = [2.0, 0.2]  # Initial guess for Kf and n

# Apply Gauss-Newton Method
Kf_GN, n_GN = gauss_newton(C_eq_data, C_s_data, theta_init)

# ----------------------------------------------
# Task 3: Compare with SciPy’s Nonlinear Least Squares
# ----------------------------------------------

# Apply SciPy's least_squares Method
result = least_squares(residuals, theta_init, args=(C_eq_data, C_s_data), jac=compute_jacobian)
Kf_scipy, n_scipy = result.x

# Print Results
print(f"True Parameters:          Kf = {true_Kf:.2f}, n = {true_n:.2f}")
print(f"Gauss-Newton Fit:         Kf = {Kf_GN:.2f}, n = {n_GN:.2f}")
print(f"SciPy least_squares Fit:  Kf = {Kf_scipy:.2f}, n = {n_scipy:.2f}")

# ----------------------------------------------
# Task 4: Visualize and Interpret Results
# ----------------------------------------------

# Generate fitted curves for visualization
C_eq_fit = np.linspace(0.1, 1, 20)
C_s_fit_GN = freundlich_model(C_eq_fit, Kf_GN, n_GN)
C_s_fit_scipy = freundlich_model(C_eq_fit, Kf_scipy, n_scipy)

# Plot Results
plt.figure(figsize=(8, 5))
plt.scatter(C_eq_data, C_s_data, color='gray', label="Experimental Data")
plt.plot(C_eq_fit, C_s_fit_GN, 'r-', label="Gauss-Newton Fit (Manual)")
plt.plot(C_eq_fit, C_s_fit_scipy, 'b--', label="SciPy least_squares Fit")
plt.xlabel("Equilibrium Concentration [C_eq]", fontsize=12)
plt.ylabel("Solid Concentration [C_s]", fontsize=12)
plt.title("Freundlich Isotherm Parameter Estimation", fontsize=14)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

