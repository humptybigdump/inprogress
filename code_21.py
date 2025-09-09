# Define some data.
data = [
    {"type": "Point", "coordinates": [1, 2]},
    {"type": "Point", "coordinates": [4, 5]},
    {"type": "Point", "coordinates": [9, 9]},
    {"type": "LineString", 
        "coordinates": [[3, 6], [-2, 7], [1, 1], [4, 9]]}
]

# Iterate through all the elements of the list.
for elem in data:
    # Match each element.
    match elem:
        # Here it is a point.
        case {"type": "Point", "coordinates": [x, y]}:
            print(f"Just a point: {x=}, {y=}")
        # And here it is a line.
        case {"type": "LineString", "coordinates": pos_list}:
            print(f"A line: {pos_list=}")
        # It must be something else.
        case _:
            print(f"Something else...")

