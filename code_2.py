def divide_numbers(a, b):
    """Divides two numbers and handles division by zero errors."""
    try:
        result = a / b
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"
    except Exception as e:
        return f"Unexpected error occurred: {e}"

# Example Usage
print(divide_numbers(10, 2))  # Output: Result: 5.0
print(divide_numbers(5, 0))   # Output: Error: Cannot divide by zero!
