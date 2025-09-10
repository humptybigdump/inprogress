# Demo codes to perform all numerical experiments in chapter 3.1 of my lecture notes
# "Numerische Mathematik 1".
#
# Tested on the Linux console with Python 3.12.6 and NumPy 2.1.1,
# but any recent Python, NumPy and MatPlotLib should do the trick.
#
# (c) 2019-2024, dominik.goeddeke@mathematik.uni-stuttgart.de
#
# Scroll to the end of the file to comment in/out selected functionality.
#
# Warning: the way we do Lagrange interpolation here via
#   np.polyfit() and np.polyval()
# is numerically unstable and a hack, we abuse another method (see Chapter 6.1) 
# because it requires less typing. 
# In your codes, you should really be using divided differences.


#######################################################
# imports
#######################################################

import matplotlib.pyplot as plt    # for plotting
import numpy as np                 # for linear algebra

import warnings
warnings.filterwarnings("ignore")  # highly discouraged, used because in trigcardinal() 
                                   # we deliberately divide by zero

#######################################################

def plot1() :
  # generates figure 3.1
  n = 100
  xexact = np.linspace(0,np.pi,n+2)  # nothing fancy, just standard function plotting
  sinexact = np.sin(xexact)
  x = np.array([0, np.pi/2, np.pi])  # function plotting with three evaluations instead of "smoothly many"
  sinx = np.sin(x)
  plt.plot(xexact,sinexact, color='blue', linestyle='-', linewidth=2, markersize=2)
  plt.plot(x,sinx, color='green', linestyle='-', linewidth=2, markersize=2)
  plt.savefig('motivation_example2_1.pdf')
  plt.close()

#######################################################

def plot2() :
  # generates figure 3.1
  n = 100
  xexact = np.linspace(0,np.pi,n+2)
  sinexact = np.sin(xexact)
  x = np.array([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
  sinx = np.sin(x)
  plt.plot(xexact,sinexact, color='blue', linestyle='-', linewidth=2, markersize=2)
  plt.plot(x,sinx, color='green', linestyle='-', linewidth=2, markersize=2)
  plt.savefig('motivation_example2_2.pdf')
  plt.close()

#######################################################

def plot3() :
  # generates figure 3.1
  n = 100
  xexact = np.linspace(0,np.pi,n+2)
  sinexact = np.sin(xexact)
  x = np.array([0, np.pi/8, np.pi/4, 3*np.pi/8, np.pi/2, 5*np.pi/8, 3*np.pi/4, 7*np.pi/8, np.pi])
  sinx = np.sin(x)
  plt.plot(xexact,sinexact, color='blue', linestyle='-', linewidth=2, markersize=2)
  plt.plot(x,sinx, color='green', linestyle='-', linewidth=2, markersize=2)
  plt.savefig('motivation_example2_3.pdf')
  plt.close()

#######################################################
# stuff to generate figure 3.2
# shamelessly adapted from https://en.wikipedia.org/wiki/Trigonometric_interpolation
# all this will be explained in Numerische Mathematik 2
# for this lecture, I recommend to ignore the code
#######################################################

def f_trig(x) :                  # function to interpolate
  return np.sin(2*x) + np.sin(4*x) + np.cos(x)

def triginterp(xi,x,y) :         # computes the triginometric interpolant of the pairs x,y
  N = len(x)                     # in all points in xi
  h = 2/N;                       # adjust the spacing of the given independent variable
  scale = (x[1]-x[0]) / h
  x = x/scale
  xi = xi/scale
  P = np.zeros(len(xi))          # evaluate interpolant
  for k in range(0,N,1) :
    P = P + y[k]*trigcardinal(xi-x[k],N)
  return P

def trigcardinal(x,N) :          # helper function to compute the terms of the interpolant
  if np.mod(N,2)==1 :            # odd number of interpolation points
    tau = np.sin(N*np.pi*x/2) / (N*np.sin(np.pi*x/2))
  else :                         # even number of interpolation points
    tau = np.sin(N*np.pi*x/2) / (N*np.tan(np.pi*x/2))
  tau[x==0] = 1                  # fix value at x=0 instead of divide by zero
  return tau

def plot4() :
  # set xtics to multiples of pi
  plt.xticks(np.arange(-2*np.pi,5*np.pi,step=np.pi))

  # plot two helper lines
  plt.axvline(x=0, color='black', linestyle='--', linewidth=1, markersize=1)
  plt.axvline(x=2*np.pi, color='black', linestyle='--', linewidth=1, markersize=1)

  # define and plot interpolation points
  n = 5
  x_points = np.linspace(0,2*np.pi,n+1)
  y_points = f_trig(x_points)
  plt.plot(x_points,y_points, color='green', marker='o', markersize=8, linestyle=' ')

  # plot original function
  nn = 1000  # linspace stepsize for plotting
  x_orig = np.linspace(-2*np.pi-0.1,4*np.pi+0.1,nn+2)
  y_orig = f_trig(x_orig)
  plt.plot(x_orig,y_orig, color='black', linestyle='-', linewidth=2, markersize=2)

  # compute (using NumPy functions) and plot Lagrange interpolant
  x_poly = np.linspace(0,2*np.pi,n+1)            # interpolation points
  y_poly = f_trig(x_poly)                        # values to interpolate
  pol = np.polyfit(x_poly,y_poly,len(x_poly)-1)  # coefficients of the interpolating polynomial (note that this computes a least squares approximation, which coincides with the Lagrange interpolant since degree = n-1
  y_poly = np.polyval(pol,x_orig)                # important: evaluate polynomial everywhere for plotting, not just at interpolation points
  plt.plot(x_orig,y_poly, color='blue', linestyle='-', linewidth=2, markersize=2)

  # adjust axis to actually see something
  plt.axis([min(x_orig)-0.1, max(x_orig)+0.1, min(y_orig)-0.1, max(y_orig)+0.1])

  # compute (using https://en.wikipedia.org/wiki/Trigonometric_interpolation) the trigonometric interpolant in [0,2pi]
  x_trig = x_points[:-1]                     # don't use last point on the right side for trigo interpolation
  y_trig = f_trig(x_trig)                    # values to interpolate in plot space
  xi_trig = np.linspace(0,2*np.pi,nn)
  y_trig = triginterp(xi_trig,x_trig,y_trig) # compute trigonometric interpolant values in plot points
  # concatenate periodic interpolants for final plot
  xi_trig = np.concatenate((xi_trig - 2*np.pi, xi_trig, xi_trig + 2*np.pi))
  y_trig = np.concatenate((y_trig, y_trig, y_trig))

  plt.plot(xi_trig,y_trig, color='red', linestyle='-', linewidth=2, markersize=2)
  plt.savefig('motivation_poly_trig.pdf')
  plt.close()

#######################################################
# actual scripting area
#######################################################


#plot1()
#plot2()
#plot3()
plot4()