################################################################################
#                                                                              #
#                       EXERCISE 1: BASICS                                     #
#                                                                              #
################################################################################

# Import NumPy
import numpy as np
# Alternative:
# import numpy # -> then you'll have to call functions with the full library name
# instead of a shorter alias
# from numpy import * #-> you do not have to use any alias but this is not a good
# practice with larger libraries as it could lead to severe clashes in names

# Create an array of four zeros
array1 = np.zeros(4)

# Transform this array into a vector with command
array1.shape = (4,1)

# Transform this vector into a 2 × 2 matrix
array1.shape = (2,2)

# Create array A
A = np.array([[1,2],[5,4]])
print('Matrix A')
print(A)
print('')

# Determine the maximum in each row
print('Maximum in each row')
print('Row 1:', np.maximum(A[0,0],A[0,1]))
print('Row 2:', np.maximum(A[1,0],A[1,1]))
print('')

# Determine the maximum element
print('Maximum element')
print(np.amax(A))
print('')

# Construct the matrix C as the inverse of A
C = np.linalg.inv(A)

# Construct column vector b
b = np.array([1,2,3])
b.shape = (3,1)

# Multiply b by 2 (we choose a better name here)
vector_c = b*2

# Construct the inner product of b and vector_c
print('Inner product:')
print(np.transpose(b)@vector_c)
print('')

# Construct the outer product of b and vector_c
print('Outer product:')
print(b@np.transpose(vector_c))
print('')

# Construct the Hadamard product (element-by-element) of b and vector_c
print('Hadamard product')
print(b*vector_c)
print('')

# Run a loop from 0 to 9
print('Loop from 0 to 9')
for i in range(10):
    print(i)
print('')

# Run a loop backwards from 10 to 1 (note that the second input is not included)
print('Loop from 10 to 1')
for i in range(10,0,-1):
    print(i)
print('')
