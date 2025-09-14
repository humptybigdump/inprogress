import numpy as np
from fractional_step import get_star, get_star_slice, get_poisson_matrix, solve_poisson, solve_poisson_slice
from mesh_utils import rectangular_mesh
from matplotlib import pyplot as plt
from progressbar import progressbar


# Inputs & Parameters
# -------------------------------------------

ly_lx = 1.0              # ratio between ly and lx (ly/lx)

nx = 100; ny = 100       # number of cells within the computational domain,
                       # i.e. excluding the ghost cells
                       
re = 400               # utop * lx / nu

dt = 0.01             # time step

f_snap = 5             # 

t_final = dt*25        # 

islice = True  # False: use for loops in get_star and solve_poisson; True: use slicing

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
pn  = np.zeros((nx,ny)) 
pc  = np.zeros_like(pn)
uplot = np.zeros_like(pn)
vplot = np.zeros_like(pn)

un  = np.zeros((nx+1,ny+2)) # horizontal component is (Nx + 1) * Ny
us  = np.zeros_like(un) 

vn  = np.zeros((nx+2,ny+1)) # vertical component is Nx * (Ny + 1)
vs  = np.zeros_like(vn) 


# Time loop
# -------------------------------------------
for i,t in enumerate(progressbar(time_array)):

    if islice: 
        us, vs = get_star_slice(us, vs, un, vn, pn, m, dt, re) # evolve un to get u*
        pc = solve_poisson_slice(m, us, vs, pc, dt) # solve poisson equation to find pc
    else: 
        us, vs = get_star(us, vs, un, vn, pn, m, dt, re) # evolve un to get u*
        pc = solve_poisson(m, us, vs, pc, dt) # solve poisson equation to find pc

    un[1:-1,1:-1] = us[1:-1,1:-1] - dt/m.dx * (pc[1:m.nx, :] - pc[0:(m.nx-1), :])

    vn[1:-1,1:-1] = vs[1:-1,1:-1] - dt/m.dy * (pc[:, 1:m.ny] - pc[:, 0:(m.ny-1)])
    
    pn += pc # update pressure field as well
    
    # Adjust boundary condition
    un[1:-1,-1] = 2 - un[1:-1,-2] 
    un[1:-1,0]  = - un[1:-1,1]
    
    vn[0,1:-1]  = - vn[1,1:-1]
    vn[-1,1:-1] = - vn[-2,1:-1]

    # get plottable fields by interpolation
    uplot[:,:] = ((un[0:-1, 1:-1] + un[1:,1:-1])/2).transpose()
    vplot[:,:] = ((vn[1:-1,0:-1] + vn[1:-1,1:])/2).transpose()

    # plot
    if i % f_snap == 0:
        fig, ax = plt.subplots()
        ax.pcolormesh(m.x_cells,m.y_cells,pn.transpose())
        #ax.quiver(x_quiver, y_quiver, uplot, vplot)
        ax.set_aspect('equal', 'box')
        ax.set_xlim([m.x_cells[0], m.x_cells[-1]])
        ax.set_ylim([m.y_cells[0], m.y_cells[-1]])
        ax.streamplot(m.x, m.y, uplot, vplot, color='white')
        fig.savefig('figs/t_'+str(round(i/f_snap,0)).replace('.','_')+'.png', format='png')
        plt.close(fig)