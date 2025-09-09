import seaborn as sns
import matplotlib.pyplot as plt

def generate_data(n_samples=100, seed=42):
    """Generates synthetic dataset with linear and nonlinear relationships."""
    np.random.seed(seed)
    
    X1 = np.random.rand(n_samples) * 10  # Random values
    X2 = 2 * X1 + np.random.randn(n_samples) * 2  # Linear relationship
    X3 = np.log(X1 + 1) + np.random.randn(n_samples) * 0.1  # Monotonic but nonlinear
    
    return pd.DataFrame({'X1': X1, 'X2': X2, 'X3': X3})

def plot_correlation_heatmap(df, method, title):
    """Plots a correlation heatmap for a given correlation method."""
    corr_matrix = df.corr(method=method)
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title(title, fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()

def plot_scatter_matrix(df):
    """Plots scatter plots for each pair of features."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    sns.scatterplot(x=df['X1'], y=df['X2'], ax=axes[0], color="royalblue")
    axes[0].set_title("X1 vs X2 (Linear Relationship)")
    
    sns.scatterplot(x=df['X1'], y=df['X3'], ax=axes[1], color="darkorange")
    axes[1].set_title("X1 vs X3 (Nonlinear Monotonic)")

    sns.scatterplot(x=df['X2'], y=df['X3'], ax=axes[2], color="green")
    axes[2].set_title("X2 vs X3 (Indirect Relationship)")

    for ax in axes:
        ax.set_xlabel("Feature 1")
        ax.set_ylabel("Feature 2")

    plt.tight_layout()
    plt.show()

# Generate dataset
df = generate_data()

# Compute and visualize correlations
plot_correlation_heatmap(df, method='pearson', title="Pearson Correlation Heatmap")
plot_correlation_heatmap(df, method='spearman', title="Spearman Correlation Heatmap")

# Scatter plot matrix for feature relationships
plot_scatter_matrix(df)
