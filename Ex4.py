################################################################################
#                                                                              #
#                   EXERCISE 4: FUNCTION APPROXIMATION                         #
#                                                                              #
################################################################################
# Import the necessary libraries
import numpy as np
import scipy.interpolate as spi
import matplotlib.pyplot as plt

# Set the boundaries
x = 0.0
y = 2*np.pi

# Create an array of n=10 equidistant evaluation points
n = 10
xgrid = np.linspace(x,y,n)
ypts = np.sin(xgrid)

# Create an array of 100 query points
nx = 100
xp = np.linspace(x,y,nx)

## Define the interpolant and evaluate it at the query points
# Linear interpolation
xpLin_10 = spi.interp1d(xgrid,ypts,'linear')
yp_lin = xpLin_10(xp)

# Cubic spline interpolation
xpCub_10 = spi.interp1d(xgrid,ypts,'cubic')
yp_cub = xpCub_10(xp)

# Plot both linear and cubic interpolations
fig,ax=plt.subplots(figsize=(10,6))
ax.plot(xp,yp_lin,xp,yp_cub)
plt.show()

# We repeat this exercise, but this time choose n=50
x = 0.0
y = 2*np.pi
n = 50

xgrid = np.linspace(x,y,n)
ypts = np.sin(xgrid)
xpLin_50 = spi.interp1d(xgrid,ypts,'linear')
yp_lin = xpLin_50(xp)
xpCub_50 = spi.interp1d(xgrid,ypts,'cubic')
yp_cub = xpCub_50(xp)

# Plot both linear and cubic interpolations

fig,ax=plt.subplots(figsize=(10,6))
ax.plot(xp,yp_lin,xp,yp_cub)
plt.show()

## Evaluate accuracy of Approximation

np.random.seed(seed=26102021)
TT = 100
# Draw random numbers and transform them to [0,2*pi]
evalPoints = np.random.rand(TT)*2*np.pi

fTrue = np.sin(evalPoints)
fImpL10 = xpLin_10(evalPoints)
fImpL50 = xpLin_50(evalPoints)
fImpC10 = xpCub_10(evalPoints)
fImpC50 = xpCub_50(evalPoints)

AvgErrorL10 = np.sum((np.abs(fTrue-fImpL10)))/TT
AvgErrorL50 = np.sum((np.abs(fTrue-fImpL50)))/TT
AvgErrorC10 = np.sum((np.abs(fTrue-fImpC10)))/TT
AvgErrorC50 = np.sum((np.abs(fTrue-fImpC50)))/TT

MaxErrorL10 = np.amax(np.abs(fTrue-fImpL10))
MaxErrorL50 = np.amax(np.abs(fTrue-fImpL50))
MaxErrorC10 = np.amax(np.abs(fTrue-fImpC10))
MaxErrorC50 = np.amax(np.abs(fTrue-fImpC50))

print(' ')
print('Average Errors')
print('L10', AvgErrorL10)
print('L50', AvgErrorL50)
print('C10', AvgErrorC10)
print('C50', AvgErrorC50)
print(' ')
print('Maximum Errors')
print('L10', MaxErrorL10)
print('L50', MaxErrorL50)
print('C10', MaxErrorC10)
print('C50', MaxErrorC50)
