# Demo codes to perform all numerical experiments in chapter 8 of my lecture notes
# "Numerische Mathematik 1".
#
# Tested on the Linux console with Python 3.12.6 and NumPy 2.1.1,
# but any recent Python, NumPy and MatPlotLib should do the trick.
#
# (c) 2019-2025, dominik.goeddeke@mathematik.uni-stuttgart.de



#######################################################
# imports
#######################################################

import matplotlib.pyplot as plt    # for plotting
import numpy as np                 # for linear algebra
from scipy.integrate import fixed_quad # for Gauss-Legendre quadrature

#######################################################

def tscheby_roots(a,b,n) :
  # computes roots of Tschebyschow polynomials
  zeros = np.zeros(n+1)
  kk = np.arange(n+1)
  zeros = np.cos( np.pi * (2*kk+1)/(2*n+2) )
  zeros = 0.5*(a+zeros*(b-a)+b)   # extend from [-1,1] to arbitrary [a,b]
  return zeros

#######################################################

def lagrange_basispoly(x,i,n,stuetz) :
  # evaluates the i-th lagrange basis polynomial in x for n+1 equidistant points in [0,1]
  p = 1.
  for j in range(0,n+1,1) :
    if j != i :
      p = p * (x-stuetz[j]) / (stuetz[i]-stuetz[j])
  return p

#######################################################

def newton_basispoly(x,i,n,x_points) :
  # evaluates the i-th Newton basis polynomial in x for interpolation points x_points
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

def plot_lagrangebasis_tscheby() :
  xx = np.linspace(0,1,1001)
  for n in np.array([5,10,15,20]) :
    for i in range(0,n+1,1) :
      stuetz = tscheby_roots(0,1,n)
      yy = lagrange_basispoly(xx,i,n,stuetz)
      plt.plot(xx,yy,linestyle='-', linewidth=2)
    plt.savefig('lagrange_basispolynome_tschebystuetz_n' + str(n) + '.pdf')
    plt.close()  

#######################################################

def table_newtonpolys_tscheby() :
  for n in np.array([5,10,15,20,25,30]) :
    # compute Newton infty poly norms by naive sampling -- not accurate but easy
    a = -1
    b = 1
    xx = np.linspace(a,b,1001)
    x_points = tscheby_roots(a,b,n)
    m1 = np.max(np.abs(newton_basispoly(xx,n+1,n+1,x_points)))
    a = -5
    b = 5
    xx = np.linspace(a,b,1001)
    x_points = tscheby_roots(a,b,n)
    m2 = np.max(np.abs(newton_basispoly(xx,n+1,n+1,x_points)))
    print(f'{n:2} {m1:6.4e} {m2:6.4e}')

#######################################################

def table_lebesgueconstants_tscheby() :
  for n in np.array([5,10,15,20]) :
    a = 0
    b = 1
    xx = np.linspace(a,b,1001)
    x_points = tscheby_roots(a,b,n)
    sum = np.zeros(len(xx)) 
    for i in range(0,n+1,1) :
      sum = sum + np.abs(lagrange_basispoly(xx,i,n,x_points))
    m = np.max(sum)  
    print(f'{n:2} {m:6.4e}')

#######################################################

def f1(x) :
  return np.sin(2*np.pi*x)

def f2(x) :
  return 1./ (1+x*x)

def f3(x) :
  return np.abs(x)

#######################################################

def plot_sineexample_tscheby() :
  for n in np.array([4,8,16]) :
    a = 0
    b = 1
    xx = np.linspace(a,b,1001)
    yy = f1(xx)
    plt.plot(xx,yy,color='black', linewidth=2, linestyle='-')
    x_points = tscheby_roots(a,b,n)
    f_values = f1(x_points)
    plt.plot(x_points,f_values, color='red', marker='s', markersize=8, linestyle=' ')
    pol = np.polyfit(x_points,f_values,len(x_points)-1) 
    yy = np.polyval(pol,xx)
    plt.plot(xx, yy, color='red', linestyle='-', linewidth=2, markersize=2)
    plt.savefig('sinus' + str(n) + '_tscheby.pdf')
    plt.close()

def plot_rungeexample_tscheby() :
  for n in np.array([4,8,16]) :
    a = -5
    b = 5
    xx = np.linspace(a,b,1001)
    yy = f2(xx)
    plt.plot(xx,yy,color='black', linewidth=2, linestyle='-')
    x_points = tscheby_roots(a,b,n)
    f_values = f2(x_points)
    plt.plot(x_points,f_values, color='red', marker='s', markersize=8, linestyle=' ')
    pol = np.polyfit(x_points,f_values,len(x_points)-1) 
    yy = np.polyval(pol,xx)
    plt.plot(xx, yy, color='red', linestyle='-', linewidth=2, markersize=2)
    plt.savefig('runge' + str(n) + '_tscheby.pdf')
    plt.close()

def plot_absexample_tscheby() :
  for n in np.array([4,8,16]) :
    a = -1
    b = 1
    xx = np.linspace(a,b,1001)
    yy = f3(xx)
    plt.plot(xx,yy,color='black', linewidth=2, linestyle='-')
    x_points = tscheby_roots(a,b,n)
    f_values = f3(x_points)
    plt.plot(x_points,f_values, color='red', marker='s', markersize=8, linestyle=' ')
    pol = np.polyfit(x_points,f_values,len(x_points)-1) 
    yy = np.polyval(pol,xx)
    plt.plot(xx, yy, color='red', linestyle='-', linewidth=2, markersize=2)
    plt.savefig('abs' + str(n) + '_tscheby.pdf')
    plt.close()

#######################################################

def table_interperrors_tscheby() :
  for n in np.array([0,4,8,16,32]) :
    xx_sine = np.linspace(0,1,1001)
    func_sine = f1(xx_sine)
    x_points_sine = tscheby_roots(0,1,n)
    f_values_sine = f1(x_points_sine)
    pol = np.polyfit(x_points_sine,f_values_sine,len(x_points_sine)-1) 
    interp = np.polyval(pol,xx_sine)
    error_sine = np.max(np.abs(func_sine - interp))
    
    xx_runge = np.linspace(-5,5,1001)
    func_runge = f2(xx_runge)
    x_points_runge = tscheby_roots(-5,5,n)
    f_values_runge = f2(x_points_runge)
    pol = np.polyfit(x_points_runge,f_values_runge,len(x_points_runge)-1) 
    interp = np.polyval(pol,xx_runge)
    error_runge = np.max(np.abs(func_runge - interp))

    xx_abs = np.linspace(-1,1,1001)
    func_abs = f3(xx_abs)
    x_points_abs = tscheby_roots(-1,1,n)
    f_values_abs = f3(x_points_abs)
    pol = np.polyfit(x_points_abs,f_values_abs,len(x_points_abs)-1) 
    interp = np.polyval(pol,xx_abs)
    error_abs = np.max(np.abs(func_abs - interp))

    print(f'{n:2} {error_sine:6.4e} {error_runge:6.4e} {error_abs:6.4e}') 

#######################################################

def pk(x,k) :
  return (k+1) * x**k

def intpk(k,a,b) :
  return b**(k+1) - a**(k+1)

def table_exact_polynomials_gauss() :
  a = 0
  b = 1
  for k in range(0,11,1) :   # loop over polynomial degree
    s = ''
    s = s + f'{k}' + '\t'
    s = s + f'{2*k+1}' + '\t'
    for n in range(1,5,1) :  # loop over integration order
      quadres, none = fixed_quad(pk,a,b,n=n+1,args=[k])  # Gaussian integration
      exres = intpk(k,a,b)  # exact integration, computed a priori with pen and paper
      err = np.abs(quadres-exres)
      s = s + f'{err:6.6f}' + '\t'
    print(s)

    
#######################################################    

#plot_lagrangebasis_tscheby()
#table_newtonpolys_tscheby()
#table_lebesgueconstants_tscheby()
#plot_sineexample_tscheby()
#plot_rungeexample_tscheby()
#plot_absexample_tscheby()
#table_interperrors_tscheby()

table_exact_polynomials_gauss()
