# Demo codes to perform all numerical experiments in chapter 3.4 of my lecture notes
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

#######################################################
# stuff to generate figure 3.13
#######################################################

def p(x) :
  return 1.5 + 0.5*x*x + x*x*x 

def pstrich(x) :
  return 0 + 2*0.5*x + 3*1*x*x

def plot_hermiteexample() :
  # data
  x_points = np.array([-1, 1])
  f_values = np.array([1, 3])
  fstrich_values = np.array([2, 4])
  plt.plot(x_points,f_values, color='red', marker='s', markersize=8, linestyle=' ')
  plt.plot(x_points,fstrich_values, color='blue', marker='s', markersize=8, linestyle=' ')
  # Hermite
  xx = np.linspace(-1,1,1001)
  yy = p(xx)
  plt.plot(xx, yy, color='red', linestyle='-', linewidth=2, markersize=2)
  yy = pstrich(xx)
  plt.plot(xx, yy, color='blue', linestyle='-', linewidth=2, markersize=2)
  plt.savefig('hermite-example.pdf')
  plt.close()
  
#######################################################

plot_hermiteexample()

# another example is coded up in chap4.py
