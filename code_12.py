data = {
'Region': ['North', 'South', 'North', 'East', 'East'],
'WellID': [101, 102, 103, 104, 105],
'Nitrate_mg_L': [3.5, 12.0, 2.0, 1.5, 10.0]
}
df = pd.DataFrame(data)
# Group by 'Region' and compute mean nitrate
grouped = df.groupby('Region')['Nitrate_mg_L'].mean()
print("Mean nitrate by region:\n", grouped)
# Multiple aggregations
agg_df = df.groupby('Region')['Nitrate_mg_L'].agg(['mean', 'max', 'min','std'])
print("\nMultiple aggregations for nitrate:\n", agg_df)
