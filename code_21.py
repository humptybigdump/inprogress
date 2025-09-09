# Set Seaborn theme
sns.set_theme(style="whitegrid")

# Generate a synthetic topographic surface
x = np.linspace(-50, 50, 200)  
y = np.linspace(-50, 50, 200)
X, Y = np.meshgrid(x, y)

# Create elevation data (simulating hills & valleys)
Z = (np.sin(X / 10) * np.cos(Y / 10)) * 50 + np.random.normal(0, 2, X.shape)  # Add random noise for realism

# Create figure
fig = plt.figure(figsize=(14, 7))

# ---- Surface Plot ----
ax = fig.add_subplot(111, projection='3d')
surface = ax.plot_surface(X, Y, Z, cmap='terrain', edgecolor='k', linewidth=0.1, alpha=0.9)

# Labels and formatting
ax.set_xlabel('X Distance (km)', fontsize=12, labelpad=10)
ax.set_ylabel('Y Distance (km)', fontsize=12, labelpad=10)
ax.set_zlabel('Elevation (m)', fontsize=12, labelpad=10)
ax.set_title('3D Topographic Surface Model', fontsize=14, fontweight='bold')

# Adjust viewing angle
ax.view_init(elev=35, azim=140)

# Add color bar
cbar = fig.colorbar(surface, ax=ax, shrink=0.7, aspect=10, pad=0.1)
cbar.set_label('Elevation (m)', fontsize=12, fontweight='bold')

# Optimize layout
plt.tight_layout()
plt.savefig("seaborn6.pdf", dpi=600, bbox_inches='tight')
plt.show()
