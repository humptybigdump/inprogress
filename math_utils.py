# Function to add two numbers
def add(a, b):
    return a + b

# Function to subtract two numbers
def subtract(a, b):
    return a - b

# Function to multiply two numbers
def multiply(a, b):
    return a * b

# Function to divide two numbers
def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b

# Test the module when run directly
if __name__ == "__main__":
    print("Testing math_utils module:")
    print(f"Addition: {add(5, 3)}")       # Output: 8
    print(f"Subtraction: {subtract(5, 3)}")  # Output: 2
    print(f"Multiplication: {multiply(5, 3)}")  # Output: 15
    print(f"Division: {divide(6, 3)}")     # Output: 2.0
