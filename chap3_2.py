# Demo codes to perform all numerical experiments in chapter 3.2 of my lecture notes
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

#######################################################
# generate figure 3.3
#######################################################

def plot_interpolexample() :
  # data, see table in the lecture notes
  x_points = np.array([-1, 0, 1])
  f_values = np.array([-1, 0, 3])
  # plot the datapoints to interpolate
  plt.plot(x_points,f_values, color='red', marker='s', markersize=8, linestyle=' ')
  # compute and plot the P2 Lagrange interpolant, see file intro for a WARNING
  # that abusing the Gauss normal equations for this is BAD
  # (but admittedly saves a lot of code lines).
  # You might want to reproduce this plot with divided differences and the Horner
  # scheme to check if you understood those.
  # Feel free to send me your implementations, and I will replace this professorial
  # laziness with a proper implementation in the next iteration of this lecture,
  # of course giving proper credit.
  # 
  # see the numpy documentation of polyfit() and polyval() to understand the last few lines
  pol = np.polyfit(x_points,f_values,len(x_points)-1) 
  # plot the interpolant also a bit outside the data
  xx = np.linspace(np.amin(x_points)-1, np.amax(x_points)+1,1001)  
  yy = np.polyval(pol,xx)
  plt.plot(xx, yy, color='red', linestyle='-', linewidth=2, markersize=2)
  plt.savefig('interpolation-beispiel.pdf')
  plt.close()

#######################################################

def vandermonde(n) :
  # creates Vandermonde matrix for n+1 equidistant points in [0,1]
  V = np.zeros((n+1,n+1))
  for i in range(0,n+1,1) :
    xi = i/n
    for j in range(0,n+1,1) :
      V[i,j] = xi**j
  return V

def table_vandermondecondition() :
  # generates table 4.4
  for n in np.array([2,5,10,20]) :
    V = vandermonde(n)
    #print(V)
    print(f'{n:2} {np.linalg.cond(V,1):6.4e} {np.linalg.cond(V,2):6.4e} {np.linalg.cond(V,np.inf):6.4e}')

#######################################################

def lagrange_basispoly(x,i,n) :
  # evaluates the i-th lagrange basis polynomial in x for n+1 equidistant points in [0,1]
  # note that x can be an array, then the return value is also an array
  p = 1.
  for j in range(0,n+1,1) :
    if j != i :
      p = p * (x-j/n) / (i/n-j/n)
  return p

def plot_lagrangebasis() :
  # generates figure 4.5, nothing fancy, just standard function plotting
  xx = np.linspace(0,1,1001)
  for n in np.array([2,3,4]) :
    for i in range(0,n+1,1) :
      yy = lagrange_basispoly(xx,i,n)
      lab = 'n=' + str(n)+', i=' + str(i)
      plt.plot(xx,yy,linestyle='-', linewidth=2, label=lab)
      plt.legend(loc='upper right')
    plt.savefig('lagrange_basispolynome_n' + str(n) + '.pdf')
    plt.close()  

#######################################################

def newton_basispoly(x,i,n) :
  # evaluates the i-th newton basis polynomial in x for n+1 equidistant points in [0,1]
  # note that x can be an array, then the return value is also an array
  if i==0 :
    p = np.ones(len(x))  #ugly hack
  elif i==1 :
  	p = -x_points[0]
  else :  
    p = 1.
    for j in range(0,i,1) :
      p = p * (x-j/n)
  return p

def plot_newtonbasis() :
  # generates figure 4.6, nothing fancy, just standard function plotting
  xx = np.linspace(0,1,1001)
  for n in np.array([2,3,4]) :
    for i in range(0,n+1,1) :
      yy = newton_basispoly(xx,i,n)
      lab = 'n=' + str(n)+', i=' + str(i)
      plt.plot(xx,yy,linestyle='-', linewidth=2, label=lab)
      plt.legend(loc='upper left')
    plt.savefig('newton_basispolynome_n' + str(n) + '.pdf')
    plt.close()  




#######################################################
# actual scripting area
#######################################################


#plot_interpolexample()
#table_vandermondecondition()
plot_lagrangebasis()
#plot_newtonbasis()
