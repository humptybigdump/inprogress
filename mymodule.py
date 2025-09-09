import numpy as np

def g(x):
    y = x-5
    z = x
    return np.log(y*z)


print("Hello from mymodule!")
print("This is a test of the mymodule.py file.")
print(f"Runing g(5) gives the result of: {g(5)}")