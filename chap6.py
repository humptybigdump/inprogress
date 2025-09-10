# Demo codes to perform all numerical experiments in chapter 6 of my lecture notes
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
from scipy.integrate import quad   # for integration


#######################################################
# numerical example at the end of chapter 6.1 (linear least-squares regression)
# nothing spectacular, except for the self-cooked errorbar plotter, because
# I could not get that running with standard matplotlib
#######################################################

def p(c,x) :
  return c[0] + c[1]*x

def least_squares() :
  x = np.array([ 0, 1, 2, 3 ])
  A = np.array([ [1,0], [1,1], [1,2],[1,3] ])
  f = np.array([ 0, 10, 10, 20 ])
  ATA = np.transpose(A).dot(A)
  y = np.transpose(A).dot(f)
  c = np.linalg.solve(ATA, y)

  plt.plot(x,f, color='red', marker='s', markersize=8, linestyle=' ')
  xx = np.linspace(0,3,1001)
  cc = p(c,xx)
  plt.plot(xx,cc, color='blue', linewidth=2, linestyle='-')
  errorbars_min = np.zeros(len(x))
  errorbars_max = np.zeros(len(x))
  for i in range(len(x)) :
    errorbars_min[i] = min(f[i],p(c,x[i]))
    errorbars_max[i] = max(f[i],p(c,x[i]))
  plt.vlines(x,errorbars_min,errorbars_max,color='red', linewidth=1)
  
  
  plt.savefig('leastsquares_example.pdf')
  plt.close()

#######################################################
# table 6.4, condition numbers of the "quasi-Hilbert-Matrix"
#######################################################

def assemble_matrix(n) :
  A = np.zeros((n,n), dtype=np.float64)
  for i in range(0,n,1) :
    for j in range(0,n,1) :
      if ((i+j)%2) == 0 :
        A[i,j] = 2/(i+j+1)  
  return A
  
def table_cond_gausaaprox_monom() :
  for n in np.array([5,10,15,20]) :
    A = assemble_matrix(n)
    print(f'{n:2} {np.linalg.cond(A,1):6.4e} {np.linalg.cond(A,2):6.4e} {np.linalg.cond(A,np.inf):6.4e}')

#######################################################
# demo functions for Figure 6.6
#######################################################

def testfunc(func,xi) :
  if func==1 :
    return np.sin(np.pi*xi)
  elif func==2 :
    return 1./ (1+25*xi**2)
  elif func==3 :
    return np.abs(xi)
  else :
    print('Doofmann')
    
#######################################################
# evaluation of the Legendre basis ponynomials, straight formula from Def. 6.24
# Warning: x must be a scalar
#######################################################

def legendre_proto(k,x) :   # non-normalised Legendre basis polynomials
  if k==0 :
    return 1
  elif k==1 :
    return x
  else :
    return x*legendre_proto(k-1,x) - (k-1)**2 / (4*(k-1)**2 - 1)  *legendre_proto(k-2,x)

def legendre(k,x) :     # normalised Legendre basis polynomials
  return ((np.math.factorial(2*k)) / (2**k * (np.math.factorial(k)**2))) * legendre_proto(k,x)

#######################################################
# Figure 6.5
# Nothing spectacular, except that I am too stupid to vectorise the basis functions,
# so I had to use the wacky vectorize routine from NumPy for it.
#######################################################

def plot_legendrebasis() :
  xx = np.linspace(-1,1,1001)
  legendre_vec = np.vectorize(legendre)
  yy = legendre_vec(0,xx)
  plt.plot(xx,yy, color='red', linewidth=2, linestyle='-', label='k=0')
  yy = legendre_vec(1,xx)
  plt.plot(xx,yy, color='yellow', linewidth=2, linestyle='-', label='k=1')
  yy = legendre_vec(2,xx)
  plt.plot(xx,yy, color='green', linewidth=2, linestyle='-', label='k=2')
  yy = legendre_vec(3,xx)
  plt.plot(xx,yy, color='cyan', linewidth=2, linestyle='-', label='k=3')
  yy = legendre_vec(4,xx)
  plt.plot(xx,yy, color='blue', linewidth=2, linestyle='-', label='k=4')
  yy = legendre_vec(5,xx)
  plt.plot(xx,yy, color='magenta', linewidth=2, linestyle='-', label='k=5')
  plt.legend(loc='lower right')
  plt.savefig('legendre_basispolys.pdf')
  plt.close()

#######################################################
# figure 6.6
# We use SciPy's standard integrator, which needs a function, which we define inline
#######################################################

def plot_gausslegendre_examples(func) :
  legendre_vec = np.vectorize(legendre)
  xx = np.linspace(-1,1,1001)
  ff = testfunc(func,xx)
  plt.plot(xx,ff, color='black', linewidth=2, linestyle='-', label='target')
  for n in np.array([0,2,4,8,16]) :
    result = np.zeros(len(xx))
    for i in range(0,n+1,1) :
      # compute coefficients
      def integrand1(xi) :   # probably smarter with a lambda function
        return legendre(i,xi)*legendre(i,xi)
      coeff1, err = quad(integrand1,-1,1)
      def integrand2(xi) :
        return legendre(i,xi)*testfunc(func,xi)
      coeff2,err = quad(integrand2,-1,1)
      # evaluate i-th Legendre basis function
      Li = legendre_vec(i,xx)
      result = result + (coeff2/coeff1)*Li
    plt.plot(xx,result, linewidth=2, linestyle='-', label='Gauss-Legendre (n='+str(n)+')')
  # done
  if func==1 :
    plt.legend(loc='lower right')
    plt.savefig('GaussLegendre_sinus.pdf')
  elif func==2 :
    plt.savefig('GaussLegendre_runge.pdf')
  elif func==3 :
    plt.legend(loc='upper center')
    plt.savefig('GaussLegendre_abs.pdf')
  else :
  	print('Doofmann')
    
  plt.close()
  
#######################################################
# Figure 6.7, and definition (vectorized) of the omega weight function
#######################################################

def omega(x) :
  return 1./np.sqrt(1-x**2)

def plot_gausstscheby_omega() :
  xx = np.linspace(-0.99,0.99,1001)
  yy = omega(xx)
  plt.plot(xx,yy, color='blue', linewidth=2, linestyle='-')
  plt.savefig('gausstscheby_omega.pdf')
  plt.close()

#######################################################
# Tschebyschow polynomials, straight formula from the definition 
#######################################################

def tscheby(k,x) :   # normalised Tschebyschow basis polynomials
  if k==0 :
    return 1
  elif k==1 :
    return x
  else :
    return 2*x*tscheby(k-1,x) - tscheby(k-2,x)

#######################################################
# Figure 6.8
#######################################################

def plot_tschebybasis() :
  tscheby_vec = np.vectorize(tscheby)
  xx = np.linspace(-1,1,1001)
  yy = tscheby_vec(0,xx)
  plt.plot(xx,yy, color='red', linewidth=2, linestyle='-', label='k=0')
  yy = tscheby_vec(1,xx)
  plt.plot(xx,yy, color='yellow', linewidth=2, linestyle='-', label='k=1')
  yy = tscheby_vec(2,xx)
  plt.plot(xx,yy, color='green', linewidth=2, linestyle='-', label='k=2')
  yy = tscheby_vec(3,xx)
  plt.plot(xx,yy, color='cyan', linewidth=2, linestyle='-', label='k=3')
  yy = tscheby_vec(4,xx)
  plt.plot(xx,yy, color='blue', linewidth=2, linestyle='-', label='k=4')
  yy = tscheby_vec(5,xx)
  plt.plot(xx,yy, color='magenta', linewidth=2, linestyle='-', label='k=5')
  plt.legend(loc='lower right')
  plt.savefig('tscheby_basispolys.pdf')
  plt.close()

#######################################################
# Figure 6.9, same as 6.6
#######################################################

def plot_gausstscheby_examples(func) :
  tscheby_vec = np.vectorize(tscheby)
  xx = np.linspace(-1,1,1001)
  ff = testfunc(func,xx)
  plt.plot(xx,ff, color='black', linewidth=2, linestyle='-', label='target')
  #
  for n in np.array([0,2,4,8,16]) :
    result = np.zeros(len(xx))
    for i in range(0,n+1,1) :
      Ti = tscheby_vec(i,xx)
      alpha = 0
      if i==0 :
        def integrand(xi) :
          return testfunc(func,xi)*omega(xi)
        alpha, err = quad(integrand,-1,1)
        alpha = alpha * (1./np.pi)
      else :
        def integrand(xi) :
          return testfunc(func,xi)*tscheby(i,xi)*omega(xi)
        alpha, err = quad(integrand,-1,1)
        alpha = alpha * (2./np.pi)
      result = result + alpha*Ti
    plt.plot(xx,result, linewidth=2, linestyle='-', label='Gauss-Tschebyschow (n='+str(n)+')')
  #
  if func==1 :
    plt.legend(loc='lower right')
    plt.savefig('GaussTscheby_sinus.pdf')
  elif func==2 :
    plt.savefig('GaussTscheby_runge.pdf')
  elif func==3 :
    plt.legend(loc='upper center')
    plt.savefig('GaussTscheby_abs.pdf')
  else :
  	print('Doofmann')
    
  plt.close()

#######################################################    

#least_squares()
table_cond_gausaaprox_monom()

#plot_legendrebasis()
#plot_gausslegendre_examples(1)
#plot_gausslegendre_examples(2)
#plot_gausslegendre_examples(3)

#plot_gausstscheby_omega()
#plot_tschebybasis()
#plot_gausstscheby_examples(1)
#plot_gausstscheby_examples(2)
#plot_gausstscheby_examples(3)




