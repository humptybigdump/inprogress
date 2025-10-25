# Compute five-number summary
min_value = df["Magnitude"].min()
q1_value = df["Magnitude"].quantile(0.25)
median_value = df["Magnitude"].median()
q3_value = df["Magnitude"].quantile(0.75)
max_value = df["Magnitude"].max()
