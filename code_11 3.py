# First DataFrame
geochem_data = {
    'WellID': [101, 102, 103],
    'Nitrate_mg_L': [3.5, 12.0, 2.0],
    'Arsenic_mg_L': [0.01, 0.03, 0.005]
}
df_geochem = pd.DataFrame(geochem_data)

# Second DataFrame
location_data = {
    'WellID': [101, 102, 104],
    'Latitude': [48.5, 48.7, 48.6],
    'Longitude': [9.0, 9.1, 9.05]
}
df_loc = pd.DataFrame(location_data)

# Merge on the 'WellID' column using an outer join
merged_df = pd.merge(df_geochem, df_loc, on='WellID', how='outer')
print("Merged DataFrame:\n", merged_df)
