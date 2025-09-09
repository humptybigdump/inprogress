import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
# Set Seaborn style
sns.set_theme(style="whitegrid")
# Generate data
X = np.linspace(-5, 5, 200)  # Increased resolution for smoothness
Y = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
# Create figure with increased width
fig = plt.figure(figsize=(16, 7))
# ---- Surface Plot ----
ax1 = fig.add_subplot(121, projection='3d')
surface = ax1.plot_surface(X, Y, Z, cmap='magma', edgecolor='k', linewidth=0.3, alpha=0.9)
# Enhancing visibility with clean labels and grid
ax1.set_xlabel('X-axis', fontsize=13, labelpad=12, fontweight='bold')
ax1.set_ylabel('Y-axis', fontsize=13, labelpad=12, fontweight='bold')
ax1.set_zlabel('Z-axis', fontsize=13, labelpad=8, fontweight='bold')
ax1.set_title('3D Surface Plot', fontsize=15, fontweight='bold', pad=15)
# Add color bar with a clear label
cbar1 = fig.colorbar(surface, ax=ax1, shrink=0.7, aspect=15, pad=0.1)
cbar1.set_label('Function Value', fontsize=12, fontweight='bold')
# ---- Contour Plot ----
ax2 = fig.add_subplot(122)
contour = ax2.contourf(X, Y, Z, levels=40, cmap='magma')  # Increased contour levels for smoothness
ax2.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5, alpha=0.6)  # Overlay contour lines
# Enhancing visibility with Seaborn-style grid
ax2.set_xlabel('X-axis', fontsize=13, fontweight='bold')
ax2.set_ylabel('Y-axis', fontsize=13, fontweight='bold')
ax2.set_title('Contour Plot', fontsize=15, fontweight='bold', pad=12)
ax2.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
# Add color bar with a clear label
cbar2 = fig.colorbar(contour, ax=ax2, shrink=0.7, aspect=15)
cbar2.set_label('Function Value', fontsize=12, fontweight='bold')
# Optimize layout
plt.tight_layout()
plt.show()
