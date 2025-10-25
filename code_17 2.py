import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Generate synthetic earthquake magnitude data
np.random.seed(42)
magnitude = np.random.normal(loc=5.0, scale=1.0, size=500)
magnitude = np.clip(magnitude, 3.0, 7.5)  # Magnitudes between 3 and 7.5
region = np.random.choice(['Pacific Rim', 'Himalayan Belt', 'Mid-Atlantic Ridge'], size=500)

# Create DataFrame
data = pd.DataFrame({'Magnitude': magnitude, 'Region': region})

# Set Seaborn style and context
sns.set_style('whitegrid')
sns.set_context('talk')

# Create a violin plot with an embedded boxplot
plt.figure(figsize=(10, 6))
sns.violinplot(x='Region', y='Magnitude', data=data, palette='coolwarm', inner='box')

# Customize the plot aesthetics
plt.title('Earthquake Magnitude Distribution Across Seismic Regions', fontsize=18, fontweight='bold', color='darkred')
plt.xlabel('Seismic Region', fontsize=12)
plt.ylabel('Magnitude (Richter Scale)', fontsize=12)
plt.xticks(rotation=15)

# Add gridlines and clean layout
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
