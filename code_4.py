# Traditional for loop approach
even_numbers = []
for x in range(20):
    if x % 2 == 0:
        even_numbers.append(x)

# Equivalent list comprehension
even_numbers = [x for x in range(20) if x % 2 == 0]

print(even_numbers)  # Output: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
