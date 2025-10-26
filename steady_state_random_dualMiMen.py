# =============================================================================
# This script generates random 2-D fields, computes heads and
# stream function values, constructs streamline-oriented grids,
# computes steady-state concentrations for the joint injection 
# of reactants undergoing dual Michaelis-Menten kinetics
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
from scipy.integrate import solve_ivp
from scipy.sparse.linalg import spilu, LinearOperator, bicgstab                                
from scipy.sparse import csr_matrix, bmat, spdiags
import pyamg # installation of pyamg: pip install pyamg
import time
import warnings
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
poros = 0.3     # porosity [-]
al    = 0.01    # longitudinal dispersivity [m]
at    = 0.001   # transverse dispersivity [m]
Dm    = 1e-9    # molecular diffusion coefficient [m]
c_in  = [2,1,0] # inflow concentration [conc.]
K_MM  = [.1,.1] # Michaelis-Menten coefficients [conc.]
r_max=5e-6      # Maximum reaction rate [conc./s]

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
with warnings.catch_warnings():
     warnings.simplefilter("ignore")
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
with warnings.catch_warnings():
     warnings.simplefilter("ignore")
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

# -----------------------------------------------------------------------------
# Preparation of Transport Calculations
# -----------------------------------------------------------------------------
print("Prepare Matrices for Transport Calculations")
# water-filled area of all cells
porarea = quad_cell_areas(net.x, net.y)*poros
porarea = porarea.reshape((nnet,1))
# calculate matrices to solve for ADE on streamline-oriented grid
Mstore = store_mat(net, poros)              # storage matrix
Mmob   = mob_mat(net, al, at, Dm, poros, 1) # mobility matrix

# -----------------------------------------------------------------------------
# Compute Mean Travel Time by Groundwater-Age Equation
# -----------------------------------------------------------------------------
print("Solve Mean Groundwater-Age Equation")
rhs=porarea
# Preconditioner
# ilu = spilu(Mmob)
# Mmob2 = LinearOperator(Mmob.shape, ilu.solve)
ml = pyamg.air_solver(Mmob,coarse_solver='splu')
Mmob2 = ml.aspreconditioner()
# solve for first temporal moment
m1, info = bicgstab(Mmob,rhs,rtol=1e-8,atol=1e-12,M=Mmob2)
m1=m1.reshape(ntube,nsec)

toc = time.time()
print(f"Elapsed time for calculation of 1st moment: {toc - tic:.4f} seconds")
tic = toc

# -----------------------------------------------------------------------------
# Comparison to solving the ODE system in travel-time
# -----------------------------------------------------------------------------
print('Solve ODE in travel time for comparison')
# define ODE
def MiMenODE(t,c,K_MM,r_max):
    r = c[0]/(c[0]+K_MM[0])*c[1]/(c[1]+K_MM[1])*r_max
    dcdt = np.zeros_like(c)
    dcdt[0] = -r
    dcdt[1] = -r
    dcdt[2] = r
    return dcdt
# solve ODE
sol = solve_ivp(MiMenODE, [0, np.max(m1.reshape(nnet))], 
                c_in, args=(K_MM, r_max), method='BDF')
T_ODE = sol.t
C_ODE = sol.y.T
r_ODE = C_ODE[:,0]/(C_ODE[:,0]+K_MM[0])*C_ODE[:,1]/(C_ODE[:,1]+K_MM[1])*r_max

# -----------------------------------------------------------------------------
# Steady-state reactive transport transport
# -----------------------------------------------------------------------------

# first column of cells
firstcol = list(range(0,nsec*ntube,nsec))

# initialization
c1 = np.interp(m1.reshape((nnet,1)), T_ODE, C_ODE[:,0])
# np.ones((nnet,1))*c_in[0]
c2 = np.interp(m1.reshape((nnet,1)), T_ODE, C_ODE[:,1])
# np.zeros((nnet,1))*c_in[1]
c3 = np.interp(m1.reshape((nnet,1)), T_ODE, C_ODE[:,2])
# np.zeros((nnet,1))*c_in[2]
c  = np.vstack([c1, c2, c3]) 

# specific discharge per stream tube
invec = np.zeros(nnet)
invec[0:nsec*ntube:nsec]=Qin/ntube

# inflow marker
is_in = np.zeros(nnet)
is_in[firstcol] = 1

# define transport matrix and right-hand side vector for all three components
zeromat = csr_matrix((nnet,nnet))
Mtot=bmat([[Mmob, zeromat, zeromat],
           [zeromat, Mmob, zeromat],
           [zeromat, zeromat, Mmob]])
rhs = np.hstack((invec*is_in*c_in[0],invec*is_in*c_in[1],invec*is_in*c_in[2]))

# center point of all cella
xcen=0.25*(net.x[:-1,:-1]+net.x[1:,:-1]+net.x[:-1,1:]+net.x[1:,1:])

print('Solve for Concentrations of Reactants')

# reaction rate
r=c1/(c1+K_MM[0])*c2/(c2+K_MM[1])*r_max
r_tot=np.vstack([-porarea*r, -porarea*r, porarea*r])

# compute residuals
res = Mtot@c - rhs[:,None] - r_tot
resnorm = np.linalg.norm(res)

print(f'norm of residuals: {resnorm:8.2e}')

# initialize iteration index
iter = 0

while resnorm > 2e-16:
   iter += 1
   resold = resnorm
   print(f'iteration index: {iter}')
   
   # evaluate Jacobian
   dia1=K_MM[0]*(c1+K_MM[0])**-2 * c2/(c2+K_MM[1])*r_max*porarea
   drdc1=spdiags(dia1.T,0,format='csr')
   dia2=K_MM[1]*(c2+K_MM[1])**-2 * c1/(c1+K_MM[0])*r_max*porarea
   drdc2=spdiags(dia2.T,0, format='csr')
   # Jacobian matrix
   J=bmat([[Mmob+drdc1,     drdc2,zeromat],
           [     drdc1,Mmob+drdc2,zeromat],
           [    -drdc1,    -drdc2,   Mmob]])
   print('precondition system of equations')
   # AMG preconditioner
   # ml = pyamg.air_solver(J,coarse_solver='splu')
   # J2 = ml.aspreconditioner()
   ilu = spilu(J.tocsc())
   J2 = LinearOperator(J.shape, ilu.solve)

   print('update concentrations')
   delta_c, info = bicgstab(J, -res,rtol=1e-8,atol=1e-18,M=J2)
   delta_c = delta_c.reshape((nnet*3,1))
   cold = c
   relinc = 1.
   
   while resnorm>=resold:
      c =cold+relinc*delta_c
      c[c<0]=0
      c1=c[:nnet]
      c2=c[nnet:2*nnet]
      c3=c[2*nnet:]
  
      # reaction rate
      r=c1/(c1+K_MM[0])*c2/(c2+K_MM[1])*r_max
      r_tot=r_tot=np.vstack([-porarea*r, -porarea*r, porarea*r])
      
      # compute residuals
      res = Mtot@c - rhs[:,None] - r_tot
      resnorm = np.linalg.norm(res)

      print(f'norm of residuals: {resnorm:8.2e}')
      if resnorm>=resold and relinc>1/16.:
         relinc=relinc/2;
         print(f'reduce step size to {relinc:9.3g}')
      elif relinc==1/16.: break   
    
toc = time.time()
print(f"Elapsed time for reactive-transport calculations: {toc - tic:.4f} seconds")

# distributions of concentrations as function of travel time
tmax_reg=np.quantile(m1[:,-1],0.95)
treg=np.arange(0.5/nsec,1+.1/nsec,0.5/nsec)*tmax_reg
c1_treg=np.zeros((ntube,len(treg)))
c2_treg=np.zeros((ntube,len(treg)))
c3_treg=np.zeros((ntube,len(treg)))
r_treg =np.zeros((ntube,len(treg)))
for ii in range(ntube):
    c1_treg[ii,:]=np.interp(treg,m1[ii,:],c1.reshape(((ntube,nsec)))[ii,:],
                            left=np.nan,right=np.nan)
    c2_treg[ii,:]=np.interp(treg,m1[ii,:],c2.reshape(((ntube,nsec)))[ii,:],
                            left=np.nan,right=np.nan)
    c3_treg[ii,:]=np.interp(treg,m1[ii,:],c3.reshape(((ntube,nsec)))[ii,:],
                            left=np.nan,right=np.nan)
    r_treg[ii,:] =np.interp(treg,m1[ii,:], r.reshape(((ntube,nsec)))[ii,:],
                            left=np.nan,right=np.nan)

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

# plot concentrations of reactive compounds
fig3 = fullscreenfigure(3)
# pcolor.plot of compound 1
ax1 = plt.subplot(4,3,1)
c1plot=ax1.pcolormesh(net.x,net.y,np.reshape(c1,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=c_in[0])
plt.colorbar(c1plot)
ax1.set_aspect(aspect=1.0)
ax1.set_xlabel('x [m]')
ax1.set_ylabel('y [m]')
ax1.set_title('Reactant 1')
ax1.set_xlim(0,nx[0]*dx[0])
ax1.set_ylim(0,nx[1]*dx[1])
# compound 1 as function of x
ax2 = plt.subplot(4,3,2)
plt.plot(xcen.reshape(nnet),c1,'k.',markersize=1)
ax2.set_xlabel('x [m]')
ax2.set_ylabel('c [conc.]')
ax2.set_title('Reactant 1 as Function of Distance')
ax2.set_xlim(0,nx[0]*dx[0])
ax2.set_ylim(0,c_in[0])
# compound 1 as function of travel time
ax3 = plt.subplot(4,3,3)
plt.plot(m1.reshape(nnet)/86400,c1,'k.',markersize=1,label='2-D ADRE')
plt.plot(T_ODE/86400,C_ODE[:,0],'r',label='ODE')
plt.legend()
ax3.set_xlabel('\u03C4 [d]')
ax3.set_ylabel('c [conc.]')
ax3.set_title('Reactant 1 as Function of Mean Travel Time')
ax3.set_xlim(0,np.max(m1.reshape(nnet))/86400)
ax3.set_ylim(0,c_in[0])

# pcolor.plot of compound 2
ax4 = plt.subplot(4,3,4)
c2plot=ax4.pcolormesh(net.x,net.y,np.reshape(c2,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=c_in[1])
plt.colorbar(c2plot)
ax4.set_aspect(aspect=1.0)
ax4.set_xlabel('x [m]')
ax4.set_ylabel('y [m]')
ax4.set_title('Reactant 2')
ax4.set_xlim(0,nx[0]*dx[0])
ax4.set_ylim(0,nx[1]*dx[1])
# compound 2 as function of x
ax5 = plt.subplot(4,3,5)
plt.plot(xcen.reshape(nnet),c2,'k.',markersize=1)
ax5.set_xlabel('x [m]')
ax5.set_ylabel('c [conc.]')
ax5.set_title('Reactant 2 as Function of Distance')
ax5.set_xlim(0,nx[0]*dx[0])
ax5.set_ylim(0,c_in[1])
# compound 2 as function of travel time
ax6 = plt.subplot(4,3,6)
plt.plot(m1.reshape(nnet)/86400,c2,'k.',markersize=1,label='2-D ADRE')
plt.plot(T_ODE/86400,C_ODE[:,1],'r',label='ODE')
plt.legend()
ax6.set_xlabel('\u03C4 [d]')
ax6.set_ylabel('c [conc.]')
ax6.set_title('Reactant 2 as Function of Mean Travel Time')
ax6.set_xlim(0,np.max(m1.reshape(nnet))/86400)
ax6.set_ylim(0,c_in[1])

# pcolor.plot of compound 3
ax7 = plt.subplot(4,3,7)
c3plot=ax7.pcolormesh(net.x,net.y,np.reshape(c3,(ntube,nsec)),
                      shading='flat',cmap='jet')
plt.colorbar(c3plot)
ax7.set_aspect(aspect=1.0)
ax7.set_xlabel('x [m]')
ax7.set_ylabel('y [m]')
ax7.set_title('Product')
ax7.set_xlim(0,nx[0]*dx[0])
ax7.set_ylim(0,nx[1]*dx[1])
# compound 3 as function of x
ax8 = plt.subplot(4,3,8)
plt.plot(xcen.reshape(nnet),c3,'k.',markersize=1)
ax8.set_xlabel('x [m]')
ax8.set_ylabel('c [conc.]')
ax8.set_title('Product as Function of Distance')
ax8.set_xlim(0,nx[0]*dx[0])
ax8.set_ylim(0,min(c_in[:2]))
# compound 3 as function of travel time
ax9 = plt.subplot(4,3,9)
plt.plot(m1.reshape(nnet)/86400,c3,'k.',markersize=1,label='2-D ADRE')
plt.plot(T_ODE/86400,C_ODE[:,2],'r',label='ODE')
plt.legend()
ax9.set_xlabel('\u03C4 [d]')
ax9.set_ylabel('c [conc.]')
ax9.set_title('Product as Function of Mean Travel Time')
ax9.set_xlim(0,np.max(m1.reshape(nnet))/86400)
ax9.set_ylim(0,min(c_in[:2]))

# pcolor.plot of reaction rate
ax10 = plt.subplot(4,3,10)
rplot=ax10.pcolormesh(net.x,net.y,np.reshape(r,(ntube,nsec))*86400,
                      shading='flat',cmap='jet')
plt.colorbar(rplot)
ax10.set_aspect(aspect=1.0)
ax10.set_xlabel('x [m]')
ax10.set_ylabel('y [m]')
ax10.set_title('Reaction Rate')
ax10.set_xlim(0,nx[0]*dx[0])
ax10.set_ylim(0,nx[1]*dx[1])
# reaction rate as function of x
forlim = 10**np.floor(np.log10(max(r)*86400))
taulim = np.ceil(max(r)*86400/forlim)*forlim
ax11 = plt.subplot(4,3,11)
plt.plot(xcen.reshape(nnet),r*86400,'k.',markersize=1)
ax11.set_xlabel('x [m]')
ax11.set_ylabel('r [conc./d]')
ax11.set_title('Reaction Rate as Function of Distance')
ax11.set_xlim(0,nx[0]*dx[0])
ax11.set_ylim(0,taulim)
# reaction rate as function of travel time
ax12 = plt.subplot(4,3,12)
plt.plot(m1.reshape(nnet)/86400,r*86400,'k.',markersize=1,label='2-D ADRE')
plt.plot(T_ODE/86400,r_ODE*86400,'r',label='ODE')
plt.legend()
ax12.set_xlabel('\u03C4 [d]')
ax12.set_ylabel('r [conc./d]')
ax12.set_title('Reaction Rate as Function of Mean Travel Time')
ax12.set_xlim(0,np.max(m1.reshape(nnet))/86400)
ax12.set_ylim(0,taulim)

# plot concentration distributions as function of mean groundwater age
fig4 = fullscreenfigure(4)
ax1 = plt.subplot(2,2,1)
with warnings.catch_warnings():
     warnings.simplefilter("ignore")
     plt.fill_between(treg/86400, np.nanquantile(c1_treg,0.025,axis=0), 
                 np.nanquantile(c1_treg,0.975,axis=0),
                 color='#E6E6E6',label='2.5-97.5%')
     plt.fill_between(treg/86400, np.nanquantile(c1_treg,0.25,axis=0), 
                 np.nanquantile(c1_treg,0.75,axis=0),
                 color='#ABABAB',label='25-75%')
     plt.plot(treg/86400,np.nanmedian(c1_treg,axis=0),'k',label='median')
plt.plot(T_ODE/86400,C_ODE[:,0],'r',label='ODE')
plt.legend()
ax1.set_xlabel('\u03C4 [d]')
ax1.set_ylabel('c [conc.]')
ax1.set_title('Reactant 1')
ax1.set_xlim(0,tmax_reg/86400)

ax2 = plt.subplot(2,2,2)
with warnings.catch_warnings():
     warnings.simplefilter("ignore")
     plt.fill_between(treg/86400, np.nanquantile(c2_treg,0.025,axis=0), 
                 np.nanquantile(c2_treg,0.975,axis=0),
                 color='#E6E6E6',label='2.5-97.5%')
     plt.fill_between(treg/86400, np.nanquantile(c2_treg,0.25,axis=0), 
                 np.nanquantile(c2_treg,0.75,axis=0),
                 color='#ABABAB',label='25-75%')
     plt.plot(treg/86400,np.nanmedian(c2_treg,axis=0),'k',label='median')
plt.plot(T_ODE/86400,C_ODE[:,1],'r',label='ODE')
plt.legend()
ax2.set_xlabel('\u03C4 [d]')
ax2.set_ylabel('c [conc.]')
ax2.set_title('Reactant 2')
ax2.set_xlim(0,tmax_reg/86400)

ax3 = plt.subplot(2,2,3)
with warnings.catch_warnings():
     warnings.simplefilter("ignore")
     plt.fill_between(treg/86400, np.nanquantile(c3_treg,0.025,axis=0), 
                 np.nanquantile(c3_treg,0.975,axis=0),
                 color='#E6E6E6',label='2.5-97.5%')
     plt.fill_between(treg/86400, np.nanquantile(c3_treg,0.25,axis=0), 
                 np.nanquantile(c3_treg,0.75,axis=0),
                 color='#ABABAB',label='25-75%')
     plt.plot(treg/86400,np.nanmedian(c3_treg,axis=0),'k',label='median')
plt.plot(T_ODE/86400,C_ODE[:,2],'r',label='ODE')
plt.legend()
ax3.set_xlabel('\u03C4 [d]')
ax3.set_ylabel('c [conc.]')
ax3.set_title('Product')
ax3.set_xlim(0,tmax_reg/86400)

ax4 = plt.subplot(2,2,4)
with warnings.catch_warnings():
     warnings.simplefilter("ignore")
     plt.fill_between(treg/86400, np.nanquantile(r_treg,0.025,axis=0)*86400, 
                 np.nanquantile(r_treg,0.975,axis=0)*86400,
                 color='#E6E6E6',label='2.5-97.5%')
     plt.fill_between(treg/86400, np.nanquantile(r_treg,0.25,axis=0)*86400, 
                 np.nanquantile(r_treg,0.75,axis=0)*86400,
                 color='#ABABAB',label='25-75%')
     plt.plot(treg/86400,np.nanmedian(r_treg,axis=0)*86400,'k',label='median')
plt.plot(T_ODE/86400,r_ODE*86400,'r',label='ODE')
plt.legend()
ax4.set_xlabel('\u03C4 [d]')
ax4.set_ylabel('r [conc./d]')
ax4.set_title('Reaction Rate')
ax4.set_xlim(0,tmax_reg/86400)
fig4.suptitle(
    'Concentrations and Reaction Rates as Function of Mean Groundwater Age',
    fontsize='18',fontweight='bold')
plt.show(block=True)

