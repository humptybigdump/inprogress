import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares, approx_fprime

# Define the Michaelis-Menten function
# ------------------------------------
# This function models enzyme kinetics, describing how the reaction rate (v) 
# depends on the substrate concentration (S). It follows the Michaelis-Menten equation:
#
#        v = (Vmax * S) / (Km + S)
#
# where:
# - v    = Reaction velocity (rate at which product is formed)
# - S    = Substrate concentration (amount of available reactant)
# - Vmax = Maximum reaction velocity (when all enzyme active sites are occupied)
# - Km   = Michaelis constant (substrate concentration at half of Vmax, 
#          representing enzyme affinity for the substrate)
#
# This equation is widely used in biochemistry, pharmacology, and biotechnology 
# for modeling enzyme behavior, drug interactions, and metabolic pathways.
def michaelis_menten(S, Vmax, Km):
    return (Vmax * S) / (Km + S)

# Generate synthetic experimental data
np.random.seed(42)
S_data = np.linspace(0.1, 10, 200)  # Substrate concentrations
Vmax_true, Km_true = 2.5, 1.5       # True parameters
V_data = michaelis_menten(S_data, Vmax_true, Km_true) + np.random.normal(0, 0.1, size=len(S_data))  # Add noise

# Define residual function (unchanged)
def residuals(theta, S, V):
    Vmax, Km = theta
    return V - michaelis_menten(S, Vmax, Km)

# Compute the Jacobian matrix of residuals
# Corrected Jacobian function with 3 parameters
# def jacobian(theta, S, _):  # Added third parameter "_" to absorb unused V
#     Vmax, Km = theta
#     J = np.zeros((len(S), 2))
#     J[:, 0] = -S / (Km + S)           # Partial derivative w.r.t Vmax
#     J[:, 1] = (Vmax * S) / (Km + S)2  # Partial derivative w.r.t Km
#     return J

# Compute the Jacobian matrix using automatic differentiation
def compute_jacobian(theta, S, V, epsilon=1e-6):
    return approx_fprime(theta, lambda p: residuals(p, S, V), epsilon)

# Gauss-Newton Iterative Solver (unchanged)
def gauss_newton(S, V, theta_init, max_iter=500, tol=1e-6):
    theta = np.array(theta_init, dtype=float)
    loss_old = np.sum(residuals(theta, S, V)  2)  # Initial loss function (Sum of Squared Residuals)

    for iteration in range(max_iter):
        r = residuals(theta, S, V)
        J = compute_jacobian(theta, S, V)  # Compute Jacobian using approx_derivative

        # J = jacobian(theta, S, V)  # Pass V even though Jacobian doesn't use it
        new_theta = theta-np.linalg.inv(J.T @ J) @ (J.T @ r)
        theta = new_theta
        # Compute new loss function
        loss_new = np.sum(residuals(theta, S, V)  2)

        # Convergence check based on loss improvement
        if np.abs(loss_new - loss_old) < tol:
            print(f"Converged at iteration {iteration}, Loss Improvement: {np.abs(loss_new - loss_old):.6e}")
            break

        # Update loss for next iteration
        loss_old = loss_new
    return theta

# Initial Guess
theta_init = [1.0, 1.0]  # Initial guess for Vmax and Km

# Apply Manual Gauss-Newton Method
Vmax_GN, Km_GN = gauss_newton(S_data, V_data, theta_init)

# Apply SciPy's least_squares Method
# result = least_squares(residuals, theta_init, args=(S_data, V_data), jac=jacobian)
result = least_squares(residuals, theta_init, args=(S_data, V_data), jac=compute_jacobian)
Vmax_scipy, Km_scipy = result.x

# Print Results
print(f"True Parameters:          Vmax = {Vmax_true:.2f}, Km = {Km_true:.2f}")
print(f"Gauss-Newton Fit:         Vmax = {Vmax_GN:.2f}, Km = {Km_GN:.2f}")
print(f"SciPy least_squares Fit:  Vmax = {Vmax_scipy:.2f}, Km = {Km_scipy:.2f}")

# Generate fitted curves
S_fit = np.linspace(0.1, 10, 100)
V_fit_GN = michaelis_menten(S_fit, Vmax_GN, Km_GN)
V_fit_scipy = michaelis_menten(S_fit, Vmax_scipy, Km_scipy)

# Plot Results
plt.figure(figsize=(8, 5))
plt.scatter(S_data, V_data, color='gray', label="Experimental Data")
plt.plot(S_fit, V_fit_GN, 'r-', label="Gauss-Newton Fit (Manual)")
plt.plot(S_fit, V_fit_scipy, 'b--', label="SciPy least_squares Fit")
plt.xlabel("Substrate Concentration [S]", fontsize=12)
plt.ylabel("Reaction Velocity [V]", fontsize=12)
plt.title("Michaelis-Menten Parameter Estimation", fontsize=14)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()
