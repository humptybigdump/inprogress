# =============================================================================
# This script generates random 2-D fields, computes heads and
# stream function values, constructs streamline-oriented grids,
# computes transient concentrations for a step-input inflow condition, 
# and evaluates breakthrough curves for all stream tubes
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
# Matlab Code: September 19, 2013; updated October 4, 2019
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
from scipy.sparse.linalg import spilu, LinearOperator, bicgstab
import pyamg # installation of pyamg: pip install pyamg
import time
from types import SimpleNamespace
from datetime import datetime

from fullscreenfigure import fullscreenfigure
from randomK import randomK
import gw_FEM as gw
from streamlinegrid import slgrid, store_mat, mob_mat, quad_cell_areas

# number of elements per direction (x,y)
nx = [500, 250]
# grid spacing
dx = [0.01, 0.01]
# correlation lengths
lx = [.5, .1]
# rotation angle
ang= 0.*np.pi/180.
# variance of ln(K)
sigY= 1.
# type of autocovariance function
Ctype = 1
# geometric mean of conductivity
Kg = 1e-4

# head difference
phiin = nx[0]*dx[0]*0.01

# transport parameters
poros = 0.3    # porosity [-]
al    = 0.01   # longitudinal dispersivity [m]
at    = 0.001  # transverse dispersivity [m]
Dm    = 1e-9   # molecular diffusion coefficient [m]
CN=1.0         # Crank-Nicolson weight for time integration
plottransient=False # flag whether transient profiles should be plotted

# dimensions of the streamline-oriented grid
ntube = 250
nsec = 500

# nodal coordinates
X = np.arange(nx[0]+1)*dx[0]
Y = np.arange(nx[1]+1)*dx[1]
(X,Y)=np.meshgrid(X,Y)
# number of nodes
nnod = (nx[0]+1)*(nx[1]+1)

# -----------------------------------------------------------------------------
# generate conductivity field
# -----------------------------------------------------------------------------
print("Generate Random Field")
K = randomK(nx, dx, lx, ang, sigY, Ctype, Kg)

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
print("Preconditioning of the System of Equations")
# ILU preconditioning (if pyamg is not available)
# ilu = spilu(Mmod)
# Mmod2 = LinearOperator(Mmod.shape, ilu.solve)
# AMG preconditioning (requires pyamg)
ml = pyamg.ruge_stuben_solver(Mmod)
Mmod2 = ml.aspreconditioner()
# solve groundwater-flow equation
h0=(1-np.reshape(X,(nnod,1))/dx[0]/nx[0])*phiin
print("Solve System of Equations")
h, info = bicgstab(Mmod, np.array(rmod)[:,None],rtol=1e-8,atol=1e-12,M=Mmod2,x0=h0)
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
print("Preconditioning of the System of Equations")
# ILU preconditioning (if pyamg is not available)
# ilu = spilu(Mmod)
# Mmod2 = LinearOperator(Mmod.shape, ilu.solve)
# AMG preconditioning (requires pyamg)
ml = pyamg.ruge_stuben_solver(Mmod)
Mmod2 = ml.aspreconditioner()
print("Solve System of Equations")
psi0=(1-np.reshape(Y,(nnod,1))/dx[1]/nx[1])
psi, info = bicgstab(Mmod, np.array(rmod)[:,None],rtol=1e-8,atol=1e-16,M=Mmod2,x0=psi0)
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

# np.savez('mydata.npz',K=K,h=h,psi=psi,Qin=Qin,xnet=net.x,ynet=net.y,
#          psinet=net.psi,phinet=net.phi)

# data = np.load('mydata.npz',allow_pickle=True)
# psi = data['psi']
# h = data['h']
# K = data['K']
# Qin = data['Qin']
# net = SimpleNamespace(
#       x=data["xnet"], y=data["ynet"],
#       phi=data["phinet"], psi=data["psinet"])

# -----------------------------------------------------------------------------
# Preparation of Transport Calculations
# -----------------------------------------------------------------------------
print("Prepare Matrices for Transport Calculations")
# water-filled area of all cells
porarea = quad_cell_areas(net.x, net.y)*poros

# calculate matrices to solve for ADE on streamline-oriented grid
Mstore = store_mat(net, poros)              # storage matrix
Mmob   = mob_mat(net, al, at, Dm, poros, 1) # mobility matrix

# -----------------------------------------------------------------------------
# Compute Mean Travel Time by Groundwater-Age Equation
# -----------------------------------------------------------------------------
print("Solve Mean Groundwater-Age Equation")
rhs=porarea.reshape((ntube*nsec,1))
# Preconditioner
ilu = spilu(Mmob)
Mmob2 = LinearOperator(Mmob.shape, ilu.solve)
# solve for first temporal moment
m1, info = bicgstab(Mmob,rhs,rtol=1e-8,atol=1e-12,M=Mmob2)
m1=m1.reshape(ntube,nsec)

toc = time.time()
print(f"Elapsed time for calculation of 1st moment: {toc - tic:.4f} seconds")

# -----------------------------------------------------------------------------
# Transient transport
# -----------------------------------------------------------------------------
# prepare transient simulation
# total time
tend  = 1.5*np.max(m1)
if CN<1:
   # determine time step size so that maximum Courant number is unity
   dt = np.min(porarea)/Qin*ntube
else:
   # determine time step size so that mean Courant number is unity
   dt = np.mean(porarea)/Qin*ntube
tvec= np.arange(dt,tend,dt)

# initialize breakthrough curve
BTC = np.zeros((ntube,len(tvec)))
lastcol = list(range(nsec-1,nsec*ntube,nsec))

# Remark: Use Crank-Nicolson for transport
# (Mstore/dt + CN*Mmob)*c_new = (Mstore/dt - (1-CN)*Mmob)*c_old + r_source
Mleft  = Mstore/dt + CN*Mmob
Mright = Mstore/dt - (1-CN)*Mmob

# initialization
c = np.zeros((ntube*nsec,1))

# specific discharge per stream tube
invec = np.zeros((ntube*nsec,1))
invec[0:nsec*ntube:nsec]=Qin/ntube

cin = np.zeros((ntube*nsec,1))
cin[0:nsec*ntube:nsec]=1.


# AMG preconditioner
ml = pyamg.air_solver(Mleft)
Mleft2 = ml.aspreconditioner()


print('Solve for Transient Concentrations')
t=0.
tdt=datetime.utcfromtimestamp(t)
tdays=0.

# initialize plot
if plottransient:
   fig2 = fullscreenfigure(2)
   ax = fig2.add_subplot()
   ax.cla()
   cplot=ax.pcolormesh(net.x, net.y, c.reshape((ntube,nsec)), 
                       shading='flat', cmap='jet', vmin=0., vmax=1.)
   plt.colorbar(cplot, label='c/c$_{in}$ [-]')
   ax.set_aspect(aspect=1.0)
   ax.set_xlabel('x [m]')
   ax.set_ylabel('y [m]')
   titext = ax.set_title(f'Transient Concentration after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
   plt.draw()
   plt.pause(0.1)
   plt.show()

# time loop
for i in range(len(tvec)):
    t = (i+1)*dt
    print(f't = {t:10.0f} s')
    BTCold=c[lastcol]
    # update right-hand side vector
    rhs=Mright @ c + np.ones((ntube*nsec,1))*invec*cin
    # solve for concentration
    c, info = bicgstab(Mleft, rhs,rtol=1e-8,atol=1e-16,M=Mleft2,x0=c)
    c = c.reshape((ntube*nsec,1))
    # breakthrough curves in the outflow
    BTC[:,i]=(1-CN)*BTCold[:,0]+CN*c[lastcol,0]
    # stop loop if breakthrough is complete
    if np.min(BTC[:,i]) > 0.999:
       tvec=tvec[:i+1]
       BTC = BTC[:,:i+1]
       break
    # update plot
    if plottransient:
       tdt=datetime.utcfromtimestamp(t)
       tdays = np.floor(t/86400)
       cplot.set_array(c.reshape((ntube,nsec)))
       titext.set_text(
 f'Transient Concentration after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
       # updated values
       fig2.canvas.draw()
       fig2.canvas.flush_events()
       plt.pause(0.1)
       plt.show()

# -----------------------------------------------------------------------------
# Travel-Time Distributions
# -----------------------------------------------------------------------------
# take derivative of BTCs to obtain travel-time pdf of each streamtube
ptau = np.zeros((ntube,len(tvec)))
ptaurel = np.zeros((ntube,len(tvec)))
trel=np.outer(m1[:,-1]**-1,tvec)
for ii in range(ntube):
    ptau[ii,:]=np.gradient(BTC[ii,:],tvec)
    ptaurel[ii,:]=np.gradient(BTC[ii,:],trel[ii,:]);

# -----------------------------------------------------------------------------
# REPLACEMENT SCENARIO  A+B > C with 1:1:1 stoichiometry
# Initial concentration of B: 1
# Injected concentration of A: 1
# -----------------------------------------------------------------------------
# Use local breakthrough curves
BTC_A=2*BTC-1
BTC_A[BTC_A<0] = 0
BTC_B=1-2*BTC
BTC_B[BTC_B<0] = 0
BTC_C=BTC-BTC_A

# use averaged BTC of mixing ratio
BTC_Am=2*np.mean(BTC,0)-1
BTC_Am[BTC_Am<0]=0
BTC_Bm=1-2*np.mean(BTC,0)
BTC_Bm[BTC_Bm<0]=0
BTC_Cm=np.mean(BTC,0)-BTC_Am


# plot conductivity field
fig1 = fullscreenfigure(1)
ax1  = plt.subplot(2,2,1)
pc   = ax1.pcolormesh(X, Y, np.log10(K), shading='flat', cmap='jet')
ax1.set_aspect(aspect=1.0)
plt.colorbar(pc, label='log$_{10}$K [K in m/s]')
ax1.set_xlabel('x [m]')
ax1.set_ylabel('y [m]')
ax1.set_title('Log-Conductivity Field')
# plot flownet
ax2 = plt.subplot(2,2,2)
ax2.contour(X,Y,psi,50,colors='k')
co  = ax2.contour(X,Y,h,50,cmap='jet')
ax2.set_aspect(aspect=1.0)
cb2 = plt.colorbar(co, label='h [m]')
ax2.set_xlabel('x [m]')
ax2.set_ylabel('y [m]')
ax2.set_title('Flownet')
# plot streamline-oriented grid
ax3 = plt.subplot(2,2,3)
ax3.plot(net.x,net.y,'k-', linewidth = 0.5)
ax3.plot(net.x.T,net.y.T,'k-',linewidth = 0.5)
ax3.set_aspect(aspect=1.0)
ax3.set_xlabel('x [m]')
ax3.set_ylabel('y [m]')
ax3.set_title('Streamline-Oriented Grid')
ax3.set_xlim(0,nx[0]*dx[0])
ax3.set_ylim(0,nx[1]*dx[1])
# plot mean groundwater age
ax4 = plt.subplot(2,2,4)
m1plot=ax4.pcolormesh(net.x, net.y, m1/86400, shading='flat', cmap='jet')
plt.colorbar(m1plot, label='\u03C4 [d]')
ax4.set_aspect(aspect=1.0)
ax4.set_xlabel('x [m]')
ax4.set_ylabel('y [m]')
ax4.set_title('Mean Groundwater Age')
ax4.set_xlim(0,nx[0]*dx[0])
ax4.set_ylim(0,nx[1]*dx[1])

# plot travel-time distributions
fig3 = fullscreenfigure(3)
plt.subplot(2,1,1)
plt.plot(np.outer(np.ones(ntube),tvec).T/86400,ptau.T*86400,'#808080', linewidth = 0.5)
plt.plot(tvec/86400,np.mean(ptau,0)*86400,'k',linewidth=4)
plt.xlabel('\u03C4 [d]')
plt.ylabel('p(\u03C4) [1/d]')
plt.title('Local Travel-Time Distributions at the Outlet Face')
plt.subplot(2,1,2)
plt.plot(trel.T,ptaurel.T,'#808080', linewidth = 0.5)
plt.xlabel('\u03C4$_{rel}$ [-]')
plt.ylabel('p(\u03C4$_{rel}$) [-]')
plt.title('Local Travel-Time Distributions Scaled by Local Mean Groundwater Age')

# plot mean and standard deviation of travel-time distribution
fig4 = fullscreenfigure(4)
plt.plot(tvec/86400,np.mean(ptau,0)*86400,label='mean of p(\u03C4)')
plt.plot(tvec/86400,np.std(ptau,0)*86400,label='std. dev. of p(\u03C4)')
plt.xlabel('\u03C4 [d]')
plt.ylabel('p(\u03C4) [1/d]')
plt.legend()
plt.title('Mean and Stndard Deviation of Local Travel-Time Distributions')

# plot concentrations of mixing-controlled reactive transport
fig5 = fullscreenfigure(5)
plt.subplot(2,1,1)
plt.plot(np.outer(np.ones(ntube),tvec).T/86400,BTC_A.T,'#76a5d2',linewidth=0.5)
plt.plot(np.outer(np.ones(ntube),tvec).T/86400,BTC_B.T,'#e88c8f',linewidth=0.5)
plt.plot(np.outer(np.ones(ntube),tvec).T/86400,BTC_C.T,'#7ac67a',linewidth=0.5)
plt.plot(tvec/86400,np.mean(BTC_A,0),'b',linewidth=4,label='A')
plt.plot(tvec/86400,np.mean(BTC_B,0),'r',linewidth=4,label='B')
plt.plot(tvec/86400,np.mean(BTC_C,0),'g',linewidth=4,label='C')
plt.xlabel('t [d]')
plt.ylabel('c$_{reac}$')
plt.legend()
plt.title('Reactive-Species Concentrations at the Outlet Face')

plt.subplot(2,1,2)
plt.plot(tvec/86400,np.mean(BTC_A,0),'b',label='correct average')
plt.plot(tvec/86400,np.mean(BTC_B,0),'r')
plt.plot(tvec/86400,np.mean(BTC_C,0),'g')
plt.plot(tvec/86400,BTC_Am,'b--',label='from average mixing ratio')
plt.plot(tvec/86400,BTC_Bm,'r--')
plt.plot(tvec/86400,BTC_Cm,'g--')
plt.xlabel('t [d]')
plt.ylabel('c$_{reac}$')
plt.legend()
plt.title('Mean Reactive-Species Concentrations at the Outlet Face')

plt.show(block=True)

