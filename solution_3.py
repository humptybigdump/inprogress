# Step 1: Download the JSON data file from the given URL and Open the JSON file

import json
import bz2
from collections import Counter

filename = "Pedestrian_Crossings.geojson.bz2"
with bz2.BZ2File(filename) as f:
    data = json.load(f)

# Step 2: Figure out what kind of "Site Types" there are.
# Counter is a data type (class) that helps with counting.
num_of_sites: Counter = Counter() 
all_sites = []

for feature in data["features"]:
    # Use structrual pattern matching.
    match feature:
        case {"properties": {"Site Type": site_type}, "geometry": {"type": "Point", 
            "coordinates": [lon, lat]}}:
            # Step 3: Count the number of sites.
            num_of_sites[site_type] += 1
            # Store the geometry data.
            all_sites.append({"Site Type": site_type, "geometry": [lon, lat]})

# Print the number for each site.
print(f"Num of site type: {num_of_sites}")

# Step 4: Export the data into a new JSON file.
with open('pedestrian_crossings_site_data.json', 'w') as output_file:
    json.dump(all_sites, output_file, indent=1)

