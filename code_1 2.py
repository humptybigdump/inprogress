# Compute measures of dispersion
range_value = df["Magnitude"].max() - df["Magnitude"].min()
variance_value = df["Magnitude"].var()
std_dev_value = df["Magnitude"].std()
iqr_value = df["Magnitude"].quantile(0.75) - df["Magnitude"].quantile(0.25)
print(f'Range: {range_value:.2f}, Variance: {variance_value:.2f}, STD: {std_dev_value:.2f}, IQR: {iqr_value:.2f}')
