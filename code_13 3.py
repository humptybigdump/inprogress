data = {
'WELL ID ': [101.0, 102.0, 103.0],
'NO3(mg/L)': [3.5, 12.0, 2.0],
' Region ': ['North', 'South', 'North'],
}
df = pd.DataFrame(data)
# Strip whitespace and rename columns
df.rename(columns={
'WELL ID ': 'WellID',
' Region ': 'Region',
'NO3(mg/L)': 'Nitrate_mg_L'
}, inplace=True)
print("Renamed DataFrame:\n", df)
# Convert columns to desired types if necessary
df['WellID'] = df['WellID'].astype(int)
print("Converted WellID:\n", df)
# Replace values if necessary (example: replace 'North' with 'N')
df.replace({'Region': {'North': 'N', 'South': 'S'}}, inplace=True)
print("Region name:\n", df)
# Drop row with index 1 (second row)
df.drop(index=1, inplace=True)
print("Droped First row:\n", df)
# Reset index after dropping the row
df.reset_index(drop=True, inplace=True)
print("Reseted index:\n", df)
