# Demo codes to perform all numerical experiments in chapter 1 of my lecture notes 
# "Numerische Mathematik 1". 
#
# Tested on the Linux console with Python 3.12.6 and NumPy 2.1.1,
# but any recent Python, NumPy and MatPlotLib should do the trick.
#
# (c) 2019-2024, dominik.goeddeke@mathematik.uni-stuttgart.de

import numpy as np 


# print out some limits
print(f'numpy version: {np.version.version}')
print(f'machine epsilon in double precision: {np.finfo(float).eps}') 
print(f'machine epsilon in single precision: {np.finfo(np.float32).eps}')

# see lecture notes for details, Chapter 1.2 
print('solve original problem in double precision')
A = np.array([ [1.2969, 0.8648], [0.2161, 0.1441] ]) 
b = np.array([0.8642, 0.1440])  
x = np.linalg.solve(A, b)
print(f'solution vector: {x}')
# check if solution is accurate by computing Ax-b and comparing against 10*machine_eps
if np.linalg.norm(A.dot(x)-b,np.inf)<10*np.finfo(float).eps :
  print('Solution is accurate enough')
else :
  print('Solution is inaccurate')
print()


print('solve modified problem in double precision')
A = np.array([ [1.2969, 0.8648], [0.2161, 0.1441] ]) 
b = np.array([0.86419999, 0.14400001])  
x = np.linalg.solve(A, b)
print(f'solution vector: {x}')
if np.linalg.norm(A.dot(x)-b,np.inf)<10*np.finfo(float).eps :
  print('Solution is accurate enough')
else :
  print('Solution is inaccurate')
print()


print('solve original problem in single precision')
A = np.array([ [1.2969, 0.8648], [0.2161, 0.1441] ]) 
b = np.array([0.8642, 0.1440])  
As = A.astype(np.float32) 
bs = b.astype(np.float32)
xs = np.linalg.solve(As,bs)
print(f'solution vector: {xs}')
# check if solution is accurate by computing Ax-b and comparing against 10*machine_eps
if np.linalg.norm(As.dot(xs)-bs,np.inf)<10*np.finfo(float).eps :
  print('Solution is accurate enough')
else :
  print('Solution is inaccurate')
print()


# see lecture notes, section 1.4.2 
print('compute condition numbers')
A = np.array([ [1.2969, 0.8648], [0.2161, 0.1441] ])
normA = np.linalg.norm(A,np.inf)
print(f'||A||_oo    = {normA:.4f}')
normAinv = np.linalg.norm(np.linalg.inv(A),np.inf)
print(f'||A^-1||_oo = {normAinv}')
print(f'cond_oo(A)  = {normA*normAinv}')
b = np.array([0.8642, 0.1440])
normdeltab = 10**(-8)
normb = np.linalg.norm(b,np.inf)
print(f'||deltab||_oo / ||b||_oo = {normdeltab/normb}')
print(f'perturbation theorem bound: {normA*normAinv*(normdeltab/normb)}')
print()


# see lecture notes, section 1.5.2
print('Toying with floating point')
a64 = np.float64(1.0)
b64 = np.float64(1e-8)
c64 = np.float64(0.9998)
d64 = np.float64(1.0002)
e64 = np.float64(1e8)
a32 = np.float32(1.00000000)
b32 = np.float32(1e-8)
c32 = np.float32(0.9998)
d32 = np.float32(1.0002)
e32 = np.float32(1e8)
  
ab64 = a64+b64
cd64 = c64*d64
ab32 = a32+b32
cd32 = c32*d32
  
print(f'double: {a64:.8f} + {b64:.8f} = {ab64:.8f}')
print(f'float : {a32:.8f} + {b32:.8f} = {ab32:.8f}')
print(f'double: {c64:.4f} * {d64:.4f} = {cd64:.8f}')
print(f'float : {c32:.4f} * {d32:.4f} = {cd32:.8f}')
print(f'double: ({ab64:.8f} - {a64:.8f})*10^8 = {(ab64-a64)*e64:.8f}')
print(f'float : ({ab32:.8f} - {a32:.8f})*10^8 = {(ab32-a32)*e32:.8f}')
print(f'double: ({cd64:.8f} - {a64:.8f})*10^8 = {(cd64-a64)*e64:.8f}')
print(f'float : ({cd32:.8f} - {a32:.8f})*10^8 = {(cd32-a32)*e32:.8f}')
print(f'double: ({a64:.8f} - {a64:.8f} + {b64:.8f})*10^8 = {(a64-a64+b64)*e64:.8f}')
print(f'float : ({a32:.8f} - {a32:.8f} + {b32:.8f})*10^8 = {(a32-a32+b32)*e32:.8f}')







