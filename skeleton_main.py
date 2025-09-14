import numpy as np
from fractional_step import get_star, get_poisson_matrix, solve_poisson
from mesh_utils import rectangular_mesh
from matplotlib import pyplot as plt
from progressbar import progressbar


# Inputs & Parameters
# -------------------------------------------

ly_lx = 1.0            # ratio between ly and lx (ly/lx)

nx = 25; ny = 25       # number of cells within the computational domain,
                       # i.e. excluding the ghost cells
                       
re = 400               # utop * lx / nu

dt = 0.01              # time step

f_snap = 5             # 

t_final = 1            # TODO: increase time step once your script is working

# Initialisations 
# -------------------------------------------
dx = 1 / nx

dy = ly_lx / ny

time_array = np.arange(0, t_final, dt)

class pressure_mesh(rectangular_mesh):
    def __init__(self, nx, lx, ny, ly):

        self.nx = nx # save nx into class
        self.lx = lx # save lx into class
        self.ny = ny # save ny into class
        self.ly = ly # save nx into class

        # generate mesh
        self.x_cells = np.linspace(0, self.lx, self.nx+1)
        self.x = (self.x_cells[0:self.nx] + self.x_cells[1:(self.nx+1)])/2
        self.y_cells = np.linspace(0, self.ly, self.ny+1)
        self.y = (self.y_cells[0:self.ny] + self.y_cells[1:(self.ny+1)])/2

        # calculate mesh resolution
        self.dx = lx/nx
        self.dy = ly/ny

m = pressure_mesh(nx, 1, ny, ly_lx) # this is the mesh for the pressure!


get_poisson_matrix(m)


# allocate arrays
pn  = np.zeros((nx,ny)) # nx, ny are the dimensions of the pressure mesh
pc  = np.zeros_like(pn)
uplot = np.zeros_like(pn)
vplot = np.zeros_like(pn)

un  = np.zeros((?,?)) # TODO: fill me in!
us  = np.zeros_like(un) 

vn  = np.zeros((?,?)) # TODO: fill me in!
vs  = np.zeros_like(vn) 


# Time loop
# -------------------------------------------
for i,t in enumerate(progressbar(time_array)):

    # TODO: fill me in!

    # get fields ready for plotting:
    # we want the values of u and v on the pressure cells,
    # we calculate them by interpolation
    uplot[:,:] = ((un[0:-1, 1:-1] + un[1:,1:-1])/2).transpose()
    vplot[:,:] = ((vn[1:-1,0:-1] + vn[1:-1,1:])/2).transpose()

    # plot
    if i % f_snap == 0:
        fig, ax = plt.subplots()
        ax.pcolormesh(m.x_cells,m.y_cells,pn.transpose())
        ax.set_aspect('equal', 'box')
        ax.set_xlim([m.x_cells[0], m.x_cells[-1]])
        ax.set_ylim([m.y_cells[0], m.y_cells[-1]])
        ax.streamplot(m.x, m.y, uplot, vplot, color='white')
        fig.savefig('figs/t_'+str(round(i/f_snap,0)).replace('.','_')+'.png', format='png')
        plt.close(fig)