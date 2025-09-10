# Demo codes to perform all numerical experiments in chapter 7 of my lecture notes
# "Numerische Mathematik 1".
#
# Tested on the Linux console with Python 3.12.6 and NumPy 2.1.1,
# but any recent Python, NumPy and MatPlotLib should do the trick.
#
# (c) 2019-2024, dominik.goeddeke@mathematik.uni-stuttgart.de


#######################################################
# imports
#######################################################

import matplotlib.pyplot as plt    # for plotting
import numpy as np                 # for linear algebra
from scipy.interpolate import CubicSpline  # to avoid implementing splines myself


#######################################################

def lagrange_basispoly(x,i,x_points) :
  # evaluates the i-th lagrange basis polynomial in x using x_points as support
  n = len(x_points) - 1
  p = 1.
  for j in range(0,n+1,1) :
    if j != i :
      p = p * (x-x_points[j]) / (x_points[i]-x_points[j])
  return p


def plot1(x_points,f_values) :
  # plots the interpolation data, the piecewise linear interpolant and the Lagrange
  # interpolant for the data given in the tupels (x_points[i],f_values[i])
  plt.plot(x_points, f_values, color='blue', marker='s', markersize=8, linestyle=' ')
  plt.plot(x_points, f_values, color='blue', linestyle='-', linewidth=2, label='linear spline')
  
  a = x_points[0]
  b = x_points[len(x_points)-1]
  xx = np.linspace(a,b,1001)
  yy = np.zeros(len(xx))
  for i in range(0,len(x_points),1) :
    yy = yy + f_values[i] * lagrange_basispoly(xx,i,x_points)
  plt.plot(xx, yy, color='green', linestyle='-', linewidth=2, label='Lagrange')
  
  plt.legend(loc='lower right')
  plt.savefig('splines_poly1.pdf')
  plt.close()


def plot2(x_points,f_values) :
  # plots the interpolation data, the piecewise linear interpolant and the spline
  # interpolant for the data given in the tupels (x_points[i],f_values[i])
  plt.plot(x_points, f_values, color='blue', marker='s', markersize=8, linestyle=' ')
  plt.plot(x_points, f_values, color='blue', linestyle='-', linewidth=2, label='linear spline')
  
  a = x_points[0]
  b = x_points[len(x_points)-1]
  xx = np.linspace(a,b,1001)
  cs = CubicSpline(x_points,f_values,bc_type='natural')
  plt.plot(xx, cs(xx), color='green', linestyle='-', linewidth=2, label='cubic natural spline')
  
  plt.legend(loc='lower right')
  plt.savefig('splines_poly2.pdf')
  plt.close()
  
#######################################################

x_points = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
f_values = np.array([1, 8, 3, 3, 5, 3, 9, 7, 7, 9])

#plot1(x_points,f_values)
plot2(x_points,f_values)


