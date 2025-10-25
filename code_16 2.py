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

# Seaborn plot
plt.figure(figsize=(10, 6))
sns.histplot(data, x='Magnitude', hue='Region', element='step', kde=True, palette='coolwarm')
plt.title('Earthquake Magnitude Distribution Across Different Seismic Regions')
plt.xlabel('Magnitude (Richter scale)')
plt.ylabel('Frequency')
plt.show()

