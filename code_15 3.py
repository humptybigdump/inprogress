data = {
    'WellID': [101, 102, 102, 103],
    'Region': ['North', 'South', 'South', 'North'],
    'Nitrate_mg_L': [3.5, 12.0, 12.0, 2.0]
}
df = pd.DataFrame(data)

print("Original DataFrame:\n", df)

# Check which rows are duplicates (all columns)
duplicates = df.duplicated()
print("\nDuplicate rows:\n", duplicates)

# Remove duplicates
df_no_duplicates = df.drop_duplicates()
print("\nDataFrame with duplicates removed:\n", df_no_duplicates)
