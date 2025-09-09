import re

# Task 1: Extract all monitoring well IDs (e.g., Well-123) from a dataset of groundwater data
text = "Well-101 is located at site A, Well-102 at site B, and Well-103 at site C."
pattern = r"Well-\d+"  # Matches 'Well-' followed by digits
well_ids = re.findall(pattern, text)
print("Monitoring Well IDs:", well_ids)

# Task 2: Replace all instances of 'monitoring well' with 'MW' in a list of sample locations
sample_locations = "The monitoring well at site A is monitored daily. Monitoring well at site B is active."
modified_text = re.sub(r"monitoring well", "MW", sample_locations, flags=re.IGNORECASE)
print("Modified Locations:", modified_text)

# Task 3: Validate if a given string is a valid format for a well depth in the format XX.XX m (e.g., 50.25 m)
depths = ["50.25 m", "100.1 m", "200.45 m", "300 m"]
depth_pattern = r"^\d{2,3}\.\d{2} m$"  # Matches depth format 'XX.XX m'
valid_depths = [depth for depth in depths if re.match(depth_pattern, depth)]
print("Valid Well Depths:", valid_depths)

# Task 4: Extract and standardize the date format from field data logs (e.g., from 2025-03-25 to 25/03/2025)
dates = "The data was recorded on 2025-03-25 and 2026-04-30."
date_pattern = r"(\d{4})-(\d{2})-(\d{2})"  # Matches the date format YYYY-MM-DD
standardized_dates = re.sub(date_pattern, r"\3/\2/\1", dates)  # Reverses the order to DD/MM/YYYY
print("Standardized Dates:", standardized_dates)

# Task 5: Identify and clean up any text anomalies such as extra spaces or unwanted characters in the geophysical readings
geophysical_readings = "   12.3, 14.5   , 16.7 ,   18.2,  "
cleaned_readings = re.sub(r"\s*,\s*", ",", geophysical_readings)  # Remove extra spaces around commas
cleaned_readings = re.sub(r"^\s+|\s+$", "", cleaned_readings)  # Remove leading and trailing spaces
print("Cleaned Geophysical Readings:", cleaned_readings)

