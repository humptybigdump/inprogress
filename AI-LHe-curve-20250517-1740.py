import matplotlib.pyplot as plt
import numpy as np

# Data for the lambda transition of helium
T_lambda = np.array([1.4, 1.6, 1.8, 2.0, 2.1, 2.176, 2.18, 2.15, 2.1, 2.0, 1.9, 1.8, 1.7, 1.6, 1.5])  # Temperature in Kelvin
P_lambda = np.array([0.006, 0.017, 0.031, 0.050, 0.082, 0.160, 0.50, 1.00, 1.50, 2.00, 2.50, 2.90, 3.30, 3.65, 3.95])  # Pressure in MPa

# Data for the vaporization curve of helium-4
T_vapor = np.array([2.176, 2.5, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2])
P_vapor = np.array([0.00519, 0.0098, 0.0178, 0.0274, 0.0398, 0.0556, 0.0758, 0.101, 0.132, 0.170, 0.216, 0.270, 0.334, 0.408, 0.492])

# Data for the melting curve of helium-4
T_melt = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
P_melt = np.array([2.5, 3.0, 3.5, 4.0, 4.6, 5.2, 5.8, 6.4, 7.0])

# Plotting the lambda transition
plt.plot(T_lambda, P_lambda, marker='o', label='Lambda Transition (He-4)')

# Plotting the vaporization curve
plt.plot(T_vapor, P_vapor, marker='s', label='Vaporization Curve (He-4)')

# Plotting the melting curve
plt.plot(T_melt, P_melt, marker='^', label='Melting Curve (He-4)')

# Adding labels and title
plt.xlabel('Temperature (K)')
plt.ylabel('Pressure (MPa)')
plt.title('Pressure-Temperature Diagram of Helium-4')
plt.legend()

# Annotating the superfluid phases
plt.annotate('He-II (Superfluid)', xy=(1.8, 0.1), xytext=(1.5, 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('He-I (Normal Fluid)', xy=(2.1, 0.2), xytext=(2.3, 0.8),
             arrowprops=dict(facecolor='black', shrink=0.05))

# Displaying the plot
plt.grid(True)
plt.show()
