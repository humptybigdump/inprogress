import numpy as np
import matplotlib.pyplot as plt

import lib as lb

path2sim = "./"###### your simulation folder 

nx = 256
ny = 193
nz = 128

Lx = 8
Ly = 2
Lz = 4

# read y-distribution
filename = path2sim + "yp.dat"
y = np.loadtxt(filename)

x = np.linspace(0, Lx, nx, endpoint=False)
z = np.linspace(0, Lz, nz, endpoint=False)

###############################################################
path2data = path2sim + "data/" ### data folder where snapshots are saved
idfld = 1

u = lb.read_snapshot(path2data, "ux", 1, [nx,ny,nz])
v = lb.read_snapshot(path2data, "uy", 1, [nx,ny,nz])
w = lb.read_snapshot(path2data, "uz", 1, [nx,ny,nz])

phi = lb.read_snapshot(path2data, "phi1", 1, [nx,ny,nz])

###############################################################
### show one z-slice at x=0
plt.figure()
plt.pcolormesh(z,y,u[0,:,:], shading="gouraud")
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel("z")
plt.ylabel("y")
plt.title("z-slice of U snapshot")
plt.show()
### show one x-slice at z=0
plt.figure()
plt.pcolormesh(x,y,u[:,:,0].T, shading="gouraud")
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel("x")
plt.ylabel("y")
plt.title("x-slice of U snapshot")
plt.show()

####### ## 3D snapshots at certain time t has the structure :  u[id_x,id_y,id_z] @ t


##############################################################
### calculating uu field

uu=u*u ## point-wise multiplication

plt.figure()
plt.pcolormesh(x,y,uu[:,:,0].T, shading="gouraud")
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel("x")
plt.ylabel("y")
plt.title("x-slice of uu snapshot")
plt.show()

#############################################################
### spatial averaging along the snapshot axis 0 and 2 (streamwise and spanwise)
U_sp_averaged=np.mean(u,(0,2))
V_sp_averaged=np.mean(v,(0,2))
W_sp_averaged=np.mean(w,(0,2))
T_sp_averaged=np.mean(phi,(0,2))

############The friction Retau=utau*delta/nu is 180 for this simulation####### 

#u_tau=Retau*nu/delta

u_tau=180/4200

plt.plot(y,U_sp_averaged/u_tau)
plt.title("Spatial averaged U profile")
plt.xlabel(r"$y/\delta$")
plt.ylabel(r"$U^+=U/u_\tau$")




#############################################################
### read reference file Re180 -- DNS results at Retau=180
import pandas as pd
df = pd.read_csv('Re180', sep='  ',index_col=False,names=["y/h", "y+", "U+", "u'+","v'+","w'+","-Om_z+","omx+","omy+","omz+","uv+","uw+","vw+","pr+","ps+","psto+","p'+"])

plt.plot(df["y/h"],df["U+"])
plt.plot(y,U_sp_averaged/u_tau)
plt.xlabel(r"$y/\delta$")
plt.ylabel(r"$U^+=U/u_\tau$")
plt.title("Spatial averaged U profile compared with reference")


############################################################
### calculating wall shear stress  tau_wall=mu * du/dy

Du=U_sp_averaged[1]-U_sp_averaged[0]
Dy=y[1]-y[0]
mu=1/4200
tau_w=mu*Du/Dy
print(f"wall shear stress calculated from velocity profile is {tau_w}")