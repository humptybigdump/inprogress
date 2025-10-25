# Convert a list of temperatures from Celsius to Fahrenheit
celsius = [0, 10, 20, 30, 40]
fahrenheit = [(temp * 9/5) + 32 for temp in celsius]

print(fahrenheit)  # Output: [32.0, 50.0, 68.0, 86.0, 104.0]
