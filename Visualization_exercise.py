# General packages
import pandas as pd
from pathlib import Path

# Data handling
import xarray as xr

#Visualization
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import cartopy.crs as ccrs
import cartopy.feature as cfeature



# Sample dataset of cities with seasonal temperatures
data = {
    'City': ['New York', 'Los Angeles', 'London', 'Paris', 'Tokyo', 'Sydney', 'Cape Town'],
    'Latitude': [40.71, 34.05, 51.51, 48.85, 35.68, -33.87, -33.92],
    'Longitude': [-74.01, -118.24, -0.13, 2.35, 139.65, 151.21, 18.42],
    'Winter (°C)': [2, 15, 5, 4, 6, 25, 18],
    'Spring (°C)': [10, 18, 12, 14, 15, 22, 16],
    'Summer (°C)': [25, 22, 20, 24, 28, 17, 14],
    'Fall (°C)': [15, 20, 12, 16, 19, 21, 18]
}
df = pd.DataFrame(data)

# Task1: Create violin plot
plt.figure(figsize=(10, 6))
sns.violinplot(data=df[['Winter (°C)', 'Spring (°C)', 'Summer (°C)', 'Fall (°C)']])
plt.title('Temperature Distribution for Each Season')
plt.show()

# Task 2: Interactive bar plot of seasonal temperatures per city
fig = px.bar(df, x='City', y=['Winter (°C)', 'Spring (°C)', 'Summer (°C)', 'Fall (°C)'],
             title='Average Seasonal Temperatures Across Cities',
             labels={'value': 'Temperature (°C)', 'variable': 'Season'},
             barmode='stack')
fig.show()

# Task 3: Interactive temperature map with Plotly
fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', text='City',
                     size_max=15, projection='natural earth',
                     color='Summer (°C)',
                     title='Global Temperature Map (Summer)')
fig.update_layout(geo=dict(showland=True))
fig.show()

#Task 4: Visualize Organic content in EU based on global data
# -----------------------------------------
# Load NetCDF Data
# -----------------------------------------
# Get the path of the script file, regardless of where it's run from
script_path = Path(__file__).resolve()
script_dir = script_path.parent
file_path = script_dir / "T_OC.nc4"
print(file_path)
ds = xr.open_dataset(file_path)

# Extract variable and coordinates
var = ds.T_OC.values  # 2D variable array
lat = ds.lat.values     # 1D Latitude array
lon = ds.lon.values     # 1D Longitude array


# -----------------------------------------
# Define the extent over Europe
# -----------------------------------------
lon_min, lon_max = lon.min(), lon.max()   # Use actual dataset range
lat_min, lat_max = lat.min(), lat.max()
extent = [lon.min(), lon.max(), lat.min(), lat.max()]

origin = "lower"

# -----------------------------------------
# Create the plot using Cartopy
# -----------------------------------------
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

# Set extent to focus on Europe
ax.set_extent([-10, 40, 35, 70])  # Restrict to Europe

# Add geographic features
ax.coastlines(resolution='110m', linewidth=0.5, color='#13315c')
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.8, edgecolor='black')
ax.add_feature(cfeature.LAND, facecolor='#fefae0', alpha=0.4)
ax.add_feature(cfeature.OCEAN, facecolor='lightblue', alpha=0.9)

# -----------------------------------------
# Plot the data using imshow
# -----------------------------------------
im = ax.imshow(var, cmap='Reds', origin=origin, extent=extent,
               interpolation='none', transform=ccrs.PlateCarree())

# Add a colorbar
# -----------------------------------------
cbar = plt.colorbar(im, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
cbar.set_label('Organic Content [%]', fontsize=16, fontweight='bold', color='black')
cbar.ax.tick_params(labelsize=12)

# Title
plt.title("Organic Content", fontsize=18, fontweight='bold')

plt.show()