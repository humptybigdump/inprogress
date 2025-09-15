################################################################################
#                                                                              #
#                       EXERCISE 3: ROOT-FINDING                               #
#                                                                              #
################################################################################

# Import the necessary libraries
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt


# Declare x as a symbolic variable
x = sym.symbols('x')

# Set up the equation
f = x**3 - x - 1

# Compute the first derivative
df = sym.diff(f,x)

print('Evaluate the function at x=2')
print(f.subs(x,2.0))
print('')

# Set a first guess
x_guess = -5.0

# Set up the Newton-Raphson solver
for i1 in range(1000):

    # Calculate the new x given your guess and the Newton-Raphson formula
    x_new = x_guess - f.subs(x,x_guess)/df.subs(x,x_guess)
    # Calculate the absolute difference between the old x and the new x
    metric = np.abs(x_new-x_guess)
    # You may want to print the result
    print(i1,metric)

    # If metric is below your convergence criterion, break the loop
    if metric<1e-10:
        break

    # Adjust your guess
    x_guess = x_new


# Print the solution
print('')
print('The root to f is:', x_new)
print('')

# An alternative way to find the root of f is to use fsolve from Scipy’s optimize
# sublibrary
import scipy.optimize as spo

# Define f as a (non-symbolic) function
def function_f(x_g):

    fx = x_g**3 - x_g - 1.0

    return fx

# Set a first guess
x_guess = 2.0

# Find the root with the help of fsolve
result,info,ier,msg= spo.fsolve(function_f,x_guess,args=(),full_output=1)

# Print the solution
print('The root to f is:', result)
# More information on the solution
print(info)
# Convergence info: if 1 a solution was found
print(ier)
# Convergence info in text
print(msg)
