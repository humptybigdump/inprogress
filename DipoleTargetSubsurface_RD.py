## Last touched 16.05.2023 (RD)
## ----------------------------
## Let's do the standard imports
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as lcolors
from matplotlib.colors import LinearSegmentedColormap

# Define the red-white-blue colormap
colors = [
    (1, 0, 0),    # red
    (1, 1, 1),    # white
    (0, 0, 1)     # blue
]

# Define the custom colormap
rdblue = (0.015, 0.85, 1)
rdred =  (1, 0.19, 0.19)
neon_green = (57/255, 255/255, 20/255)
cmapRD2 = lcolors.LinearSegmentedColormap.from_list(
    'black_red_blue', ['blue', 'black','red'], N=256)

# Create the colormap
cmapRD = LinearSegmentedColormap.from_list("red_white_blue", colors, N=256)

## This is a function, returning the value of a H field at r and theta from the origin
## where the magnetic dipole is located. Assume volume Magnetization M [A/m] parallel to external field.
def B(r, theta,M):
    """Return t,he magnetic field vector at (r, theta)."""
    fac = (M / r)**3
    return 2 * fac * np.cos(theta + alpha), fac * np.sin(theta + alpha)

#Background field strength in nTesla somewhat comparable to Tuebingen
Bfm = 40000;

# Induced Magnetization in A/m*mu_0; this is target material and geometry dependent
M =  100

# Deviation of magnetic pole from vertical axis,
alpha = np.radians(-65)



# Grid of x, y points on a Cartesian grid in m
nx, ny = 200, 200
XMAX, YMAX = 20, 20
x = np.linspace(-XMAX, XMAX, nx)
y = np.linspace(-YMAX, YMAX, ny)
X, Y = np.meshgrid(x, y)
r, theta = np.hypot(X, Y), np.arctan2(Y, X)

#Depth of the object (we move the surface relative to it)
Depth=5;
IndDepth=np.argmin(abs(y-Depth))

# Magnetic field vector, B = (Ex, Ey), as separate components
Br, Btheta = B(r, theta,M)
# Transform to Cartesian coordinates: NB make North point up, not to the right.
c, s = np.cos(np.pi/2 + theta), np.sin(np.pi/2 + theta)
Bx = -Btheta * s + Br * c
By = Btheta * c + Br * s
Bm = np.sqrt(Bx**2+By**2)

## Earth's Background Field is considered constant over the region of interest
## Scale it to about 40 000 nT
Bex = Bx*0+np.cos(-np.pi/2-alpha)*Bfm
Bey = Bx*0+np.sin(-np.pi/2-alpha)*Bfm
Bem = np.sqrt(Bex**2+Bey**2)


## Total Field
Btx = Bx + Bex
Bty = By + Bey
Btm = np.sqrt(Btx**2+Bty**2)
# Btm = Btm
# Btx = Btx
# Bty = Bty

## Total Field Approximatino assuming that Be >> B: B_T = B*\hat(B_E)

Btm_approx = (Bex*Bx + Bey*By)/Bfm
BtmAnomaly = Btm - Bem

normrd = lcolors.SymLogNorm(
    linthresh=1e-2,  # threshold near 0 where the norm is linear
    linscale=1.0,    # scale of the linear region
    # vmin=BtmAnomaly.min(),
    # vmax=BtmAnomaly.max(),
    vmin = -1e8,
    vmax = 1e8,
    base=10
)

## Visualizes
font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : 15}

matplotlib.rc('font', **font)


fig = plt.figure(figsize=(20,8),facecolor='black')
grid = plt.GridSpec(3, 2, wspace=0.4, hspace=0.3)


ax1 = fig.add_subplot(grid[:,1],facecolor='black')
ax2 = fig.add_subplot(grid[0,0],facecolor='black')
ax3 = fig.add_subplot(grid[1,0],facecolor='black')
ax4 = fig.add_subplot(grid[2,0],facecolor='black')

#fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1)

# Plot the induced dipole and the background field
#color = 2 * np.log(np.hypot(Bx, By))
print(BtmAnomaly.min(), BtmAnomaly.max())   
pc = ax1.pcolor(x,y,BtmAnomaly,cmap=cmapRD2,vmin=-1e4,vmax=1e4, shading='auto')
#norm=lcolors.LogNorm(vmin=BtmAnomaly.min()/1000, vmax=BtmAnomaly.max()/1000
cbar = fig.colorbar(pc, ax=ax1)
cbar.set_label('Total Anomaly (nT)', color='white')
#plt.colorbar(label='Total field (nT)', pad=0.01, shrink=0.8, aspect=10)
ax1.streamplot(x, y, Bx, By, color=neon_green, linewidth=1,
              density=1, arrowstyle='->', arrowsize=1.5)
ax1.streamplot(x, y, Bex, Bey, color=rdblue, linewidth=2,
              density=0.4, arrowstyle='->', arrowsize=1.5)
ax1.plot(x,x*0+y[IndDepth],color='w', lw=4)
ax1.plot(0,0,'x',color=neon_green, linewidth=5, markeredgewidth=4,markersize=15)
ax1.text(-XMAX-7.5, y[IndDepth]+0.5,'Surface', color='white', fontsize=15)

ax1.set_xlabel('Distance',color='white')
ax1.set_ylabel('Depth',color='white')
ax1.set_xlim(-XMAX, XMAX)
ax1.set_ylim(-YMAX, YMAX)
ax1.spines['left'].set_color('white')
ax1.spines['bottom'].set_color('white')
#ax[1].set_aspect('equal')

ax2.plot(x,(Btm[IndDepth,:]-Btm[IndDepth,0]),color=rdblue,linewidth=2) ## in nT
#ax2.plot(x,(Btm_approx[IndDepth,:]-Btm_approx[IndDepth,0]),'kx') ## in nT
for spine in ['top', 'right']:
    ax2.spines[spine].set_visible(False)
ax2.ticklabel_format(useOffset=False)

ax2.axhline(y=0.0, color='w', linestyle='--')
ax2.axvline(x=0.0, color='w', linestyle='--')
ax2.set_ylabel('Total anomaly (nT)',color='white')
ax2.set_title('Anomalies at Surface',color='white')
ax2.spines['left'].set_color('white')
ax2.spines['bottom'].set_color('white')

ax3.plot(x,Bty[IndDepth,:]-Bty[IndDepth,0],color=rdblue,linewidth=2)
ax3.axhline(y=0.0, color='white', linestyle='--')
ax3.axvline(x=0.0, color='w', linestyle='--')
ax3.set_xticks([])
ax3.set_ylabel('Vertical (nT)',color='white')
for spine in ['top', 'right']:
    ax3.spines[spine].set_visible(False)
ax3.spines['left'].set_color('white')
ax3.spines['bottom'].set_color('white')

ax4.plot(x,Btx[IndDepth,:]-Btx[IndDepth,0],color=rdblue,linewidth=2)
ax4.axhline(y=0.0, color='white', linestyle='--')
ax4.axvline(x=0.0, color='w', linestyle='--')
for spine in ['top', 'right']:
    ax4.spines[spine].set_visible(False)
ax4.set_ylabel('Horizontal (nT)',color='white')
ax4.set_xlabel('Distance',color='white')
ax4.spines['left'].set_color('white')
ax4.spines['bottom'].set_color('white')
for ax in [ax2, ax3, ax4]:
    ax.tick_params(axis='both', colors='white')
    ax.set_yticks([0])
    ax.set_xticks([0])
plt.tight_layout()
plt.savefig('figout.png',bbox_inches='tight',dpi=300)
plt.show()