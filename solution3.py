# Task 1: Filter out negative seismic velocities
V_s = [3.2, 4.8, 2.1, 5.6, 7.3, -1.2, 6.1, 3.9, -0.5]
valid_velocities = [v for v in V_s if v > 0]
print(f'Task1: {valid_velocities}')

# Task 2: Normalize gravity anomaly values
g = [-40, -10, 0, 15, 30, 50, 80]
g_min, g_max = min(g), max(g)
normalized_g = [(x - g_min) / (g_max - g_min) for x in g]
print(f'Task2: {normalized_g}')

# Task 3: Extract high-resistivity regions
R = [20, 45, 150, 200, 25, 300, 500, 60, 1000]
high_resistivity = [r for r in R if r > 100]
print(f'Task3: {high_resistivity}')

# Task 4: Convert depths from meters to kilometers
d = [100, 250, 500, 1000, 1500, 3000]
depth_km = [depth / 1000 for depth in d]
print(f'Task4: {depth_km}')

# Task 5: Classify subsurface layers based on seismic velocity
categories = ["Sedimentary" if v < 3.5 else "Metamorphic" if v < 5.0 else "Igneous" for v in valid_velocities]
print(f'Task5: {categories}')

