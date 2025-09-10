# Demo codes to perform all numerical experiments in chapter 4 of my lecture notes
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
  # evaluates the i-th hat function in x
  # not vectorised due to professorial laziness 
  # [x_points] defines the local intervals, same indexing as definition 4.19 in the lecture
  n = len(x_points) - 1
  if i==0 :
    return max((x_points[1] - x) / (x_points[1] - x_points[0]),0)
  elif i==n :
    return max((x - x_points[n-1]) / (x_points[n] - x_points[n-1]),0)
  else :
    if (x >= x_points[i-1]) and (x <= x_points[i]) :
      return ((x - x_points[i-1]) / (x_points[i] - x_points[i-1]))
    elif (x >= x_points[i]) and (x <= x_points[i+1]) :
      return (x_points[i+1] - x) / (x_points[i+1] - x_points[i])
    else :
      return 0

#######################################################

def myfunc(func,xx) :
  # evaluates a certain function in all points xx, fully vectorised
  # this function will be implemented in a variety of ways in later codes.
  # Reason: I don't want to have a common file for such things, that I update incrementally.
  # You should really have that, instead of copypasting so much as I do.
  if func==1 :
    res = np.sin(2*np.pi*xx)
  elif func==2 :
    res = 1./ (1+xx*xx)
  elif func == 3 :
    res = np.abs(xx)
  else :
    print('Doofmann') # TODO proper error message :)
  return res


def interpol_error(func,a,b,numpoints) :
  x_points = np.linspace(a,b,num=numpoints)  # interpolation points
  f_values = myfunc(func,x_points) # interpolation values

  xx = np.linspace(a,b,1001) # evaluation points
  ff = myfunc(func,xx) # exact evaluation values for error calculation

  pp = np.zeros(len(xx)) # evaluations of interpolating pw linear polynomial with numpoints-1 intervals
  for j in range(0,len(xx),1) :
    for i in range(0,numpoints,1) :
      pp[j] = pp[j] + hatfunction(x_points,xx[j],i) * f_values[i] 

  # debug output
  #plt.plot(x_points,f_values,marker='s', linestyle=' ', markersize=8, color='red')
  #plt.plot(xx, ff, linestyle='-', linewidth=2, color='red')
  #plt.plot(xx, pp, linestyle='-', linewidth=2, color='blue')
  #plt.savefig('test'+str(numpoints)+'.pdf')
  #plt.close()

  return ff-pp

#######################################################

def table_eoc(do_eoc) :
  # if do_eoc==TRUE, generate table 4.1, otherwise, generate table 3.15
  maxintervals = 15
  errors = np.zeros(maxintervals)
  h = np.zeros(maxintervals)
  for func in [1,2,3] :   # not nice, can be done much better with classes
    if func == 1 :
      a = 0
      b = 1
      print('sine on [0,1]')
    elif func == 2 :
      a = -5
      b = 5
      print('runge')
    elif func == 3 :
      a = -1
      b = 1
      print('abs')
    else :
      print('Doofmann')

    for i in range(1,maxintervals+1,1) :
      numpoints = i+1
      h[i-1] = (b-a)/(numpoints-1)
      errors[i-1] = np.linalg.norm(interpol_error(func,a,b,numpoints), np.inf)
      if (do_eoc) :
        if i>1 :
          print(str(i) + '\t' + str(errors[i-1]) + '\t' + str(np.log(errors[i-2]/errors[i-1]) / np.log(h[i-2]/h[i-1])))
      else :
        print(str(i) + '\t' + str(errors[i-1]))

#######################################################
# stuff for example 1 in chapter 4.2
#######################################################

def extrapol_lhospital() :
  def a(x) :
    return (np.cos(x) - 1) / np.sin(x)

  # first test if evaluating for something small works
  for n in range(1,9,1) :
    print(a(10**(-n)))
  # does work, should not :(

  h = [1/2,1/4,1/8,1/16]
  ah = a(h)
  print(ah)
  pol = np.polyfit(h,ah,len(h)-1) 
  print(np.polyval(pol,0)) 

#######################################################
# stuff for example 2 in chapter 4.2
#######################################################

def extrapol_ableitung() :
  def a(x) :
    return (np.sin(x) - np.sin(np.negative(x))) / (2*x)

  h1 = np.array([1/2, 1/3, 1/4])
  ah1 = a(h1)
  print(ah1)
  pol = np.polyfit(h1,ah1,len(h1)-1) 
  print(np.polyval(pol,0) ) 
  
  h2 = h1**2
  print(ah1)
  pol = np.polyfit(h2,ah1,len(h2)-1) 
  print(np.polyval(pol,0)) 
  


#######################################################
# actual scripting area


table_eoc(False)
#table_eoc(True)       

#extrapol_lhospital()
#extrapol_ableitung()


