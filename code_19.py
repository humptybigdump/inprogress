import json

# Create a new dictionary with some keys and values.
data: dict = {"sample_id": 567, "name":"rock1", "mass [kg]":11.58}

# Contert it into a JSON string.
output: str = json.dumps(data)

# Write the file.
with open("output.json", "w") as f:
    f.write(output)
