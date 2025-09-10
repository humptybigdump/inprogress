# Demo codes to perform all numerical experiments in chapter 3.5 of my lecture notes
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

def hatfunction(x_points,x,i) :
  # evaluates the i-th hat function in x, not vectorised. 
  # x_points defines the local intervals
  n = len(x_points) - 1
  if i==0 :
    return max((x_points[1] - x) / (x_points[1] - x_points[0]),0)
  elif i==n :
    return max((x - x_points[n-1]) / (x_points[n] - x_points[n-1]),0)
  else :
    if (x >= x_points[i-1]) and (x <= x_points[i]) :
      return (x - x_points[i-1]) / (x_points[i] - x_points[i-1])
    elif (x >= x_points[i]) and (x <= x_points[i+1]) :
      return (x_points[i+1] - x) / (x_points[i+1] - x_points[i])
    else :
      return 0

def colormap(i, shifted) :
  # utility function to avoid conditionals, see e.g.
  # https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python 
  # on how to do switch statements in python. This solution uses dictionary functionality.
  # if shifted==TRUE, start with blue, instead start with red and skip blue
  if shifted :
    colors = {0:'blue', 1:'red', 2:'green', 3:'cyan', 4:'magenta'}
  else:
    colors = {0:'red', 1:'green', 2:'cyan', 3:'magenta'}
  return colors.get(i, 'black')

def plot_linearpiecewise(x_points,f_values) :
  # plots the interpolation data and the piecewise linear interpolant for the data 
  # given in the tupels (x_points[i],f_values[i])
  # figure 4.14 left
  plt.plot(x_points, f_values, color=colormap(0,True), marker='s', markersize=8, linestyle=' ')
  plt.plot(x_points, f_values, color=colormap(0,True), linestyle='-', linewidth=2)
  plt.axis([min(x_points)-0.1, max(x_points)+0.1, -0.1, 1.1])
  plt.savefig('pw_ploynom_interpol_function.pdf')
  plt.close()

def plot_hatfunctions(x_points) :
  # plot the hat functions defined by the intervals defined by x_points
  # figure 4.14 centre
  # note that due to the missing array-isation (vectorisation) of the hat function
  # implementation, we need another loop here that we didn't need before. This can be 
  # done in a much better way, but my time is limited.
  n = len(x_points) - 1
  for i in range(0,n+1,1) :
    xx = np.linspace(x_points[0], x_points[n], 1001)
    yy = np.zeros(len(xx))
    for j in range(0,len(yy),1) :
      x = xx[j]
      yy[j] = hatfunction(x_points,x,i)
    lab = 'H_' + str(i)
    plt.plot(xx, yy, color=colormap(i,False), linestyle='-', linewidth=2, label=lab)
    plt.legend(loc='upper right')
    plt.axis([min(x_points)-0.1, max(x_points)+0.1, -0.1, 1.1])
  plt.savefig('pw_ploynom_interpol_basisfunc.pdf')
  plt.close()

def plot_basisrepresentation(x_points,f_values) :
  # plot the piecewise linear interpolant of the data 
  # figure 4.14 right
  plt.plot(x_points, f_values, color=colormap(0,True), marker='s', markersize=8, linestyle=' ')
  plt.plot(x_points, f_values, color=colormap(0,True), linestyle='-', linewidth=2)
  # plot the basis functions (hat functions) weighted by the data, no idea how to vectorise
  n = len(x_points) - 1
  xx = np.linspace(x_points[0], x_points[n], 1001)
  yy = np.zeros(len(xx))
  for i in range(0,n+1,1) :
    for j in range(0,len(yy),1) :
      x = xx[j]
      yy[j] = f_values[i] * hatfunction(x_points,x,i)
    plt.plot(xx, yy, color=colormap(i+1,True), linestyle='-', linewidth=2)
  plt.axis([min(x_points)-0.1, max(x_points)+0.1, -0.1, 1.1])
  plt.savefig('pw_ploynom_interpol_basisrepresentation.pdf')
  plt.close()

#######################################################

x_points = np.array([0, 2, 3, 6])
f_values = np.array([0.2, 0.8, 0.5, 0.65])



plot_linearpiecewise(x_points,f_values)
plot_hatfunctions(x_points)
plot_basisrepresentation(x_points,f_values)

# table 3.15 is implemented in chap4.py

