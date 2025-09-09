# Traditional for loop approach
squares = []
for x in range(10):
    squares.append(x ** 2)

# Equivalent list comprehension
squares = [x ** 2 for x in range(10)]

print(squares)  # Output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
