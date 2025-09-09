import matplotlib.pyplot as plt
import seaborn as sns
# Histogram
plt.figure(figsize=(8,5))
sns.histplot(df["Magnitude"], bins=20, kde=True, color="blue")
# Add vertical lines for mean and median
plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_value:.2f}')
plt.axvline(median_value, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median_value:.2f}')
plt.title("Histogram of Feature")
plt.legend()

plt.show()
# Boxplot
plt.figure(figsize=(6,4))
outliers=np.copy(df["Magnitude"])
outliers[0:10]=outliers[0:10]+10
sns.boxplot(y=outliers, color="orange")
plt.title("Boxplot of Feature")
plt.show()
