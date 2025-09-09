import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, pearsonr, spearmanr

# ----------------------------------------------
# 1. Load and Preprocess Data
# ----------------------------------------------
# Read dataset from CSV file
df = pd.read_csv("all_data_multiple.csv").iloc[1:, :]  # Exclude first row

# Convert 'Timestamp' column to datetime and handle missing values
df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
df.iloc[:, 2:] = df.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')
df.dropna(inplace=True)

# Set 'Timestamp' as index for time series analysis
df.set_index("Timestamp", inplace=True)

df = df.convert_dtypes()

# ----------------------------------------------
# 2. Compute Basic Statistics for Air Temperature
# ----------------------------------------------
# Extract Air Temperature column
air_temp = df["Air temperature"]

# Compute statistical measures
statistics = {
    "Mean": air_temp.mean(),
    "Median": air_temp.median(),
    "Variance": air_temp.var(),
    "Standard Deviation": air_temp.std(),
    "Skewness": air_temp.skew(),
    "Kurtosis": air_temp.kurtosis()
}

# Display statistics
print("\nBasic Statistics for Air Temperature:")
for key, value in statistics.items():
    print(f"{key}: {value:.4f}")

# ----------------------------------------------
# 3. Check Normality of Precipitation Data (First Year)
# ----------------------------------------------
# Extract first year's precipitation data
first_year = df[df.index.year == df.index.year.min()]["Precipitation"]

# Perform Shapiro-Wilk Test for normality
stat, p_value = shapiro(first_year)

# Display results
print("\nShapiro-Wilk Test for First Year Precipitation:")
print(f"Statistic: {stat:.4f}, p-value: {p_value:.4f}")

# Interpretation
if p_value > 0.05:
    print("The data is likely normal (fail to reject H_null).")
else:
    print("The data is NOT normally distributed (reject H_null).")

# ----------------------------------------------
# 4. Correlation Analysis for the Entire Time Series
# ----------------------------------------------
# Compute Pearson and Spearman correlations
pearson_corr, _ = pearsonr(df["Air temperature"], df["Solar radiation"])
spearman_corr, _ = spearmanr(df["Air temperature"], df["Solar radiation"])

# Display correlation results
print("\nCorrelation Analysis:")
print(f"Pearson Correlation: {pearson_corr:.4f}")
print(f"Spearman Correlation: {spearman_corr:.4f}")

# ----------------------------------------------
# Visualize Correlation Using Heatmap
# ----------------------------------------------
# Compute Spearman correlation matrix for all numerical features
correlation_matrix = df.iloc[:, 1:].corr(method="spearman")

# Plot correlation heatmap
plt.figure(figsize=(10, 6))
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))  # Mask to show only lower triangle
sns.heatmap(correlation_matrix,mask=mask, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()



