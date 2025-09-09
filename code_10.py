# Sample dataset
data = {
    'WellID': [101, 102, 103, 104, 105],
    'Depth_m': [50, 75, 80, 60, 55],
    'pH': [7.2, 6.5, 8.0, 7.1, 7.5],
    'Nitrate_mg_L': [3.5, 12.0, 2.0, 1.5, 10.0]
}

df = pd.DataFrame(data)

# Filter rows where Nitrate is above 5 mg/L
high_nitrate = df[df['Nitrate_mg_L'] > 5]
print("High nitrate samples:\n", high_nitrate)

# Combine multiple conditions (e.g., Depth > 60 and pH < 7.3)
filtered = df[(df['Depth_m'] > 60) & (df['pH'] < 7.3)]
print("Filtered by depth and pH:\n", filtered)
