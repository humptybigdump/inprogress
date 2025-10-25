import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
# Load the NetCDF file
import xarray as xr

file_path = 'S_SAND.nc4'  # Replace with your NetCDF file path
ds = xr.open_dataset(file_path)

# -----------------------------------------
# Extract your data from the xarray dataset
# -----------------------------------------
var = ds.S_SAND.values    # Your variable data (assumed to be 2D)
lat = ds.lat.values       # 1D latitude array
lon = ds.lon.values       # 1D longitude array

# -----------------------------------------
# Create a global map using Cartopy
# -----------------------------------------
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())

# Set the view to display the entire globe
ax.set_global()

# Add geographic features
ax.coastlines(resolution='110m', linewidth=0.5, color='#13315c')
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.8, edgecolor='black')
ax.add_feature(cfeature.LAND, facecolor='#fefae0', alpha=0.4)
ax.add_feature(cfeature.OCEAN, facecolor='lightblue', alpha=0.9)

# -----------------------------------------
# Plot the data using imshow
# -----------------------------------------
# Define the spatial extent from your coordinate arrays.
extent = [lon.min(), lon.max(), lat.min(), lat.max()]
# Use origin="lower" if your latitude array is in ascending order.
im = ax.imshow(var,
               cmap='Reds',
               origin='lower',
               extent=extent,
               interpolation='none',
               transform=ccrs.PlateCarree())

# Add a colorbar
# -----------------------------------------
cbar = plt.colorbar(im, ax=ax, orientation='vertical', shrink=0.7, pad=0.05)
cbar.set_label('Sand Content [%]', fontsize=16, fontweight='bold', color='black')
cbar.ax.tick_params(labelsize=12)

# -----------------------------------------
# Add gridlines with labeled axes
# -----------------------------------------
gridlines = ax.gridlines(draw_labels=True,
                         color='gray',
                         alpha=0.5,
                         linestyle='--',
                         linewidth=0.5)
gridlines.top_labels = False
gridlines.right_labels = False
gridlines.xlabel_style = {'size': 10, 'color': 'black'}
gridlines.ylabel_style = {'size': 10, 'color': 'black'}

# -----------------------------------------
# Add a custom legend
# -----------------------------------------
land_patch = mpatches.Patch(facecolor='#fefae0', alpha=0.4, edgecolor='black', label='No Data')
ocean_patch = mpatches.Patch(facecolor='lightblue', alpha=0.9, edgecolor='black', label='Ocean')
coastline_line = mlines.Line2D([], [], color='#13315c', linestyle='-', linewidth=2, label='Coastline')
border_line = mlines.Line2D([], [], color='black', linestyle=':', linewidth=2, label='Borders')

legend = plt.legend(handles=[land_patch, ocean_patch, coastline_line, border_line],
                    loc='lower center',
                    bbox_to_anchor=(0.5, -0.2),
                    ncol=4,
                    fontsize=12,
                    frameon=True)
legend.get_frame().set_edgecolor('gray')
legend.get_frame().set_linewidth(1)

# -----------------------------------------
# Add a title and display the plot
# -----------------------------------------
plt.title("Sand Content", fontsize=18, fontweight='bold')
plt.show()
