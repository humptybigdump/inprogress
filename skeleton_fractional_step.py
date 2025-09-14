import numpy as np
from scipy.sparse import csc_matrix # for sparse matrix
from scipy.sparse.linalg import spsolve # for sparse matrix



A_poisson = 0



def get_star(us, vs, un, vn, pn, m, dt, re):

    # Solve momentum equation
    for ix in range(?,?):  # cycle for horizontal component
        for iy in range(?,?):

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
            #    and this is the local coordinate system like fig. 21 in § 6.5 of the script
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
            
            # Maybe you could define here already some variables so that 
            # the expression below (the equation for us) does not get too nasty
            #
            # One idea could be to use the (i,j) notation of the local coordinate
            # system like in our script or notes and retrieve the variable in the 
            # Python coordinate system

            # fill the discretized u-momentum equation to get u*
            us[?,?] = un[?,?] + dt # * (  ?  )

    for ix in range(m.nx): # cycle for vertical component
        for iy in range(1,m.ny):

            # fill the discretized u-momentum equation to get v*
            vs[?,?] = vn[?,?] + dt # * (  ?  )

    return us,vs



def get_poisson_matrix(m):

    global A_poisson

    # allocation
    A = np.zeros((?,?))

    for ii in range(?): # cycle over rows of A

        north, south, west, east = m.get_compass(ii) # get indices of neighbouring points
        boundary, _, _, _ = m.is_boundary(ii) # assess whether you are on a boundary

        # write coefficients corresponding to central differences
        if not boundary:

            A[ii, ii] = ?
            A[ii, north] = ?
            A[ii, south] = ?
            A[ii, west ] = ?
            A[ii, east ] = ?

        else:

            if 'n' in boundary:
                # ...

            if 's' in boundary:
                # ...

            if 'w' in boundary:
                # ...

            if 'e' in boundary:
                # ...

    A_poisson = csc_matrix(A) # update global variable


def solve_poisson(m, us, vs, pc, dt):

    b = np.zeros(?)

    for ii in range(len(b)):
        ix, iy = m.get_mat_pos(ii) # get actual indices

        b[ii] = ?

    # then solve system
    pc1d = spsolve(A_poisson, b)
    
    # make pc 2D again
    pc = pc1d.reshape(?)

    return pc
