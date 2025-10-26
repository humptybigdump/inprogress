# =============================================================================
# This script generates random 2-D fields, computes heads and
# stream function values, constructs streamline-oriented grids,
# computes steady-state concentrations for the joint injection 
# of reactants undergoing a microbially mediated reaction
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
# Matlab Code: September 21, 2013
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
from scipy.sparse.linalg import spsolve, spilu, LinearOperator, bicgstab                                
from scipy.sparse import csr_matrix, bmat, spdiags
import pyamg # installation of pyamg: pip install pyamg
import time
from datetime import datetime
import warnings
from scipy.special import erf
from scipy.optimize import fsolve

from fullscreenfigure import fullscreenfigure
from randomK import randomK
import gw_FEM as gw
from streamlinegrid import slgrid, store_mat, mob_mat, quad_cell_areas

# number of elements per direction (x,y)
nx = [250, 100]
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
Dm    = [3e-10, 1e-9, 8e-10, 1e-10]  # pore diffusion coefficient of DOC, 
                                     # oxygen, product, and mobile biomass
# time control
dt_max = 86400*10.
dt_ini = 86400.
dt = dt_ini
t_end = 365*86400.
# convergence criterion: maximum norm of the residuals
resnormmax=1e-10; 

# biokinetic parameters
# A + B -> C
# biomass in steady state
# stoichiometry
stoch_a = 1.     # reactant 1
stoch_b = 1.     # reactant 2
stoch_c = 1.     # product
# concentrations in the inflow
Ain = 0.33       # mmol/L = 4 mg/L Corg 
Bamb = 0.25      # mmol/L = 8 mg/L O2
bioin = 1e-3     # mg/L biomass (permanent inocculation)
# Monod-related coefficients
KA = 8.33e-2     # mmol/L Monod coeff. = 1 mg/L Corg
KB = 3.13e-2     # mmol/L Monod coeff. = 1 mg/L O2
mumax = 1/86400. # 1/s max. spec. growth rate
Yield = 1.       # mg/mmol specific yield
# additional biomass related coefficients
kdec =0.1/86400  # 1/s decay rate coeff.
R_bio=100.       # retardation factor for transport of biomass

# dimensions of the streamline-oriented grid
ntube = 100
nsec  = 250
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
# random field
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
# K = randomK(nx, dx, lx, ang, sigY, Ctype, Kg)

# single rectangular inclusion
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
# psi0=(1-np.reshape(Y,(nnod,1))/dx[1]/nx[1])
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
# water-filled area of all cells
porarea = quad_cell_areas(net.x, net.y)*poros
porarea = porarea.reshape((nnet,1))
# calculate matrices to solve for ADE on streamline-oriented grid
# storage matrix
Mstore = store_mat(net, poros)
# mobility matrix
# using average Dp-value for mixing ratio
Mmob  = mob_mat(net,al,at,np.mean(Dm[0:3]),poros,1)
# for DOC
Mmob1 = mob_mat(net,al,at,Dm[0],poros,1)
# for oxygen
Mmob2 = mob_mat(net,al,at,Dm[1],poros,1)
# for product
Mmob3 = mob_mat(net,al,at,Dm[2],poros,1)
# for mobile biomass
Mmob4 = mob_mat(net,al,at,Dm[3],poros,1) 

# -----------------------------------------------------------------------------
# Compute Mixing Ratio
# -----------------------------------------------------------------------------
# first column of cells
firstcol = list(range(0,nsec*ntube,nsec))

# specific discharge per stream tube
invec = np.zeros(nnet)
invec[0:nsec*ntube:nsec]=Qin/ntube

# inflow marker
is_in1 = np.zeros(((ntube,nsec)))
is_in1[np.floor(ntube/2).astype(int)+np.arange(-15,15).astype(int),0] = 1
is_in1=is_in1.reshape(nnet)
is_in2 = np.zeros(((ntube,nsec)))
is_in2[:,0]=1
is_in2[np.floor(ntube/2).astype(int)+np.arange(-15,15).astype(int),0] = 0
is_in2=is_in2.reshape(nnet)

print('Solve for Mixing Ratio')
rhs=invec*is_in1
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
# Analytical solutions at steady state
# -----------------------------------------------------------------------------
# O.A. Cirpka & A.J. Valocchi (2007): Two-dimensional concentration 
# distribution for mixing-controlled bi-oreactive transport in steady state. 
# Advances Water Resour. 30(6-7): 1668-1679, 
# doi:10.1016/j.advwatres.2006.05.022.
# O.A. Cirpka & A.J. Valocchi (2009): Reply to Comments on "Two-dimensional 
# concentration distribution for mixing-controlled bioreactive transport in 
# steady state" by H. Shao et al. Advances Water Re-sour. 32(2): 298-301

print('Compute Analytical Results at Steady State')

def concdist(mixratio, rtype, a, b, c, KA, KB, Ain, Bamb, kdec, mumax, Y, 
             Mmob=None, porarea=None):
    kdecrel = kdec / mumax

    # Total concentrations
    Atot = mixratio * Ain
    Btot = (1 - mixratio) * Bamb

    # Critical mixing ratio
    Xcrit = a * Bamb / (b * Ain + a * Bamb)

    if rtype == 1:
        # Instantaneous reaction
        A = np.zeros_like(mixratio)
        B = np.zeros_like(mixratio)
        C = np.zeros_like(mixratio)

        # For mixratio >= Xcrit
        mask1 = mixratio >= Xcrit
        A[mask1] = mixratio[mask1] * Ain - a / b * Bamb * (1 - mixratio[mask1])
        C[mask1] = c / b * Bamb * (1 - mixratio[mask1])

        # For mixratio < Xcrit
        mask2 = mixratio < Xcrit
        B[mask2] = (1 - mixratio[mask2]) * Bamb - b / a * Ain * mixratio[mask2]
        C[mask2] = c / a * Ain * mixratio[mask2]
        return A, B, C

    elif rtype == 2:
        # Double-Monod kinetics with linear decay
        omega_max = (Xcrit * Ain / (KA + Xcrit * Ain)) * ((1 - Xcrit) * Bamb / (KB + (1 - Xcrit) * Bamb)) / kdecrel

        if omega_max < 1:
            C = np.zeros_like(mixratio)
            A = Atot*np.ones_like(mixratio)
            B = Btot*np.ones_like(mixratio)
            Bio = np.zeros_like(mixratio)
        else:
            def C_ex_X(X, a, b, c, KA, KB, Ain, Bamb, kdecrel):            
                Atot = X * Ain
                Btot = (1 - X) * Bamb
            
                p2 = (1 - kdecrel) * a * b / c**2
                p1 = kdecrel * ((KA + Atot) * b / c + (KB + Btot) * a / c) - Atot * b / c - Btot * a / c
                p0 = Atot * Btot - kdecrel * (KA + Atot) * (KB + Btot)
            
                # Suppress warnings for potential sqrt of negative numbers
                with np.errstate(invalid='ignore'):
                    discriminant = np.sqrt(p1**2 - 4 * p2 * p0)
                    C = 0.5 * (-p1 - discriminant) / p2      
                return C
            
            def dCdX_ex_X(X, a, b, c, KA, KB, Ain, Bamb, kdecrel):
                Atot = X * Ain
                Btot = (1 - X) * Bamb
            
                p2 = (1 - kdecrel) * a * b / c**2
                p1 = kdecrel * ((KA + Atot) * b / c + (KB + Btot) * a / c) - Atot * b / c - Btot * a / c
                p0 = Atot * Btot - kdecrel * (KA + Atot) * (KB + Btot)
            
                # Derivatives of the coefficients with respect to X
                dp0dX = Ain * Bamb * (1 - 2 * X) * (1 - kdecrel) - kdecrel * (Ain * KB - Bamb * KA)
                dp1dX = (kdecrel - 1) * (Ain * b / c - Bamb * a / c)
            
                # Derivatives of C w.r.t. polynomial coefficients
                with np.errstate(invalid='ignore'):
                    discriminant = np.sqrt(p1**2 - 4 * p2 * p0)
                    dCdp0 = 1 / discriminant
                    dCdp1 = -0.5 / p2 * (p1 / discriminant + 1)
            
                    dCdX = dp0dX * dCdp0 + dp1dX * dCdp1
                return dCdX
           
            # Finding Xmin and Xmax
            Xmin = fsolve(lambda X_: 
                          C_ex_X(X_, a, b, c, KA, KB, Ain, Bamb, kdecrel) 
                          - X_ * dCdX_ex_X(X_, a, b, c, KA, KB, Ain, Bamb, kdecrel),
                          Xcrit)[0]
            Xmax = fsolve(lambda X_: 
                          C_ex_X(X_, a, b, c, KA, KB, Ain, Bamb, kdecrel) 
                          + (1 - X_) * 
                          dCdX_ex_X(X_, a, b, c, KA, KB, Ain, Bamb, kdecrel), 
                          Xcrit)[0]

            slope1 = dCdX_ex_X(Xmin, a, b, c, KA, KB, Ain, Bamb, kdecrel)
            slope2 = dCdX_ex_X(Xmax, a, b, c, KA, KB, Ain, Bamb, kdecrel)

            # Concentrations
            C = C_ex_X(mixratio, a, b, c, KA, KB, Ain, Bamb, kdecrel)
            C[mixratio < Xmin] = slope1 * mixratio[mixratio < Xmin]
            C[mixratio > Xmax] = (mixratio[mixratio > Xmax] - 1) * slope2

            A = Atot - a / c * C
            B = Btot - b / c * C
            Bio=(Mmob@C)/porarea*(KA+A)*(KB+B)/A/B/mumax/c*Y
            Bio[mixratio<Xmin] = 0
            Bio[mixratio>Xmax] = 0
            return A, B, C, Bio
    else:
        raise ValueError("Invalid 'rtype'. Use 1 or 2.")

Ainst,Binst,Cinst  = concdist(mixratio.reshape((nnet,1)), 1, stoch_a, stoch_b, 
                              stoch_c, KA, KB, Ain, Bamb, kdec, mumax, Yield)
Abio,Bbio,Cbio,Bio = concdist(mixratio.reshape((nnet,1)), 2, stoch_a, stoch_b, 
                              stoch_c, KA, KB, Ain, Bamb, kdec, mumax, Yield, 
                              Mmob, porarea)

# -----------------------------------------------------------------------------
# Transient bioreactive transport simulation
# -----------------------------------------------------------------------------

# define transport matrix and right-hand side vector for all three components
zeromat = csr_matrix((nnet,nnet))
Mtot=bmat([[  Mmob1, zeromat, zeromat, zeromat],
           [zeromat,   Mmob2, zeromat, zeromat],
           [zeromat, zeromat,   Mmob3, zeromat],
           [zeromat, zeromat, zeromat,Mmob4/R_bio]])
Mstore=bmat([[ Mstore, zeromat, zeromat, zeromat],
             [zeromat,  Mstore, zeromat, zeromat],
             [zeromat, zeromat,  Mstore, zeromat],
             [zeromat, zeromat, zeromat,  Mstore]])
rhs =np.vstack([(invec*is_in1*Ain).reshape((nnet,1)),
                (invec*is_in2*Bamb).reshape((nnet,1)),
                np.zeros((nnet,1)),
                (invec*bioin/R_bio).reshape((nnet,1))])

# initialization: steady-state transport without reactions
# ilu = spilu(Mtot)
# Mtot2 = LinearOperator(Mtot.shape, ilu.solve)
with warnings.catch_warnings():
     warnings.simplefilter("ignore")
     ml = pyamg.ruge_stuben_solver(Mtot)
     Mtot2 = ml.aspreconditioner()
c, info = bicgstab(Mtot, rhs,rtol=1e-10,atol=1e-18,M=Mtot2)
# c=spsolve(Mtot,rhs)


c1=c[      :  nnet]
c2=c[  nnet:2*nnet]
c3=c[2*nnet:3*nnet]
c4=c[3*nnet:      ]
cold=c;

# plot concentrations of reactive compounds
fig2 = fullscreenfigure(2)
# pcolor.plot of substrate
ax1 = plt.subplot(4,3,1)
c1plot=ax1.pcolormesh(net.x,net.y,np.reshape(c1,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=Ain)
plt.colorbar(c1plot,label='c [mmol/L]')
ax1.set_aspect(aspect=1.0)
ax1.set_xlabel('x [m]')
ax1.set_ylabel('y [m]')
ax1.set_title('Substrate')
ax1.set_xlim(0,nx[0]*dx[0])
ax1.set_ylim(0,nx[1]*dx[1])
# pcolor.plot of oxygen
ax2 = plt.subplot(4,3,4)
c2plot=ax2.pcolormesh(net.x,net.y,np.reshape(c2,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=Bamb)
plt.colorbar(c2plot,label='c [mmol/L]')
ax2.set_aspect(aspect=1.0)
ax2.set_xlabel('x [m]')
ax2.set_ylabel('y [m]')
ax2.set_title('Oxygen')
ax2.set_xlim(0,nx[0]*dx[0])
ax2.set_ylim(0,nx[1]*dx[1])
# pcolor.plot of product
ax3 = plt.subplot(4,3,7)
c3plot=ax3.pcolormesh(net.x,net.y,np.reshape(c3,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,
                      vmax=np.max(Cinst))
plt.colorbar(c3plot,label='c [mmol/L]')
ax3.set_aspect(aspect=1.0)
ax3.set_xlabel('x [m]')
ax3.set_ylabel('y [m]')
ax3.set_title('Product')
ax3.set_xlim(0,nx[0]*dx[0])
ax3.set_ylim(0,nx[1]*dx[1])
# pcolor.plot of biomass
ax4 = plt.subplot(4,3,10)
c4plot=ax4.pcolormesh(net.x,net.y,np.log10(c4).reshape(ntube,nsec),
                      shading='flat',cmap='jet',vmin=np.log10(bioin)-1,
                      vmax=np.log10(np.quantile(Bio,0.99)))
plt.colorbar(c4plot,label='log$_{10}$c [c in mg/L]')
ax4.set_aspect(aspect=1.0)
ax4.set_xlabel('x [m]')
ax4.set_ylabel('y [m]')
ax4.set_title('Biomass')
ax4.set_xlim(0,nx[0]*dx[0])
ax4.set_ylim(0,nx[1]*dx[1])
tdays=0
tdt=datetime.utcfromtimestamp(0)
titext = fig2.suptitle(
f'Concentrations after {tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}',
fontweight='bold', fontsize=16)

ax=plt.subplot(4,3,2)
Abioplot=ax.pcolormesh(net.x,net.y,np.reshape(Abio,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=Ain)
plt.colorbar(Abioplot,label='c [mmol/L]')
ax.set_aspect(aspect=1.0)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('Substrate (anal.)')
ax.set_xlim(0,nx[0]*dx[0])
ax.set_ylim(0,nx[1]*dx[1])

ax=plt.subplot(4,3,3)
Ainstplot=ax.pcolormesh(net.x,net.y,np.reshape(Ainst,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=Ain)
plt.colorbar(Ainstplot,label='c [mmol/L]')
ax.set_aspect(aspect=1.0)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('Substrate (instant. reac.)')
ax.set_xlim(0,nx[0]*dx[0])
ax.set_ylim(0,nx[1]*dx[1])

ax=plt.subplot(4,3,5)
Bbioplot=ax.pcolormesh(net.x,net.y,np.reshape(Bbio,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=Bamb)
plt.colorbar(Bbioplot,label='c [mmol/L]')
ax.set_aspect(aspect=1.0)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('Oxygen (anal.)')
ax.set_xlim(0,nx[0]*dx[0])
ax.set_ylim(0,nx[1]*dx[1])

ax=plt.subplot(4,3,6)
Binstplot=ax.pcolormesh(net.x,net.y,np.reshape(Binst,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=Bamb)
plt.colorbar(Binstplot,label='c [mmol/L]')
ax.set_aspect(aspect=1.0)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('Oxygen (instant. reac.)')
ax.set_xlim(0,nx[0]*dx[0])
ax.set_ylim(0,nx[1]*dx[1])

ax=plt.subplot(4,3,8)
Cbioplot=ax.pcolormesh(net.x,net.y,np.reshape(Cbio,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0,vmax=np.max(Cinst))
plt.colorbar(Cbioplot,label='c [mmol/L]')
ax.set_aspect(aspect=1.0)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('Product (anal.)')
ax.set_xlim(0,nx[0]*dx[0])
ax.set_ylim(0,nx[1]*dx[1])

ax=plt.subplot(4,3,9)
Cinstplot=ax.pcolormesh(net.x,net.y,np.reshape(Cinst,(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=0)
plt.colorbar(Cinstplot,label='c [mmol/L]')
ax.set_aspect(aspect=1.0)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('Product (instant. reac.)')
ax.set_xlim(0,nx[0]*dx[0])
ax.set_ylim(0,nx[1]*dx[1])

ax=plt.subplot(4,3,11)
Bio2=np.copy(Bio)
Bio2[Bio2==0]=bioin*.1
Bioanalplot=ax.pcolormesh(net.x,net.y,np.log10(Bio2.reshape(ntube,nsec)),
                      shading='flat',cmap='jet',vmin=np.log10(bioin)-1,
                      vmax=np.log10(np.quantile(Bio,0.99)))
plt.colorbar(Bioanalplot,label='log$_{10}$c [c in mg/L]')
ax.set_aspect(aspect=1.0)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('Biomass (anal.)')
ax.set_xlim(0,nx[0]*dx[0])
ax.set_ylim(0,nx[1]*dx[1])

fig2.canvas.draw()
fig2.canvas.flush_events()
plt.pause(0.01)
plt.show()

print('Solve Transient Bioreactive Transport')

t = 0.

while t<t_end:
   t = t+dt
   print(f'Solve for Concentrations at t = {t:10.3g} s')
   done=False
   iter = 0
   # reaction rate
   mu=c1/(c1+KA)*c2/(c2+KA)*mumax*c4
   r_tot=np.vstack([(-porarea[:,0]*mu/Yield*stoch_a).reshape((nnet,1)),
                    (-porarea[:,0]*mu/Yield*stoch_b).reshape((nnet,1)),
                    ( porarea[:,0]*mu/Yield*stoch_c).reshape((nnet,1)),
                    ( porarea[:,0]*mu-porarea[:,0]*c4*kdec).reshape((nnet,1))])

   # Matrices
   Mleft=Mtot*dt+Mstore
   Mright=Mstore

   # compute residuals
   res=Mleft@c[:,None]-rhs*dt-r_tot*dt-Mright@cold[:,None]
   resnorm=np.linalg.norm(res)
   print(f'iter {iter}: norm of residuals {resnorm:10.3g}')
   while done==False:
       if resnorm < resnormmax: 
          done=True
       else:
          iter +=1
          resold=resnorm
          # evaluate Jacobian
          dmudc1=KA/(c1+KA)**2 *c2/(c2+KB)   *mumax*c4*porarea[:,0]
          dmudc1=spdiags(dmudc1, 0, nnet, nnet, format='csr')
          dmudc2=c1/(c1+KA)    *KB/(c2+KB)**2*mumax*c4*porarea[:,0]
          dmudc2=spdiags(dmudc2, 0, nnet, nnet, format='csr')
          dmudc4=c1/(c1+KA)    *c2/(c2+KB)   *mumax   *porarea[:,0]
          dmudc4=spdiags(dmudc4, 0, nnet, nnet, format='csr')
          
          J11=Mmob1+dmudc1/Yield*stoch_a
          J12=dmudc2/Yield*stoch_a
          J13=zeromat
          J14=dmudc4/Yield*stoch_a
          
          J21=dmudc1/Yield*stoch_b
          J22=Mmob2+dmudc2/Yield*stoch_b
          J23=zeromat
          J24=dmudc4/Yield*stoch_b
          
          J31=-dmudc1/Yield*stoch_c
          J32=-dmudc2/Yield*stoch_c
          J33=Mmob3;
          J34=-dmudc4/Yield*stoch_c
          
          J41=-dmudc1
          J42=-dmudc2;
          J43=zeromat
          J44=Mmob4/R_bio-dmudc4+spdiags(porarea[:,0]*kdec,0,nnet,nnet,format='csr')
    
          J = bmat([[J11,J12,J13,J14],
                    [J21,J22,J23,J24],
                    [J31,J32,J33,J34],
                    [J41,J42,J43,J44]])*dt+Mstore
          # Newton-Raphson step
          # delta_c = spsolve(J,-res)
          # ilu = spilu(J)
          # J2 = LinearOperator(J.shape, ilu.solve)
          with warnings.catch_warnings():
               warnings.simplefilter("ignore")
               ml = pyamg.ruge_stuben_solver(J)
               J2 = ml.aspreconditioner()
          delta_c, info = bicgstab(J,-res,rtol=1e-10,atol=1e-18,M=J2)

          clast=c
          relinc=1.
          while resnorm>=resold:
              # update concentration
              c =clast+relinc*delta_c
              c[c<0]=0
              c1=c[      :  nnet]
              c2=c[  nnet:2*nnet]
              c3=c[2*nnet:3*nnet]
              c4=c[3*nnet:      ]
              # reaction rate
              mu=c1/(c1+KA)*c2/(c2+KA)*mumax*c4
              r_tot=np.vstack([(-porarea[:,0]*mu/Yield*stoch_a).reshape((nnet,1)),
                               (-porarea[:,0]*mu/Yield*stoch_b).reshape((nnet,1)),
                               ( porarea[:,0]*mu/Yield*stoch_c).reshape((nnet,1)),
                               ( porarea[:,0]*mu-porarea[:,0]*c4*kdec).reshape((nnet,1))])
              # compute residuals
              res=Mleft@c[:,None]-rhs*dt-r_tot*dt-Mright@cold[:,None]
              resnorm=np.linalg.norm(res)
              print(f'iter {iter}: norm of residuals {resnorm:10.3g}')
              if resnorm>=resold:
                 if relinc==0.125:
                    iter = 11
                 else:
                    relinc=relinc*.5
                    print(f'reduce step size to {relinc}')
   # now done==True
   cold = c
   if iter>10:
      dt = dt/1.5
      print(f'new dt =  {dt }s')
   if iter<5 and relinc==1.:
      dt=np.min([dt*1.5,dt_max])
      print(f'new dt =  {dt }s')
   c1plot.set_array(c1.reshape((ntube,nsec)))
   c2plot.set_array(c2.reshape((ntube,nsec))) 
   c3plot.set_array(c3.reshape((ntube,nsec))) 
   c4plot.set_array(np.log10(c4).reshape(ntube,nsec))
   # c3plot.set_clim(0,np.max(c3))
   # c4plot.set_clim(np.log10(bioin)-1,np.log10(np.max(c4)))
   tdays=np.floor(t/86400)
   tdt=datetime.utcfromtimestamp(t)
   titext.set_text(
   f'Concentrations after {tdays:3.0f} days, {tdt.strftime("%H:%M:%S")}')

   # updated values
   fig2.canvas.draw()
   fig2.canvas.flush_events()
   plt.pause(0.01)
   plt.show()
    
toc = time.time()
print(f"Elapsed time for reactive-transport calculations: {toc - tic:.4f} seconds")


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

# length profiles of mass flux
A_of_h=np.mean(c[0:nnet].reshape((ntube,nsec)),axis=0)
B_of_h=np.mean(c[nnet:2*nnet].reshape((ntube,nsec)),axis=0)
C_of_h=np.mean(c[2*nnet:3*nnet].reshape((ntube,nsec)),axis=0)
Ainst_of_h=np.mean(Ainst.reshape((ntube,nsec)),axis=0)
Binst_of_h=np.mean(Binst.reshape((ntube,nsec)),axis=0)
Cinst_of_h=np.mean(Cinst.reshape((ntube,nsec)),axis=0)
Aana_of_h=np.mean(Abio.reshape((ntube,nsec)),axis=0)
Bana_of_h=np.mean(Bbio.reshape((ntube,nsec)),axis=0)
Cana_of_h=np.mean(Cbio.reshape((ntube,nsec)),axis=0)

fig3 = fullscreenfigure(3)
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*A_of_h,'r',label='substrate')
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*B_of_h,'b',label='oxygen')
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*C_of_h,'g',label='product')
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*Aana_of_h,'r--',label='analytical')
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*Bana_of_h,'b--')
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*Cana_of_h,'g--')
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*Ainst_of_h,'r:',label='inst. reac.')
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*Binst_of_h,'b:')
plt.plot(0.5*(net.phi[0,:-1]+net.phi[0,1:]),Qin*Cinst_of_h,'g:')
plt.xlabel('h [m]')
plt.ylabel('mass flux [mol/(ms)]')
plt.xlim(0,phiin)
plt.ylim(0,max(Ain*np.sum(is_in1),Bamb*np.sum(is_in2))*Qin/nx[1])
plt.gca().invert_xaxis()
plt.suptitle('Mass Flux as Function of Hydraulic Head')
plt.legend()

plt.show(block=True)

