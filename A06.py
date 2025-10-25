# Assignment 06 - Task 3

import pandas as pd

# (a) Load the dataset and compute the mean expression of each protein for the control and treatment groups
# seperately. Which two proteins show the largest difference in average expression between the groups? (2P)

df = pd.read_csv('proteomics_data.csv')

print('proteomics_data.csv:')
print(df.head())
print()

# select columns with protein information
protein_columns = [column for column in df.columns if column.startswith('protein')]

# calculate groupwise means
df_means = df.groupby('group')[protein_columns].mean()
print('Mean expression values per group:')
print(df_means)
print()

# calculate mean differences between control and treatment
mean_difference = (df_means.loc['control'] - df_means.loc['treatment']).abs()
print('Mean difference between treatment and control group')
print(mean_difference.sort_values(ascending=False))
print()

# (b) Subtract the column-wise mean from each protein expression column (i.e. mean-center the data). Then,
# for each protein, calculate the variance of the centered values. (3P)

# mean center the data
df_mean_centered = df[protein_columns] - df[protein_columns].mean()
print('Mean centered expression values:')
print(df_mean_centered)
print()

# print variance of centered values
print('Variance of expression values:')
print(df_mean_centered.var())
print()

# (c) Which protein has the highest variance and what might this imply about its role in distinguishing samples
# in a PCA? (2P)
# protein with highest expression value
print(df[protein_columns].var().sort_values(ascending=False).head(1))

# (d) Compute the False Discovery Rate (FDR) using the formula: FDR = #decoy/#target .
num_target = (df['match type'] == 'target').sum()
num_decoy = (df['match type'] == 'decoy').sum()

fdr = num_decoy / num_target
print(f'FDR = {num_decoy} / {num_target} = {fdr}')

# (e) What is one limitation of using this basic FDR formula without further corrections or assumptions, es-
# pecially in the context of complex biological data? (1P))