import time

# Timing decorator
def timing_decorator(func):
    def wrapper(*args, kwargs):
        start_time = time.time()
        result = func(*args, kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

@timing_decorator
def compute_square(n):
    return [x2 for x in range(n)]

compute_square(1000000)  # Measure execution time
