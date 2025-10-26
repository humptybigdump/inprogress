# =============================================================================
# This script generates random 2-D fields, computes heads and
# stream function values, constructs streamline-oriented grids,
# computes transient concentrations for a replacement scenario of solutions
# containing two compounds undergoing dual Michaelis-Menten kinetics
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
from scipy.sparse.linalg import spsolve #, spilu, LinearOperator, bicgstab
# import pyamg # installation of pyamg: pip install pyamg
# from types import SimpleNamespace
import time
from datetime import datetime

from fullscreenfigure import fullscreenfigure
from randomK import randomK
import gw_FEM as gw
from streamlinegrid import slgrid, store_mat, mob_mat, quad_cell_areas

# number of elements per direction (x,y)
nx = [200, 100]
# grid spacing
dx = [0.01, 0.01]
# correlation lengths
lx = [.25, .05]
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
poros = 0.3         # porosity [-]
al    = 0.01        # longitudinal dispersivity [m]
at    = 0.001       # transverse dispersivity [m]
Dm    = 1e-9        # molecular diffusion coefficient [m]
c0    = [0.,1.,0.]  # initial concentrations 
c_in  = [1.,0.,0.]  # inflow concentrations 
K_MM  = [0.1,0.1]   # Michaelis-menet coeff.
r_max = 1e-4        # maximum reaction rate [conc./s] 
CN=1.0              # Crank-Nicolson weight for time integration
plottransient=True  # flag whether transient profiles should be plotted

# dimensions of the streamline-oriented grid
ntube = 100
nsec  = 200
nnet  = ntube*nsec

# derived: maximum pseudo first-order rate-coefficient
c1m=np.max([c_in[0],c0[0]])
c2m=np.max([c_in[1],c0[1]])
lambda_max=np.max([1/K_MM[0]*c2m/(c2m+K_MM[1])*r_max,
                   1/K_MM[1]*c1m/(c1m+K_MM[0])*r_max])

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
# print("Preconditioning of the System of Equations")
# ILU preconditioning (if pyamg is not available)
# ilu = spilu(Mmod)
# Mmod2 = LinearOperator(Mmod.shape, ilu.solve)
# AMG preconditioning (requires pyamg)
# ml = pyamg.ruge_stuben_solver(Mmod)
# Mmod2 = ml.aspreconditioner()
# solve groundwater-flow equation
# h0=(1-np.reshape(X,(nnod,1))/dx[0]/nx[0])*phiin
print("Solve System of Equations")
# h, info = bicgstab(Mmod, np.array(rmod)[:,None],rtol=1e-8,atol=1e-12,M=Mmod2,x0=h0)
h = spsolve(Mmod, np.array(rmod)[:,None],use_umfpack=True)
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
# ml = pyamg.ruge_stuben_solver(Mmod)
# Mmod2 = ml.aspreconditioner()
print("Solve System of Equations")
# psi0=(1-np.reshape(Y,(nnod,1))/dx[1]/nx[1])
# psi, info = bicgstab(Mmod, np.array(rmod)[:,None],rtol=1e-8,atol=1e-16,M=Mmod2,x0=psi0)
psi = spsolve(Mmod, np.array(rmod)[:,None])
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
rhs=porarea.reshape((nnet,1))
# Preconditioner
# ilu = spilu(Mmob)
# Mmob2 = LinearOperator(Mmob.shape, ilu.solve)
# solve for first temporal moment
# m1, info = bicgstab(Mmob,rhs,rtol=1e-8,atol=1e-12,M=Mmob2)
m1 = spsolve(Mmob,rhs)
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
# make sure explicit calculation of reactions is not leading to negative
# concentrations
if 1/lambda_max<dt: dt=1/lambda_max



tvec= np.arange(dt,tend,dt)

# initialize breakthrough curves
BTC1 = np.zeros((ntube,len(tvec)))
BTC2 = np.zeros((ntube,len(tvec)))
BTC3 = np.zeros((ntube,len(tvec)))
lastcol = list(range(nsec-1,nsec*ntube,nsec))

# Remark: Use Crank-Nicolson for transport
# (Mstore/dt + CN*Mmob)*c_new = (Mstore/dt - (1-CN)*Mmob)*c_old + r_source
Mleft  = Mstore/dt + CN*Mmob
Mright = Mstore/dt - (1-CN)*Mmob

# initialization
c1 = np.ones((nnet,1))*c0[0]
c2 = np.ones((nnet,1))*c0[1]
c3 = np.ones((nnet,1))*c0[2]

# specific discharge per stream tube
invec = np.zeros((ntube*nsec,1))
invec[0:nsec*ntube:nsec]=Qin/ntube

# center point of all cella
xcen=0.25*(net.x[:-1,:-1]+net.x[1:,:-1]+net.x[:-1,1:]+net.x[1:,1:])

cin = np.zeros((ntube*nsec,1))
cin[0:nsec*ntube:nsec]=1.


# AMG preconditioner
# ml = pyamg.air_solver(Mleft)
# Mleft2 = ml.aspreconditioner()


print('Solve for Transient Concentrations')
t=0.
tdt=datetime.utcfromtimestamp(t)
tdays=0.

# initialize plot
if plottransient:
   fig2 = fullscreenfigure(2)
   # pcolor.plot of compound 1
   ax1 = plt.subplot(4,3,1)
   cplot1=ax1.pcolormesh(net.x, net.y, c1.reshape((ntube,nsec)), 
                       shading='flat', cmap='jet', vmin=0., vmax=c1m)
   plt.colorbar(cplot1)
   ax1.set_aspect(aspect=1.0)
   ax1.set_xlabel('x [m]')
   ax1.set_ylabel('y [m]')
   titext1 = ax1.set_title(f'Reactant 1 after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
   # compound 1 as function of x
   ax2 = plt.subplot(4,3,2)
   c1_of_x = plt.plot(xcen.reshape(nnet),c1,'k.',markersize=1)
   ax2.set_xlabel('x [m]')
   ax2.set_ylabel('c [conc.]')
   ax2.set_title('Reactant 1 as Function of Distance')
   ax2.set_xlim(0,nx[0]*dx[0])
   ax2.set_ylim(0,c1m)
   # compound 1 as function of travel time
   ax3 = plt.subplot(4,3,3)
   c1_of_tau = plt.plot(m1.reshape(nnet)/86400,c1,'k.',markersize=1)
   ax3.set_xlabel('\u03C4 [d]')
   ax3.set_ylabel('c [conc.]')
   ax3.set_title('Reactant 1 as Function of Mean Travel Time')
   ax3.set_xlim(0,np.max(m1.reshape(nnet))/86400)
   ax3.set_ylim(0,c1m)
   # pcolor.plot of compound 2
   ax4 = plt.subplot(4,3,4)
   cplot2=ax4.pcolormesh(net.x, net.y, c2.reshape((ntube,nsec)), 
                       shading='flat', cmap='jet', vmin=0., vmax=c2m)
   plt.colorbar(cplot2)
   ax4.set_aspect(aspect=1.0)
   ax4.set_xlabel('x [m]')
   ax4.set_ylabel('y [m]')
   titext2 = ax4.set_title(f'Reactant 2 after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
   # compound 2 as function of x
   ax5 = plt.subplot(4,3,5)
   c2_of_x = plt.plot(xcen.reshape(nnet),c2,'k.',markersize=1)
   ax5.set_xlabel('x [m]')
   ax5.set_ylabel('c [conc.]')
   ax5.set_title('Reactant 1 as Function of Distance')
   ax5.set_xlim(0,nx[0]*dx[0])
   ax5.set_ylim(0,c2m)
   # compound 2 as function of travel time
   ax6 = plt.subplot(4,3,6)
   c2_of_tau = plt.plot(m1.reshape(nnet)/86400,c2,'k.',markersize=1)
   ax6.set_xlabel('\u03C4 [d]')
   ax6.set_ylabel('c [conc.]')
   ax6.set_title('Reactant 2 as Function of Mean Travel Time')
   ax6.set_xlim(0,np.max(m1.reshape(nnet))/86400)
   ax6.set_ylim(0,c2m)
   # pcolor.plot of compound 3
   ax7 = plt.subplot(4,3,7)
   cplot3=ax7.pcolormesh(net.x, net.y, c3.reshape((ntube,nsec)), 
                       shading='flat', cmap='jet', vmin=0., 
                       vmax=np.min([c1m,c2m])*0.5)
   plt.colorbar(cplot3)
   ax7.set_aspect(aspect=1.0)
   ax7.set_xlabel('x [m]')
   ax7.set_ylabel('y [m]')
   titext3 = ax7.set_title(f'Product after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
   # compound 3 as function of x
   ax8 = plt.subplot(4,3,8)
   c3_of_x = plt.plot(xcen.reshape(nnet),c3,'k.',markersize=1)
   ax8.set_xlabel('x [m]')
   ax8.set_ylabel('c [conc.]')
   ax8.set_title('Reactant 1 as Function of Distance')
   ax8.set_xlim(0,nx[0]*dx[0])
   ax8.set_ylim(0,0.5*np.min([c1m,c2m]))
   # compound 3 as function of travel time
   ax9 = plt.subplot(4,3,9)
   c3_of_tau = plt.plot(m1.reshape(nnet)/86400,c3,'k.',markersize=1)
   ax9.set_xlabel('\u03C4 [d]')
   ax9.set_ylabel('c [conc.]')
   ax9.set_title('Product as Function of Mean Travel Time')
   ax9.set_xlim(0,np.max(m1.reshape(nnet))/86400)
   ax9.set_ylim(0,0.5*np.min([c1m,c2m]))
   # pcolor.plot of reaction rate
   ax10 = plt.subplot(4,3,10)
   rplot=ax10.pcolormesh(net.x, net.y, np.zeros((ntube,nsec)), 
                       shading='flat', cmap='jet', vmin=0., vmax=43200*r_max)
   plt.colorbar(rplot)
   ax10.set_aspect(aspect=1.0)
   ax10.set_xlabel('x [m]')
   ax10.set_ylabel('y [m]')
   titext4 = ax10.set_title(f'Reaction Rate after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
   # reaction rate as function of x
   ax11 = plt.subplot(4,3,11)
   r_of_x = plt.plot(xcen.reshape(nnet),np.zeros(nnet),'k.',markersize=1)
   ax11.set_xlabel('x [m]')
   ax11.set_ylabel('r [conc./d]')
   ax11.set_title('Reaction Rate as Function of Distance')
   ax11.set_xlim(0,nx[0]*dx[0])
   ax11.set_ylim(0,43200*r_max)
   # reaction rate as function of travel time
   ax12 = plt.subplot(4,3,12)
   r_of_tau = plt.plot(m1.reshape(nnet)/86400,np.zeros(nnet),'k.',markersize=1)
   ax12.set_xlabel('\u03C4 [d]')
   ax12.set_ylabel('r [conc./d]')
   ax12.set_title('Reaction Rate as Function of Mean Travel Time')
   ax12.set_xlim(0,np.max(m1.reshape(nnet))/86400)
   ax12.set_ylim(0,43200*r_max)

   plt.draw()
   plt.pause(0.01)
   plt.show()

# time loop
for i in range(len(tvec)):
    t = (i+1)*dt
    print(f't = {t:10.0f} s')
    BTC1old=c1[lastcol]
    BTC2old=c2[lastcol]
    BTC3old=c3[lastcol]
    # ADE for compound 1
    # update right-hand side vector
    rhs=Mright @ c1 + np.ones((ntube*nsec,1))*invec*cin*c_in[0]
    # solve for concentration
    # c1, info = bicgstab(Mleft, rhs,rtol=1e-8,atol=1e-16,M=Mleft2,x0=c1)
    c1 = spsolve(Mleft, rhs)
    c1 = c1.reshape((ntube*nsec,1))
    # ADE for compound 2
    # update right-hand side vector
    rhs=Mright @ c2 + np.ones((ntube*nsec,1))*invec*cin*c_in[1]
    # solve for concentration
    # c2, info = bicgstab(Mleft, rhs,rtol=1e-8,atol=1e-16,M=Mleft2,x0=c2)
    c2 = spsolve(Mleft, rhs)
    c2 = c2.reshape((ntube*nsec,1))
    # ADE for compound 3
    # update right-hand side vector
    rhs=Mright @ c3 + np.ones((ntube*nsec,1))*invec*cin*c_in[2]
    # solve for concentration
    # c3, info = bicgstab(Mleft, rhs,rtol=1e-8,atol=1e-16,M=Mleft2,x0=c3)
    c3 = spsolve(Mleft, rhs)
    c3 = c3.reshape((ntube*nsec,1))
    
    # Reaction by operator split
    # rate law
    r=c1/(c1+K_MM[0])*c2/(c2+K_MM[1])*r_max
    # explicit Euler integration
    c1=c1-dt*r
    c2=c2-dt*r
    c3=c3+dt*r
    
    # breakthrough curves in the outflow
    BTC1[:,i]=(1-CN)*BTC1old[:,0]+CN*c1[lastcol,0]
    BTC2[:,i]=(1-CN)*BTC2old[:,0]+CN*c2[lastcol,0]
    BTC3[:,i]=(1-CN)*BTC3old[:,0]+CN*c3[lastcol,0]
    
    # stop loop if breakthrough is complete
    if np.min(BTC1[:,i]) > 0.999:
       tvec=tvec[:i+1]
       BTC1 = BTC1[:,:i+1]
       BTC2 = BTC2[:,:i+1]
       BTC3 = BTC3[:,:i+1]
       break
    # update plot
    if plottransient:
       tdt=datetime.utcfromtimestamp(t)
       tdays = np.floor(t/86400)
       cplot1.set_array(c1.reshape((ntube,nsec)))
       cplot2.set_array(c2.reshape((ntube,nsec)))
       cplot3.set_array(c3.reshape((ntube,nsec)))
       rplot.set_array(r.reshape((ntube,nsec))*86400)
       rplot.set_clim(0,np.max(r)*86400)
       titext1.set_text(
       f'Reactant 1 after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
       titext2.set_text(
       f'Reactant 2 after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
       titext3.set_text(
       f'Product after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
       titext4.set_text(
       f'Reaction Rate after{tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')
       c1_of_x[0].set_ydata(c1)
       c1_of_tau[0].set_ydata(c1)
       c2_of_x[0].set_ydata(c2)
       c2_of_tau[0].set_ydata(c2)
       c3_of_x[0].set_ydata(c3)
       c3_of_tau[0].set_ydata(c3)
       r_of_x[0].set_ydata(r*86400)
       r_of_tau[0].set_ydata(r*86400)
       ax11.set_ylim(0,np.max(r)*86400)
       ax12.set_ylim(0,np.max(r)*86400)
       # updated values
       fig2.canvas.draw()
       fig2.canvas.flush_events()
       plt.pause(0.01)
       plt.show()

# Compute product of A and B using different averaging rules
meanprodAB=np.sum(BTC1*BTC2)/ntube
prodmeanAmeanB=np.sum(np.mean(BTC1,axis=0)*np.mean(BTC2,axis=0))
print(f'Mean product of A and B in the outflow:  {meanprodAB:10.3g}')
print(f'Product of mean A and mean B in outflow: {prodmeanAmeanB:10.3g}')

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
plt.plot(np.outer(tvec,np.ones(ntube)),BTC1.T,color='#FF8080',linewidth=0.5)
plt.plot(np.outer(tvec,np.ones(ntube)),BTC2.T,color='#8080FF',linewidth=0.5)
plt.plot(np.outer(tvec,np.ones(ntube)),BTC3.T,color='#80FF80',linewidth=0.5)
plt.plot(tvec,np.mean(BTC1,axis=0),'r',linewidth=4)
plt.plot(tvec,np.mean(BTC2,axis=0),'b',linewidth=4)
plt.plot(tvec,np.mean(BTC3,axis=0),'g',linewidth=4)
plt.ylim(0,1)
plt.xlabel('t [d]')
plt.ylabel('c [conc.]')

plt.show(block=True)

