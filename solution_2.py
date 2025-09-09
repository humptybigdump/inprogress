# Step 1: Download the JSON data file from the given URL and Open the JSON file
import json

filename = "Pedestrian_Crossings.geojson"
with open(filename) as f:
    data = json.load(f)

# Step 2: Figure out what kind of "Site Types" there are
site_types = set()  # Using a set to keep unique site types

for feature in data['features']:
    # Assuming 'properties' contains the site type information
    if 'Site Type' in feature['properties']:
        site_types.add(feature['properties']['Site Type'])

# Step 3: Count the number of each type in the dataset and print it on screen
site_type_counts = {}

for feature in data['features']:
    site_type = feature['properties'].get('Site Type', None)
    if site_type:
        site_type_counts[site_type] = site_type_counts.get(site_type, 0) + 1

# Print the counts
print("Site Type Counts:")
for site_type, count in site_type_counts.items():
    print(f"{site_type}: {count}")

# Step 4: Export the site types and locations (lat, lon) into a new JSON file
site_data = []

for feature in data['features']:
    site_type = feature['properties'].get('Site Type', None)
    coordinates = feature['geometry']['coordinates']
    # Assuming that coordinates are [longitude, latitude]
    if site_type and coordinates:
        site_data.append({
            "Site Type": site_type,
            "Location": {"Latitude": coordinates[1], "Longitude": coordinates[0]}
        })

# Export the data into a new JSON file
with open('pedestrian_crossings_site_data.json', 'w') as output_file:
    json.dump(site_data, output_file, indent=1)

