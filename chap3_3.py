# Demo codes to perform all numerical experiments in chapter 3.3 of my lecture notes
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
# is numerically unstable and a hack, we abuse another method (see Chapter 7.1) 
# because it requires less typing. 
# In your codes, you should really be using divided differences.


#######################################################
# imports
#######################################################

import matplotlib.pyplot as plt    # for plotting
import numpy as np                 # for linear algebra

#######################################################

def lagrange_basispoly(x,i,n,x_points) :
  # evaluates the i-th Lagrange basis polynomial in x for interpolation points x_points
  # note that x can be an array, then the return value is also an array
  # difference to chap4_2.py: arbitrary interval
  p = 1.
  for j in range(0,n+1,1) :
    if j != i :
      p = p * (x-x_points[j]) / (x_points[i]-x_points[j])
  return p

def newton_basispoly(x,i,n,x_points) :
  # evaluates the i-th Newton basis polynomial in x for interpolation points x_points
  # note that x can be an array, then the return value is also an array
  # difference to chap4_2.py: arbitrary interval
  if i==0 :
    p = np.ones(len(x))
  elif i==1 :
  	p = x-x_points[0]
  else :  
    p = np.ones(len(x))
    for j in range(0,i,1) :
      p = p * (x-x_points[j])
  return p

#######################################################

def table_lebesgueconstants() :
  # generates table 4.7
  for n in np.array([5,10,15,20]) :
    # compute Lebesgue constants by naive sampling -- not accurate but easy
    # The main point here is that we need to somehow "approximate" the maximum
    # over a continous interval [a,b]. We do this in a brute force way, by sampling
    # the interval 1001 times, summing up the Lagrange polynomials in all those
    # sample points, and then taking the maximum over all these summed samples.
    a = 0
    b = 1
    xx = np.linspace(a,b,1001)
    x_points = np.linspace(a,b,n+1)  # sample points
    sum = np.zeros(len(xx))          # holds the sum values for each sample point
    for i in range(0,n+1,1) :
      sum = sum + np.abs(lagrange_basispoly(xx,i,n,x_points))
    m = np.max(sum)  
    print(f'{n:2} {m:6.4e}')

#######################################################

def plot_lagrangebasis() :
  # generates figure 4.8, just standard function plotting from pointwise evaluations
  xx = np.linspace(0,1,1001)
  a = 0
  b = 1
  for n in np.array([5,10,15,20]) :
    x_points = np.linspace(a,b,n+1)  # interpolation points
    for i in range(0,n+1,1) :
      yy = lagrange_basispoly(xx,i,n,x_points)
      lab = 'n=' + str(n)+', i=' + str(i)
      plt.plot(xx,yy,linestyle='-', linewidth=2, label=lab)
      #plt.legend(loc='upper right')
    plt.savefig('lagrange_basispolynome_n' + str(n) + '.pdf')
    plt.close()  

#######################################################

def plot_newtonbasis() :
  # generates figure 4.9, just standard function plotting from pointwise evaluations
  xx = np.linspace(0,1,1001)
  a = 0
  b = 1
  for n in np.array([5,10,15,20]) :
    x_points = np.linspace(a,b,n+1)  # interpolation points
    for i in range(0,n+1,1) :
      yy = newton_basispoly(xx,i,n,x_points)
      lab = 'n=' + str(n)+', i=' + str(i)
      plt.plot(xx,yy,linestyle='-', linewidth=2, label=lab)
      #plt.legend(loc='upper left')
    plt.savefig('newton_basispolynome_n' + str(n) + '.pdf')
    plt.close()  

#######################################################

def table_newtonpolys() :
  # generates table 4.10, see table_lebesgueconstants() for how we do it
  for n in np.array([5,10,15,20,25,30]) :
    # compute Newton infty poly norms by naive sampling -- not accurate but easy
    a = -1
    b = 1
    xx = np.linspace(a,b,1001)
    x_points = np.linspace(a,b,n+1)  # sample points
    m1 = np.max(np.abs(newton_basispoly(xx,n+1,n+1,x_points)))
    a = -5
    b = 5
    xx = np.linspace(a,b,1001)
    x_points = np.linspace(a,b,n+1)  # sample points
    m2 = np.max(np.abs(newton_basispoly(xx,n+1,n+1,x_points)))
    print(f'{n:2} {m1:6.4e} {m2:6.4e}')
    
#######################################################
# stuff to generate figure 3.11
#######################################################

def f1(x) :
  # first test function, if x is an array then an array is returned
  return np.sin(2*np.pi*x)

def f2(x) :
  # second test function, if x is an array then an array is returned
  return 1./ (1+x*x)  

def f3(x) :
  # third test function, if x is an array then an array is returned
  return np.abs(x)

def plot_sineexample() :
  # create 3 figures in one go
  for n in np.array([4,8,16]) :
    a = 0
    b = 1
    xx = np.linspace(a,b,1001)
    # plot exact function
    yy = f1(xx)
    plt.plot(xx,yy,color='black', linewidth=2, linestyle='-')
    # create interpolation points
    x_points = np.linspace(a,b,n+1)
    # create interpolation data
    f_values = f1(x_points)
    # plot interpolation data
    plt.plot(x_points,f_values, color='red', marker='s', markersize=8, linestyle=' ')
    # compute interpolant, again in a hacky highly discouraged way. 
    # Feel free to insert your own divided difference implementation here, 
    # if the plots look the same, then your implementation is as correct as mine.
    pol = np.polyfit(x_points,f_values,len(x_points)-1) 
    yy = np.polyval(pol,xx)
    plt.plot(xx, yy, color='red', linestyle='-', linewidth=2, markersize=2)
    plt.savefig('sinus' + str(n) + '.pdf')
    plt.close()

def plot_rungeexample() :
  # see above for documentation. This can be done much cooler with classes and the like,
  # but professorial laziness implies copypaste. You should not follow my example.
  for n in np.array([4,8,16]) :
    a = -5
    b = 5
    xx = np.linspace(a,b,1001)
    yy = f2(xx)
    plt.plot(xx,yy,color='black', linewidth=2, linestyle='-')
    x_points = np.linspace(a,b,n+1)
    f_values = f2(x_points)
    plt.plot(x_points,f_values, color='red', marker='s', markersize=8, linestyle=' ')
    pol = np.polyfit(x_points,f_values,len(x_points)-1) 
    yy = np.polyval(pol,xx)
    plt.plot(xx, yy, color='red', linestyle='-', linewidth=2, markersize=2)
    plt.savefig('runge' + str(n) + '.pdf')
    plt.close()

def plot_absexample() :
  # see above for documentation. This can be done much cooler with classes and the like,
  # but professorial laziness implies copypaste. You should not follow my example.
  for n in np.array([4,8,16]) :
    a = -1
    b = 1
    xx = np.linspace(a,b,1001)
    yy = f3(xx)
    plt.plot(xx,yy,color='black', linewidth=2, linestyle='-')
    x_points = np.linspace(a,b,n+1)
    f_values = f3(x_points)
    plt.plot(x_points,f_values, color='red', marker='s', markersize=8, linestyle=' ')
    pol = np.polyfit(x_points,f_values,len(x_points)-1) 
    yy = np.polyval(pol,xx)
    plt.plot(xx, yy, color='red', linestyle='-', linewidth=2, markersize=2)
    plt.savefig('abs' + str(n) + '.pdf')
    plt.close()

#######################################################

def table_interperrors() :
  # generates table 4.12
  # see table_lebesgueconstants() for an explanation on how we implement the maxnorm by sampling
  for n in np.array([0,4,8,16,32]) :
    xx_sine = np.linspace(0,1,1001)
    func_sine = f1(xx_sine)
    x_points_sine = np.linspace(0,1,n+1)
    f_values_sine = f1(x_points_sine)
    pol = np.polyfit(x_points_sine,f_values_sine,len(x_points_sine)-1) 
    interp = np.polyval(pol,xx_sine)
    error_sine = np.max(np.abs(func_sine - interp))
    
    xx_runge = np.linspace(-5,5,1001)
    func_runge = f2(xx_runge)
    x_points_runge = np.linspace(-5,5,n+1)
    f_values_runge = f2(x_points_runge)
    pol = np.polyfit(x_points_runge,f_values_runge,len(x_points_runge)-1) 
    interp = np.polyval(pol,xx_runge)
    error_runge = np.max(np.abs(func_runge - interp))

    xx_abs = np.linspace(-1,1,1001)
    func_abs = f3(xx_abs)
    x_points_abs = np.linspace(-1,1,n+1)
    f_values_abs = f3(x_points_abs)
    pol = np.polyfit(x_points_abs,f_values_abs,len(x_points_abs)-1) 
    interp = np.polyval(pol,xx_abs)
    error_abs = np.max(np.abs(func_abs - interp))

    print(f'{n:2} {error_sine:6.4e} {error_runge:6.4e} {error_abs:6.4e}') 



#######################################################
# actual scripting area
#######################################################


table_lebesgueconstants()
#plot_lagrangebasis()
#plot_newtonbasis()
#table_newtonpolys()
#plot_sineexample()
#plot_rungeexample()
#plot_absexample()
#table_interperrors()
