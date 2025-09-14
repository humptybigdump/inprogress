import numpy as np
from scipy.sparse import csc_matrix # for sparse matrix
from scipy.sparse.linalg import spsolve # for sparse matrix
#from numba import jit

A_poisson = 0

#@jit
def get_star(us, vs, un, vn, pn, m, dt, re):
    
    # Solve momentum equation
    for ix in range(1,m.nx):  # cycle for horizontal component
        for iy in range(m.ny):
            
            #    WARNING!! ATTENTION!!
            # 
            #    This is the coordinate system for the cell (i,j) in Python
            #
            #    --------------
            #    |            |
            #    |            |
            #    |            |
            #    Ui,j+1 Pi,j  |
            #    |            | 
            #    |            |
            #    |            |
            #    ----Vi+1,j----
            #
            #
            #    and this is the local coordinate system like fig. 21 in § 7.5 of the script
            #
            #    --------------
            #    |            |
            #    |            |
            #    |            |
            #    Uij   Pij    |
            #    |            | 
            #    |            |
            #    |            |
            #    ------Vij-----
            #
            #
        
            #    To simpify the expression below, I define some variable with the sintax
            #    u_ij, where the letters used here refer to the local coordinate system
            u_ij     = un[ix,iy+1]
            u_ijp1   = un[ix,iy+2]
            u_ijm1   = un[ix,iy]
            u_ip1j   = un[ix+1,iy+1]
            u_im1j   = un[ix-1,iy+1]
            v_im1jp1 = vn[ix,iy+1]
            v_ijp1   = vn[ix+1,iy+1]
            v_ij     = vn[ix+1,iy]
            v_im1j   = vn[ix,iy]
            p_ij     = pn[ix,iy]
            p_im1j   = pn[ix-1,iy]
            
            us[ix,iy+1] = u_ij + dt * ( \
                             - ((u_ip1j + u_ij)**2 - (u_im1j + u_ij)**2)/(4*m.dx) \
                             - ((u_ijp1 + u_ij)*(v_ijp1 + v_im1jp1) - (u_ijm1 + u_ij)*(v_ij + v_im1j)) / (4*m.dy) \
                             -  (p_ij - p_im1j) / m.dx \
                             + ((u_ip1j + u_im1j - 2*u_ij)/(m.dx*m.dx) + (u_ijm1 + u_ijp1 - 2*u_ij)/(m.dy*m.dy)) / re \
                                        )
                
    for ix in range(m.nx): # cycle for vertical component
        for iy in range(1,m.ny):

            # Same index caution to be used as for the u-momentum equations
            v_ij     = vn[ix+1,iy]
            v_ip1j   = vn[ix+2,iy]
            v_im1j   = vn[ix,iy]
            v_ijp1   = vn[ix+1,iy+1]
            v_ijm1   = vn[ix+1,iy-1]
            u_ij     = un[ix,iy+1]
            u_ip1jm1 = un[ix+1,iy]
            u_ip1j   = un[ix+1,iy+1]
            u_ijm1   = un[ix,iy]
            p_ij     = pn[ix,iy]
            p_ijm1   = pn[ix,iy-1]      
            
            vs[ix+1,iy] = v_ij + dt * (\
                             - ((u_ip1jm1 + u_ip1j)*(v_ip1j + v_ij) - (u_ijm1 + u_ij)*(v_ij + v_im1j))/(4*m.dx) \
                             - ((v_ijp1 + v_ij)**2 - (v_ij + v_ijm1)**2)/(4*m.dy) \
                             -  (p_ij - p_ijm1) / m.dy \
                             + ((v_ip1j + v_im1j - 2*v_ij)/(m.dx*m.dx) + (v_ijp1 + v_ijm1 - 2*v_ij)/(m.dy*m.dy)) / re \
                                         )
                
    # Adjust boundary condition (ghost cells)
    us[1:-1,-1] = 2 - us[1:-1,-2] 
    us[1:-1,0]  = - us[1:-1,1]
    
    vs[0,1:-1]  = - vs[1,1:-1]
    vs[-1,1:-1] = - vs[-2,1:-1]
    
    return us,vs

def get_star_slice(us, vs, un, vn, pn, m, dt, re):
    
    us[1:-1,1:-1] = un[1:-1,1:-1] + dt * (\
                             - ( (un[2:,1:-1]  + un[1:-1,1:-1])**2 - (un[:-2,1:-1] + un[1:-1,1:-1])**2 ) / (4*m.dx) \
                             - ( (un[1:-1,2:]  + un[1:-1,1:-1])*(vn[1:-2,1:]  + vn[2:-1,1:])\
                               - (un[1:-1,:-2] + un[1:-1,1:-1])*(vn[1:-2,:-1] + vn[2:-1,:-1])\
                               ) / (4*m.dy) \
                             - (pn[1:,:] - pn[:-1,:] ) / m.dx \
                             + ( (un[2:,1:-1] + un[:-2,1:-1] - 2*un[1:-1,1:-1])/(m.dx*m.dx) \
                               + (un[1:-1,2:] + un[1:-1,:-2] - 2*un[1:-1,1:-1])/(m.dy*m.dy) \
                               ) / re \
                            )
              
    vs[1:-1,1:-1] = vn[1:-1,1:-1] + dt * (\
                             - ( (un[1:,2:-1]  + un[1:,1:-2] )*(vn[2:,1:-1]   + vn[1:-1,1:-1]) \
                               - (un[:-1,2:-1] + un[:-1,1:-2])*(vn[1:-1,1:-1] + vn[:-2,1:-1])\
                               ) / (4*m.dx) \
                             - ( (vn[1:-1,2:] + vn[1:-1,1:-1])**2 - (vn[1:-1,1:-1] + vn[1:-1,:-2])**2) / (4*m.dy) \
                             -  (pn[:,1:]  - pn[:,:-1]) / m.dy \
                             + ( (vn[2:,1:-1] + vn[:-2,1:-1] - 2*vn[1:-1,1:-1])/(m.dx*m.dx) \
                               + (vn[1:-1,2:] + vn[1:-1,:-2] - 2*vn[1:-1,1:-1])/(m.dy*m.dy) \
                               ) / re \
                            )
         
                
    # Adjust boundary condition (ghost cells)
    us[1:-1,-1] = 2 - us[1:-1,-2] 
    us[1:-1,0]  = - us[1:-1,1]
    
    vs[0,1:-1]  = - vs[1,1:-1]
    vs[-1,1:-1] = - vs[-2,1:-1]
    
    return us,vs

def get_poisson_matrix(m):

    global A_poisson

    # allocation
    A = np.zeros((m.nx*m.ny,m.nx*m.ny))

    for ii in range(m.nx*m.ny): # cycle over rows of A

        north, south, west, east = m.get_compass(ii) # get indices of neighbouring points
        boundary, _, _, _ = m.is_boundary(ii) # assess whether you are on a boundary

        A[ii, ii] = - 2/(m.dx)**2 - 2/(m.dy)**2 # diagonal terms always have this,
                                                # no matter what

        if not boundary: # points inside the domain

            A[ii, north] = 1/(m.dy)**2
            A[ii, south] = 1/(m.dy)**2
            A[ii, west ] = 1/(m.dx)**2
            A[ii, east ] = 1/(m.dx)**2

        else: # points on the boundary

            if 'n' in boundary: # if on northern boundary
                A[ii,ii] += 1/(m.dy)**2 # trick for b.c.
            else: # if not on northern boundary
                A[ii, north] = 1/(m.dy)**2 # normal expression

            if 's' in boundary: # if on southern boundary
                A[ii,ii] += 1/(m.dy)**2 # trick for b.c.
            else: # if not on southern boundary
                A[ii, south] = 1/(m.dy)**2 # normal expression
            
            if 'w' in boundary: # if on western boundary
                A[ii,ii] += 1/(m.dx)**2 # trick for b.c.
            else: # if not on western boundary
                A[ii, west ] = 1/(m.dx)**2 # normal expression

            if 'e' in boundary: # if on eastern boundary
                A[ii,ii] += 1/(m.dx)**2 # trick for b.c.
            else: # if not on eastern boundary
                A[ii, east ] = 1/(m.dx)**2 # normal expression

    A_poisson = csc_matrix(A) # update global variable



#@jit
def solve_poisson(m, us, vs, pc, dt):

    # calculate divergence of u*

    b = np.zeros(m.nx*m.ny)

    for ii, _ in enumerate(b):
        ix, iy = m.get_mat_pos(ii) # get actual indices
        u = lambda i, j : us[ix+i,iy+j+1]
        v = lambda i, j : vs[ix+i+1,iy+j]
        b[ii] = (u(1,0) - u(0,0))/m.dx + (v(0,1) - v(0,0))/m.dy

    b /= dt

    # then solve system
    pc = spsolve(A_poisson, b).reshape(m.nx,m.ny)

    return pc

#@jit
def solve_poisson_slice(m, us, vs, pc, dt):

    # calculate divergence of u*
    b = ( (us[1:,1:-1] - us[:-1,1:-1]) / m.dx + (vs[1:-1,1:] - vs[1:-1,:-1]) / m.dy ).flatten()

    b /= dt

    # then solve system
    pc = spsolve(A_poisson, b).reshape(m.nx,m.ny)

    return pc
