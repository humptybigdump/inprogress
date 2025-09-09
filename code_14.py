data = {
    'WellID': [101, 102, 103, 104],
    'Nitrate_mg_L': [3.5, np.nan, 2.0, None],
    'Arsenic_mg_L': [0.01, 0.03, np.nan, 0.005]
}
df = pd.DataFrame(data)

# Check for missing values
print("Missing data:\n", df.isna())

# Drop rows with any missing value
df_dropped = df.dropna()
print("\nData after dropping rows with missing values:\n", df_dropped)

# Fill missing values with a constant or a method
df_filled = df.fillna({'Nitrate_mg_L': 0.0,\
'Arsenic_mg_L': df['Arsenic_mg_L'].mean()})
print("\nData after filling missing values:\n", df_filled)
