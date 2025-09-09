# Generate synthetic soil texture data
np.random.seed(42)
sand = np.random.uniform(40, 90, 300)
silt = np.random.uniform(5, 40, 300)
clay = 100 - sand - silt
soil_type = np.where(clay > 30, 'Clayey', np.where(silt > 30, 'Silty', 'Sandy'))

# Create a DataFrame
data = pd.DataFrame({'Sand (%)': sand, 'Silt (%)': silt, 'Clay (%)': clay, 'Soil Type': soil_type})

# Set Seaborn style
sns.set(style="whitegrid")

# Seaborn pairplot to see relationships
pair_plot = sns.pairplot(data, hue='Soil Type', palette='Set2', markers=["o", "s", "D"])

# Customizing the plot
plt.suptitle('Soil Texture Distribution', y=1.02, fontsize=16, fontweight='bold')
plt.tight_layout()

# Adjust the legend position
pair_plot._legend.set_bbox_to_anchor((1.1, 0.5))  # Adjust the legend to the right of the plot


# Save the plot with high resolution and better styling
plt.savefig("seaborn3.pdf", dpi=600, bbox_inches='tight')

# Show the plot
plt.show()
