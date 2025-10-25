from itertools import islice

# A generator for the Fibonacci sequence
def fibonacci():
    """Generates an infinite sequence of Fibonacci numbers"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b  # Update values

# Using the generator
for n in islice(fibonacci(), 10):
    print(n)  # Print the first 10 Fibonacci numbers
