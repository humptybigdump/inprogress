import stats
from scipy.stats import shapiro
import numpy as np

# Generate sample data
np.random.seed(42)
data = np.random.normal(0, 1, 100)  # Normally distributed data

# Shapiro-Wilk Test
stat, p = shapiro(data)
print(f"Shapiro-Wilk Test: p-value = {p:.5f}")
###########################################
##Variance Check
# Example data
data = {'group': ['A']*5 + ['B']*5 + ['C']*5,
        'score': [5,7,8,6,9, 15,17,14,18,16, 25,27,29,26,28]}
df = pd.DataFrame(data)

# Extracting numerical groups properly
group_A = df[df['group'] == 'A']['score']
group_B = df[df['group'] == 'B']['score']
group_C = df[df['group'] == 'C']['score']

# Perform Levene’s test
stat, p_levene = stats.levene(group_A, group_B, group_C)

print(f"Levene’s Test: p-value = {p_levene:.5f}")

# Check for equal variance
if p_levene > 0.05:
    print("Variances are equal (p > 0.05), Tukey HSD is appropriate.")
else:
    print("Variances are not equal (p < 0.05), consider Games-Howell test.")
