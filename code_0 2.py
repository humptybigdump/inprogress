# Generate synthetic earthquake magnitude data
np.random.seed(42)
magnitude = np.random.normal(loc=5.0, scale=1.0, size=500)
magnitude = np.clip(magnitude, 3.0, 7.5)  # Magnitudes between 3 and 7.5
region = np.random.choice(['Pacific Rim', 'Himalayan Belt', 'Mid-Atlantic Ridge'], size=500)
# Create DataFrame
df = pd.DataFrame({'Magnitude': magnitude, 'Region': region})
# Compute measures of central tendency
mean_value = df["Magnitude"].mean()
median_value = df["Magnitude"].median()
mode_value = df["Magnitude"].mode()
print(f'Mean: {mean_value:.2f}, Median: {median_value:.2f}, Mode: {mode_value[0]:.2f}')
