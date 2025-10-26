# =============================================================================
# This script computes 2-D fields of heads and
# stream function values, constructs streamline-oriented grids,
# computes steady-state concentrations, and concentrations of
# reactive compounds undergoing an instantaneous reaction
#
# written by 
#
# Olaf A. Cirpka
#
# University of Tuebingen
# Department of Geosciences
# Schnarrenbergstr. 94-96
# 72076 Tuebingen
# Germany
# olaf.cirpka@uni-tuebingen.de
#
# Matlab Code: September 19, 2013
# transferred to python: April 2025
# =============================================================================

# clear all variables
from IPython import get_ipython
get_ipython().run_line_magic('reset', '-sf')
# clear console
import os
os.system('cls' if os.name == 'nt' else 'clear')

import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse.linalg import spsolve #, bicgstab, spilu, LinearOperator,                                
# import pyamg # installation of pyamg: pip install pyamg
import time
# import warnings
from fullscreenfigure import fullscreenfigure
import gw_FEM as gw
from streamlinegrid import slgrid, mob_mat

# number of elements per direction (x,y)
nx = [200, 100]
# grid spacing
dx = [0.05, 0.0125]
# hydraulic conductivity of the matrix
K1 = 1e-4
# hydraulic conductivity of the inclusion
K2 = 1e-3
# head difference
phiin = nx[0]*dx[0]*0.01

# transport parameters
poros = 0.3     # porosity [-]
al    = 0.01    # longitudinal dispersivity [m]
at    = 0.001   # transverse dispersivity [m]
Dm    = 1e-9    # molecular diffusion coefficient [m]

# dimensions of the streamline-oriented grid
ntube = 100
nsec  = 200
nnet  = ntube*nsec

# nodal coordinates
X = np.arange(nx[0]+1)*dx[0]
Y = np.arange(nx[1]+1)*dx[1]
(X,Y)=np.meshgrid(X,Y)
# number of nodes
nnod = (nx[0]+1)*(nx[1]+1)

# -----------------------------------------------------------------------------
# generate conductivity field
# -----------------------------------------------------------------------------
K = np.ones((nx[1],nx[0]))*K1
K[np.floor(nx[1]*.4).astype(int):np.floor(nx[1]*.6+1).astype(int), \
  np.floor(nx[0]*.3).astype(int):np.floor(nx[0]*.7+1).astype(int)] = K2

# -----------------------------------------------------------------------------
# groundwater flow
# -----------------------------------------------------------------------------
tic = time.time()
print("Groundwater Flow")
# set up system of equations for groundwater flow
print("Set up System of Equations")
M = gw.mat(K,dx[0],dx[1])

# Account for fixed-head boundary conditions
print("Account for Fixed-Head Boundary Conditions")
leftnodes  = np.arange(nx[1]+1)*(nx[0]+1)
rightnodes = leftnodes + nx[0]
r = np.zeros(nnod)
Mmod, rmod = gw.diri(M,r,leftnodes,phiin*np.ones((nx[1]+1,1)))
Mmod, rmod = gw.diri(Mmod,rmod,rightnodes,np.zeros((nx[1]+1,1)))
# Preconditioner
# print("Preconditioning of the System of Equations")
# ILU preconditioning (if pyamg is not available)
# ilu = spilu(Mmod)
# Mmod2 = LinearOperator(Mmod.shape, ilu.solve)
# AMG preconditioning (requires pyamg)
# with warnings.catch_warnings():
#      warnings.simplefilter("ignore")
#      ml = pyamg.ruge_stuben_solver(Mmod)
#      Mmod2 = ml.aspreconditioner()
# solve groundwater-flow equation
# h0=(1-np.reshape(X,(nnod,1))/dx[0]/nx[0])*phiin
print("Solve System of Equations")
# h, info = bicgstab(Mmod, np.array(rmod)[:,None],rtol=1e-8,atol=1e-12,M=Mmod2,x0=h0)
h = spsolve(Mmod, np.array(rmod)[:,None], use_umfpack=True)


# evaluate total flux
Qin = sum(M[leftnodes,:]@h)

# -----------------------------------------------------------------------------
# stream function
# -----------------------------------------------------------------------------
print("Stream Function")
# set up system of equations for stream-function equation
print("Set up System of Equations")
M = gw.mat(K**-1,dx[0],dx[1])

# Dirichlet boundary conditions
print("Account for Fixed-Value Boundary Conditions")
botnodes = np.arange(nx[0]+1)
topnodes = botnodes + nx[1]*(nx[0]+1)
r = np.zeros(nnod)
Mmod, rmod = gw.diri(M,r,botnodes,np.zeros((nx[0]+1,1)))
Mmod, rmod = gw.diri(Mmod,rmod,topnodes,Qin*np.ones((nx[0]+1,1)))
# Preconditioner
# print("Preconditioning of the System of Equations")
# ILU preconditioning (if pyamg is not available)
# ilu = spilu(Mmod)
# Mmod2 = LinearOperator(Mmod.shape, ilu.solve)
# AMG preconditioning (requires pyamg)
# with warnings.catch_warnings():
#      warnings.simplefilter("ignore")
#      ml = pyamg.ruge_stuben_solver(Mmod)
#      Mmod2 = ml.aspreconditioner()
print("Solve System of Equations")
psi0=(1-np.reshape(Y,(nnod,1))/dx[1]/nx[1])
# psi, info = bicgstab(Mmod, np.array(rmod)[:,None],rtol=1e-8,atol=1e-16,M=Mmod2,x0=psi0)
psi = spsolve(Mmod, np.array(rmod)[:,None], use_umfpack=True)

toc = time.time()
print(f"Elapsed time for head and stream-function calculation: {toc - tic:.4f} seconds")
tic = toc

psi = np.reshape(psi,(nx[1]+1,nx[0]+1))
h   = np.reshape(h,(nx[1]+1,nx[0]+1))

# -----------------------------------------------------------------------------
# streamline-oriented grid generation
# -----------------------------------------------------------------------------
print("Streamline-Oriented Grid Generation")
net = slgrid(ntube, nsec, nx, dx, psi, h, phiin, Qin)
toc = time.time()
print(f"Elapsed time for grid generation: {toc - tic:.4f} seconds")
tic = toc

# -----------------------------------------------------------------------------
# Preparation of Transport Calculations
# -----------------------------------------------------------------------------
print("Prepare Matrices for Transport Calculations")
# calculate matrices to solve for ADE on streamline-oriented grid
Mmob   = mob_mat(net, al, at, Dm, poros, 1) # mobility matrix

# -----------------------------------------------------------------------------
# Compute Mixing Ratio
# -----------------------------------------------------------------------------

# first column of cells
firstcol = list(range(0,nsec*ntube,nsec))

# specific discharge per stream tube
invec = np.zeros(nnet)
invec[0:nsec*ntube:nsec]=Qin/ntube

# inflow marker
is_in = np.zeros(((ntube,nsec)))
is_in[np.floor(ntube/2).astype(int)+np.arange(-15,15).astype(int),0] = 1
is_in=is_in.reshape(nnet)
rhs=invec*is_in

print('Solve for Mixing Ratio')
# AMG preconditioner
# ml = pyamg.air_solver(Mmob,coarse_solver='splu')
# Mmob2 = ml.aspreconditioner()
# ilu = spilu(Mmob.tocsc())
# Mmob2 = LinearOperator(Mmob.shape, ilu.solve)
# mixratio, info = bicgstab(Mmob, rhs,rtol=1e-10,atol=1e-18,M=Mmob2)
mixratio = spsolve(Mmob, rhs, use_umfpack=True)
mixratio = mixratio.reshape((ntube,nsec))
toc = time.time()
print(f"Elapsed time for calculation of mixing ratios: {toc - tic:.4f} seconds")
tic = toc


# -----------------------------------------------------------------------------
# Analyze mixing ratio
# -----------------------------------------------------------------------------
# center point of all cella
ycen=0.25*(net.y[:-1,:-1]+net.y[1:,:-1]+net.y[:-1,1:]+net.y[1:,1:])
# width
delta_y_net=0.5*(net.y[1:,:-1]-net.y[:-1,:-1] + 
                 net.y[1:,1: ]-net.y[:-1,1: ])
# stream-function value in the center
psicen=np.outer(np.arange(.5,ntube),np.ones(nsec))*Qin/ntube

# normal transverse moments
m0 =np.sum(mixratio*delta_y_net,axis=0)
m1 =np.sum(mixratio*ycen*delta_y_net,axis=0)/m0
m2c=np.sum(mixratio*(ycen-np.outer(np.ones(ntube),m1))**2*delta_y_net,axis=0)/m0
# flux-weighted transverse moments
m0psi =np.sum(mixratio,axis=0)*Qin/ntube
m1psi =np.sum(mixratio*psicen,axis=0)/m0psi*Qin/ntube
m2cpsi=np.sum(mixratio*(psicen-np.outer(np.ones(ntube),m1psi))**2,axis=0)/m0psi*Qin/ntube
# flux related dilution index
pQ     = mixratio/(np.outer(np.ones(ntube),np.mean(mixratio,axis=0))*Qin)
pQlnpQ = pQ*np.log(pQ)
pQlnpQ[pQ<1e-30]=0
dilind = np.exp(-Qin*np.mean(pQlnpQ,axis=0))

# -----------------------------------------------------------------------------
# Compute reactive-species concentrations by postprocessing
# -----------------------------------------------------------------------------
# compute concentrations for the limiting case of an instantaneous reaction
# assumption 1:1:1 stoichiometry, inflow concentrations are unity
c1inst=2*mixratio-1
c1inst[c1inst<0]=0

c2inst=1-2*mixratio
c2inst[c2inst<0]=0

c3inst=mixratio-c1inst

# -----------------------------------------------------------------------------
# Plots
# -----------------------------------------------------------------------------
# plot conductivity field
fig1 = fullscreenfigure(1)
ax1  = plt.subplot(3,1,1)
pc   = ax1.pcolormesh(X, Y, np.log10(K), shading='flat', cmap='jet')
ax1.set_aspect(aspect=1.0)
plt.colorbar(pc, label='log$_{10}$K [K in m/s]')
ax1.set_xlabel('x [m]')
ax1.set_ylabel('y [m]')
ax1.set_title('Log-Conductivity Field')
# plot flownet
ax2 = plt.subplot(3,1,2)
ax2.contour(X,Y,psi,50,colors='k')
co  = ax2.contour(X,Y,h,50,cmap='jet')
ax2.set_aspect(aspect=1.0)
cb2 = plt.colorbar(co, label='h [m]')
ax2.set_xlabel('x [m]')
ax2.set_ylabel('y [m]')
ax2.set_title('Flownet')
# plot mixing ratio
ax3 = plt.subplot(3,1,3)
Xplot=ax3.pcolormesh(net.x, net.y, mixratio, shading='flat', cmap='jet')
plt.colorbar(Xplot)
ax3.set_aspect(aspect=1.0)
ax3.set_xlabel('x [m]')
ax3.set_ylabel('y [m]')
ax3.set_title('Mixing Ratio')
ax3.set_xlim(0,nx[0]*dx[0])
ax3.set_ylim(0,nx[1]*dx[1])

# plot moments and metrics of mixing
fig2 = fullscreenfigure(2)
philine = 0.5*(net.phi[0,1:]+net.phi[0,:-1])

ax1 = plt.subplot(3,1,1)
line1, = ax1.plot(philine,m1,label='center position')
ax1.set_xlabel('h [m]')
ax1.set_ylabel('y$_{cen}$ [m]')
ax1.set_xlim(0,phiin)
ax1.set_title('Transverse Spatial Moments of Mixing Ratio')
ax1.invert_xaxis()
ax2 = ax1.twinx()
line2, = ax2.plot(philine,np.sqrt(m2c),'r',label='spread')
ax2.set_ylabel('w$_y$ [m]')
lines = [line1, line2]
labels = [line.get_label() for line in lines]
plt.legend(lines,labels)

ax1 = plt.subplot(3,1,2)
line1, = ax1.plot(philine,m1psi,label='center position')
ax1.set_xlim(0,phiin)
ax1.set_xlabel('h [m]')
ax1.set_ylabel('$\psi_{cen}$ [m$^2$/s]')
ax1.set_title('Flux-Related Transverse Spatial Moments of Mixing Ratio')
ax1.invert_xaxis()
ax2 = ax1.twinx()
line2, = ax2.plot(philine,np.sqrt(m2cpsi),'r',label='spread')
ax2.set_ylabel('w$_\psi$ [m$^2$/s]')
lines = [line1, line2]
labels = [line.get_label() for line in lines]
plt.legend(lines,labels)

ax1 = plt.subplot(3,1,3)
line1, = ax1.plot(philine,np.sqrt(m2cpsi),label='spread based on moments')
ax1.set_xlim(0,phiin)
ax1.set_xlabel('h [m]')
ax1.set_ylabel('w$_\psi$ [m$^2$/s]')
ax1.set_title('Flux-Related Measure of Plume Width')
ax1.invert_xaxis()
ax2 = ax1.twinx()
line2, = ax2.plot(philine,dilind,'r',label='dilution index')
ax2.set_ylabel('E$_Q$ [m$^2$/s]')
lines = [line1, line2]
labels = [line.get_label() for line in lines]
plt.legend(lines,labels)

# plot concentrations of reactive species
fig3 = fullscreenfigure(3)
ax1  = plt.subplot(3,1,1)
pc   = ax1.pcolormesh(net.x, net.y, c1inst, shading='flat', cmap='jet')
ax1.set_aspect(aspect=1.0)
plt.colorbar(pc)
ax1.set_xlabel('x [m]')
ax1.set_ylabel('y [m]')
ax1.set_title('Reactant A')
ax2  = plt.subplot(3,1,2)
pc   = ax2.pcolormesh(net.x, net.y, c2inst, shading='flat', cmap='jet')
ax2.set_aspect(aspect=1.0)
plt.colorbar(pc)
ax2.set_xlabel('x [m]')
ax2.set_ylabel('y [m]')
ax2.set_title('Reactant B')
ax3  = plt.subplot(3,1,3)
pc   = ax3.pcolormesh(net.x, net.y, c3inst, shading='flat', cmap='jet')
ax3.set_aspect(aspect=1.0)
plt.colorbar(pc)
ax3.set_xlabel('x [m]')
ax3.set_ylabel('y [m]')
ax3.set_title('Product C')

# plot mass flux of product and dilution index
fig2 = fullscreenfigure(4)
ax1 = plt.subplot(1,1,1)
line1, = ax1.plot(philine,dilind,label='dilution index')
ax1.set_xlim(0,phiin)
ax1.set_xlabel('h [m]')
ax1.set_ylabel('E$_Q$ [m$^2$/s]')
ax1.set_title('Dilution Index and Total Mass Flux of Product')
ax1.invert_xaxis()
ax2 = ax1.twinx()
line2, = ax2.plot(philine,np.mean(c3inst,axis=0)*Qin,'r',label='mass flux of product')
ax2.set_ylabel('F$_C$ [conc. $\times$$m^2$/s]')
lines = [line1, line2]
labels = [line.get_label() for line in lines]
plt.legend(lines,labels)

plt.show(block=True)

