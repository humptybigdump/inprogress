# Function to calculate groundwater flow using Darcy's Law
def calculate_groundwater_flow(K, A, delta_h, L):
    """Computes groundwater flow rate using Darcy's Law, handling errors."""
    try:
        if K < 0 or A < 0 or delta_h < 0:
            raise ValueError("K, A, and delta_h must be non-negative.")

        Q = (K * A * delta_h) / L  # Darcy’s Law formula
        return f"Groundwater flow rate: {Q:.4f} m³/s"

    except ZeroDivisionError:
        return "Error: Flow path length (L) cannot be zero!"
    except TypeError:
        return "Error: All inputs must be numerical values!"
    except ValueError as e:
        return f"Error: {e}"

# Example Tests
print(calculate_groundwater_flow(1.5, 10, 5, 20))  # Valid input
print(calculate_groundwater_flow(2.0, 5, 3, 0))   # Division by zero
print(calculate_groundwater_flow("high", 10, 5, 20))  # Invalid input type
print(calculate_groundwater_flow(-1.5, 10, 5, 20))  # Negative value error

