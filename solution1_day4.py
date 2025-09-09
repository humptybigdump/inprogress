import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine

# Load dataset and convert to DataFrame
data: pd.DataFrame = load_wine()
df: pd.DataFrame = pd.DataFrame(data.data, columns=data.feature_names)

# Compute statistical measures
summary_stats = df.describe().T
summary_stats["range"] = df.max() - df.min()
summary_stats["variance"] = df.var()
summary_stats["std_dev"] = df.std()
summary_stats["IQR"] = df.quantile(0.75) - df.quantile(0.25)
summary_stats["skewness"] = df.skew()
summary_stats["kurtosis"] = df.kurt()

# Five-number summary
five_number_summary = pd.DataFrame({
    "Min": df.min(),
    "Q1": df.quantile(0.25),
    "Median": df.median(),
    "Q3": df.quantile(0.75),
    "Max": df.max()
})

# Histogram with Mean & Median
plt.figure(figsize=(8, 5))
sns.histplot(df["alcohol"], bins=15, kde=True, color="royalblue", alpha=0.8)
plt.axvline(df["alcohol"].mean(), color='red', linestyle='dashed', linewidth=2, label="Mean")
plt.axvline(df["alcohol"].median(), color='green', linestyle='dashed', linewidth=2, label="Median")
plt.title("Distribution of Alcohol Content", fontsize=14)
plt.xlabel("Alcohol Content")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Boxplot
plt.figure(figsize=(6, 5))
sns.boxplot(y=df["alcohol"], color="darkorange", width=0.5, linewidth=2.5, flierprops={"marker": "o", "markersize": 7})
plt.title("Boxplot of Alcohol Feature", fontsize=14)
plt.ylabel("Alcohol Content")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Violin Plots for Last Five Features
last_five = df.iloc[:, -5:]
fig, axes = plt.subplots(1, 5, figsize=(20, 6))
fig.suptitle("Violin Plots of Last Five Features", fontsize=16, fontweight="bold")

for i, feature in enumerate(last_five.columns):
    sns.violinplot(y=last_five[feature], ax=axes[i], inner="box", linewidth=2, legend=False)
    axes[i].set_title(feature, fontsize=12)
    axes[i].set_ylabel("Value")

plt.tight_layout()
plt.show()

# Correlation Heatmap
plt.figure(figsize=(12, 8))
mask = np.triu(np.ones_like(df.corr(), dtype=bool))  # Mask to show only lower triangle
sns.heatmap(df.corr(), mask=mask, annot=True, cmap="coolwarm", fmt=".1f", linewidths=0.5, cbar_kws={"shrink": 0.8}, square=True)
plt.title("Feature Correlation Heatmap", fontsize=16, fontweight="bold")
plt.show()

# Pairplot for First Five Features
sns.pairplot(df.iloc[:, :5], diag_kind="kde", plot_kws={'alpha':0.7, 's':50}, diag_kws={'fill':True}, corner=True)
plt.show()

