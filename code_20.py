import json

# Define a new class.
class Point:
    def __int__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    # Specify a method to convert the class into a Python dict.
    # Then return the JSON string.
    def to_json(self) -> str:
        data = {"x": self.x, "y": self.y}
        return json.dumps(data)

# Create a new Point object.
p: Point = Point(34.67, -12.78)

# Convert into a JSON string.
p_as_json: str = p.to_json()

# Write to a file.
with open("point.json", "w") as f:
    f.write(p_as_json)
