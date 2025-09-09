import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

# Generate Data
X = np.linspace(1, 10, 100)
Y_monotonic = (X**7 + (2*X))/1000  # Monotonic but non-linear
Y_non_monotonic = np.sin(X)  # Non-monotonic

# Compute Correlations
pearson_mono, _ = pearsonr(X, Y_monotonic)
spearman_mono, _ = spearmanr(X, Y_monotonic)

pearson_nonmono, _ = pearsonr(X, Y_non_monotonic)
spearman_nonmono, _ = spearmanr(X, Y_non_monotonic)

# Plot
sns.set(style="whitegrid", context="talk")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Monotonic Plot
sns.scatterplot(x=X, y=Y_monotonic, ax=axes[0], color='dodgerblue', label="Data")
sns.lineplot(x=X, y=Y_monotonic, ax=axes[0], color='navy', alpha=0.7, label="Trend")
axes[0].set_title("Monotonic Relationship: $Y = \\frac{(X^7 + {2X})}{1000}$", fontsize=14)
axes[0].set_xlabel("X")
axes[0].set_ylabel("Y")
axes[0].text(2, Y_monotonic.max() * 0.5, f"Pearson: {pearson_mono:.2f}\nSpearman: {spearman_mono:.2f}", 
             fontsize=12, bbox=dict(facecolor='white', alpha=0.7))

# Non-Monotonic Plot
sns.scatterplot(x=X, y=Y_non_monotonic, ax=axes[1], color='darkorange', label="Data")
sns.lineplot(x=X, y=Y_non_monotonic, ax=axes[1], color='red', alpha=0.7, label="Trend")
axes[1].set_title("Non-Monotonic Relationship: $Y = \sin(X)$", fontsize=14)
axes[1].set_xlabel("X")
axes[1].set_ylabel("Y")
axes[1].text(2, 0.5, f"Pearson: {pearson_nonmono:.2f}\nSpearman: {spearman_nonmono:.2f}", 
             fontsize=12, bbox=dict(facecolor='white', alpha=0.7))

# Show the plot
plt.tight_layout()
plt.savefig("corr.pdf", dpi=600, bbox_inches='tight')

plt.show()
