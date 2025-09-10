# Demo codes to perform all numerical experiments in chapter 5 of my lecture notes
# "Numerische Mathematik 1".
#
# Tested on the Linux console with Python 3.12.6 and NumPy 2.1.1,
# but any recent Python, NumPy and MatPlotLib should do the trick.
#
# (c) 2019-2024, dominik.goeddeke@mathematik.uni-stuttgart.de


#######################################################
# imports
#######################################################

import matplotlib.pyplot as plt          # for plotting
import numpy as np                       # for linear algebra
from scipy.integrate import newton_cotes # for lazy-ass Newton-Cotes weights

#######################################################
# table 5.4
#######################################################

def pk(x,k) :
  return (k+1) * x**k

def intpk(k,a,b) :
  return b**(k+1) - a**(k+1)

def table_exact_polynomials_closed_newton_cotes() :
  a = 0 # note that for any other interval, the weights trafo must be adapted
  b = 1 # and that it is bad to hard-code such assumptions below
  for k in range(0,10,1) :
    s = ''
    for n in range(1,7,1) :
      # quadrature points: equidistant 
      stuetz = np.arange(a,n+1,b) / n
      # weights are just looked up from some database in numpy
      weights = np.array(newton_cotes(n,equal=1)[0])
      # see scipy.integrate docs: weights are on [0,n], not [0,1]
      # so apply trafo formula from the lecture
      # you might want to think for a minute why the next line actually implements 
      # the trafo formula (theorem 6.5)
      weights = weights / n  
      #print(stuetz)
      #print(weights)
      # now that all is done, just do numerical quadrature and error calculation
      # and tabulate the results
      quadres = 0  # result of quadrature
      for i in range(a,n+1,b) :
        quadres = quadres + weights[i]*pk(stuetz[i],k)
      exres = intpk(k,a,b)  # exact integration, computed a priori with pen and paper
      err = np.abs(quadres-exres)
      s = s + f'{err:6.6f}' + '\t'
    print(s)


def table_exact_polynomials_open_newton_cotes() :
  # same as above, just with open Newton-Cotes formulae.
  # unfortunately, there is no numpy/scipy database of the weights, so we have to 
  # copy them from the lecture
  weights = np.array([ [1], [1/2,1/2], [2/3, -1/3, 2/3], [11/24,1/24,1/24,11/24], [11/20, -14/20, 26/20, -14/20,11/20] ])
  for k in range(0,6,1) :
    s = ''
    for n in range(0,5,1) :
      stuetz = np.zeros(n+1)
      for i in range(0,n+1,1) :
        stuetz[i] = (i+1)/(n+2) 
      #print(stuetz)
      #print(weights[n])
      quadres = 0  # result of quadrature
      for i in range(0,n+1,1) :
        quadres = quadres + weights[n][i]*pk(stuetz[i],k)
        exres = intpk(k,0,1)  # exact integration
        err = np.abs(quadres-exres)
      s = s + f'{err:6.6f}' + '\t'
    print(s)

#######################################################
# figure 5.8
#######################################################

def f(x,n) :
  return 0.5 * (2*n+1) * np.pi * np.sin( (2*n+1)*np.pi*x )

def plot_oscillation_example() :
  xx = np.linspace(0,1,1001)
  for n in [0,1,2,3,4] :
    yy = f(xx,n) 
    plt.plot(xx, yy, linestyle='-', linewidth=2, label='n='+str(n))
  plt.legend(loc='lower right')
  plt.savefig('kondition_oszi_beispiel.pdf')
  plt.close()


#######################################################
# actual scripting area

#table_exact_polynomials_closed_newton_cotes()
table_exact_polynomials_open_newton_cotes()

#plot_oscillation_example()

