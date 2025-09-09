print(random.sample(fruits, 2))  # Without replacement (e.g., ['banana', 'orange'])
print(random.choices(fruits, k=2)) With replacement
print(np.random.choice(fruits, size=2, replace=False))  # NumPy equivalent
