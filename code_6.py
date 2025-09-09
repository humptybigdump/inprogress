# A simple generator function
def count_up_to(n):
    """Yields numbers from 1 to n"""
    count = 1
    while count <= n:
        yield count
        count += 1  # Increments the counter

# Using the generator
for num in count_up_to(5):
    print(num)

# Output: 1, 2, 3, 4, 5
