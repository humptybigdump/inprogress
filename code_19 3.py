import seaborn as sns
import matplotlib.pyplot as plt
# Generate synthetic geoscience data with direct correlation
np.random.seed(42)
n = 300
# Generate base features
pH = np.random.normal(7, 0.5, n)  # pH varies randomly
nitrate = np.random.normal(30, 5, n)  # Independent nitrate concentrations
# Generate sulfate and EC with direct correlation
sulfate = np.random.normal(50, 10, n)  # Base sulfate concentration
electrical_conductivity = sulfate * 0.5 + np.random.normal(0, 3, n)  # EC strongly correlated with sulfate
data = pd.DataFrame({
    'pH': pH,
    'Nitrate (mg/L)': nitrate,
    'Sulfate (mg/L)': sulfate,
    'Electrical Conductivity (µS/cm)': electrical_conductivity
})
# Calculate the correlation matrix
corr_matrix = data.corr()
# Plot the heatmap with fancier design
plt.figure(figsize=(9, 7))
sns.set_theme(style='white', context='talk')
ax = sns.heatmap(corr_matrix, annot=True, cmap='crest', linewidths=2, linecolor='white', 
                 fmt='.2f', vmin=-1, vmax=1, cbar_kws={'shrink': 0.85, 'aspect': 30, 'label': 'Correlation Coefficient'})
# Add title with fancy font
plt.title('Groundwater Parameter Correlation Matrix', fontsize=18, fontweight='bold', color='teal')
# Improve axis labels readability
plt.xticks(rotation=45, ha='right', fontsize=12, color='darkslategray')
plt.yticks(fontsize=12, color='darkslategray')
# Display the plot
plt.show()
