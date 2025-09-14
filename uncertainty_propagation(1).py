"""Example of using the 'uncertainties' package to propagate uncertainties"""
from uncertainties import ufloat, ufloat_fromstr, umath, unumpy, correlation_matrix, correlated_values

# define a variable x with a nominal value of 2 and a standard deviation of 0.25 and tag with name and unit
x = ufloat( 2, 0.25, "x (m)" )

# these variables can also be generated using strings, e.g. with short-hand notation
y = ufloat_fromstr( "-1.0(5)", "y (m)")

# print tag, nominal value and standard deviation
print( "Variable tag, value, std:", y.tag, y.nominal_value, y.std_dev )

# functions of x and y
print( "Simple functions of two variables:", x+y, x-y,x**2/y )

# print breakdown of individual error components
z = umath.cos( 0.2*x**2 + y )

# pretty print
print( "Uncertainty breakdown: z = cos( 0.2x^2 + y) = {:2eP}".format(z) )
for var,err in z.error_components().items():
    print( "  ", var.tag, var, err )

# correlation matrix: x and y uncorrelated, z correlated with both
print( "Correlation matrix of of x, y, z:\n", correlation_matrix( [ x, y, z ] ) )

# create and short-hand print correlated variables with their covariance matrix
val = [ 1, 2, 3 ]
cov = [ [  0.25,  0.10, -0.30 ],
        [  0.10,  1.00,  0.75 ],
        [ -0.30,  0.75,  4.00 ] ]
(a,b,c) = correlated_values( val, cov )
print( "Sum of correlated values: {:+.2uS}".format( a+b+c ) )

# create NumPy array of values and calculate and LaTeX print sum and mean
arr = unumpy.uarray( [2,-1], [0.25,0.5] )
print( "Sum and mean of array: {:L} {:L}".format(arr.sum(), arr.mean()) )