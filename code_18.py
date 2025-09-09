import json

# Open the file.
with open("data.json", "r") as f:
    data = json.load(f)

# Print some properties.
print(f"id: {data['id']}")
print(f"name: {data['name']}")
print(f"location: {data['location']}")
print(f"population: {data['population']}")

