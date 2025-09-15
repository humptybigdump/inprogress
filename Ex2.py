################################################################################
#                                                                              #
#                       EXERCISE 2: FUNCTIONS                                  #
#                                                                              #
################################################################################

# Import the necessary libraries
import numpy as np

# Write a function that determines the maximum of the absolute difference
# between two given arrays.
def max_norm(array1,array2):

    maxNorm = np.amax(np.abs(array1-array2))

    return maxNorm


# Use the arrays b and c from Exercise 1 to test your function
vector_b = np.array([1,2,3])
vector_b.shape = (3,1)
vector_c = vector_b*2

print(max_norm(vector_b,vector_c))


# Write a function util that, given scalar inputs x and sigma
def util(x,sigma):

    utility = (x>0.0)*((x**(1.0-sigma)-1.0)/(1.0-sigma)) + (x<=0.0)*(-10000000.0)

    # if (x>0.0):
    #     utility = (x**(1.0-sigma)-1.0)/(1.0-sigma)
    # else:
    #     utility = -10000000.0

    return utility

sigma = 2.0
array = np.array([-1,3,-5,10])

print(util(array,sigma))
