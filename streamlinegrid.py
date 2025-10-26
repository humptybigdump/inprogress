"""
Functions to generate streamline-oriented grids and simulate transport on them 
(c) Olaf A. Cirpka, University of Tübingen, Department of Geosciences
April 2025
"""

import numpy as np
from scipy.interpolate import interp1d, RegularGridInterpolator
import matplotlib.pyplot as plt
from types import SimpleNamespace
import scipy.sparse as sp

# =============================================================================
# Construction of Streamline-Oriented Grid
# =============================================================================
def slgrid(ntube, nsec, nx, dx, psi, h, phiin, Qin):
    
    # nodal coordinates
    xvec = np.arange(nx[0]+1)*dx[0]
    yvec = np.arange(nx[1]+1)*dx[1]
    (X,Y)=np.meshgrid(xvec,yvec)
    
    # Compute contour lines of streamlines
    fig, ax = plt.subplots()
    contours = ax.contour(X, Y, psi, levels=np.linspace(0, Qin, ntube + 1))

    # Extract contour paths
    Cpsi = {level: segs for level, segs in zip(contours.levels, contours.allsegs)}

    plt.close(fig)  # Prevents figure from displaying    
    
    # Initialize net variables
    net = SimpleNamespace(
        x=np.zeros((ntube + 1, nsec + 1)),
        y=np.zeros((ntube + 1, nsec + 1))
    )
    net.phi, net.psi = np.meshgrid(np.linspace(phiin, 0, nsec + 1), np.linspace(0, Qin, ntube + 1))
    
    # Discretization of phi
    phi_int = np.linspace(phiin, 0, nsec + 1)
    
    # Extract contour line information
    line_x, line_y, line_phi = {}, {}, {}
    # npts = []
    
    for i, (level, paths) in enumerate(Cpsi.items()):
        for path in paths:
            x_vals, y_vals = path[:, 0], path[:, 1]
            line_x[i] = x_vals
            line_y[i] = y_vals
            mask = line_x[i]<0
            line_x[i][mask]=0
            mask = line_x[i]>nx[0]*dx[0]
            line_x[i][mask]=nx[0]*dx[0]
            mask = line_y[i]<0
            line_y[i][mask]=0
            mask = line_y[i]>nx[1]*dx[1]
            line_y[i][mask]=nx[1]*dx[1]
    #        npts.append(len(x_vals))
    
    # npts_max = max(npts)
    # Convert to arrays and interpolate phi values
    h_interpolator = RegularGridInterpolator((xvec,yvec), h.T, method='linear')
    
    # Convert to arrays and interpolate phi values
    for i in range(ntube + 1):
        interp_phi  = h_interpolator(np.array([line_x[i], line_y[i]]).T)
        line_phi[i] = interp_phi
        
    # Fix first and last line
    line_x[0]   = xvec
    line_y[0]   = np.zeros(nx[0]+1)
    line_phi[0] = h[0,:]
    line_x[ntube]   = xvec
    line_y[ntube]   = np.ones(nx[0]+1)*nx[1]*dx[1]
    line_phi[ntube] = h[-1,:]
        
    # if np.any(np.diff(line_phi[i]) <= 0):
    #    return None, True
    
    # Interpolate x and y positions
    for i in range(ntube + 1):
        # print(f'line {i}')
        f_x = interp1d(line_phi[i][-1::-1], line_x[i][-1::-1], kind='linear', fill_value='extrapolate')
        f_y = interp1d(line_phi[i][-1::-1], line_y[i][-1::-1], kind='linear', fill_value='extrapolate')
        net.x[i, :] = f_x(phi_int)
        net.y[i, :] = f_y(phi_int)
        
        # if np.any(np.diff(line_phi[i]) <= 0):
        #    return None, True
    
    # Fix boundaries
    net.x[:, 0] = 0
    net.x[:, -1] = dx[0] * nx[0]
    net.y[0, :] = 0
    net.y[-1, :] = dx[1] * nx[1]
    
    return net

# =============================================================================
# Compute the areas of quadrilateral cells on a structured, irregular grid
# using the shoelace formula
# X, Y: x- and y-coordinates of the vertices as (ny+1,nx+1) numpy-arrays
# returns the areas as (ny,nx) numpy-arrays
# =============================================================================
def quad_cell_areas(X, Y):
    # Get corners of each cell
    x0 = X[:-1, :-1]  # bottom-left
    x1 = X[:-1, 1:]   # bottom-right
    x2 = X[1:, 1:]    # top-right
    x3 = X[1:, :-1]   # top-left

    y0 = Y[:-1, :-1]
    y1 = Y[:-1, 1:]
    y2 = Y[1:, 1:]
    y3 = Y[1:, :-1]

    # Shoelace formula for each quadrilateral cell
    area = 0.5 * np.abs(
        x0 * y1 - x1 * y0 +
        x1 * y2 - x2 * y1 +
        x2 * y3 - x3 * y2 +
        x3 * y0 - x0 * y3
    )

    return area  # shape (ny, nx)

# =============================================================================
# Compute storage matrix for ADE on the streamline-oriented grid
# =============================================================================
def store_mat(net,poros):
    nel= np.prod(np.array(net.x.shape)-1)
    area = quad_cell_areas(net.x, net.y).reshape(nel)
    Mstore = sp.diags(area*poros, 0, format='csr')
    return Mstore
    
# =============================================================================
# Compute mobility matrix for ADE on the streamline-oriented grid
# =============================================================================

def mob_mat(net, al, at, Dm, por, Dttype):
    ntube, nsec = net.x.shape[0]-1, net.x.shape[1]-1
    Qin = net.psi[-1,0]
    q = np.zeros(ntube * nsec)
    itot = np.zeros(5 * ntube * nsec, dtype=int)
    jtot = np.zeros(5 * ntube * nsec, dtype=int)
    Atot = np.zeros(5 * ntube * nsec)

    n_el  = (ntube, nsec)
    n_pts = (ntube + 1, nsec + 1)
    nel   = np.prod(n_el)
    npts  = np.prod(n_pts)
    
    if type(por)==float:
       por = por*np.ones(nel)
    else:
       por = por.reshape(nel)

    # Index helpers
    incidence_el = np.array([0, 0, 1, 1]) + n_pts[1] * np.array([0, 1, 0, 1])
    
    # Generate full element and point arrays
    all_el  = np.arange(nel).reshape(n_el)
    all_pts = np.arange(npts).reshape(n_pts)
    el2pts  = all_pts[:ntube, :nsec].reshape(nel)
    
    lole = el2pts + incidence_el[0]
    uple = el2pts + incidence_el[1]
    lori = el2pts + incidence_el[2]
    upri = el2pts + incidence_el[3]

    # Coordinates of vertices as vectors
    x = net.x.reshape(npts)
    y = net.y.reshape(npts)

    def dist(i, j): return np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)

    w_lef = dist(lole, uple)
    w_rig = dist(lori, upri)
    w_bot = dist(lole, lori)
    w_top = dist(uple, upri)

    # Cell centers
    xcen = 0.25 * (x[lole] + x[uple] + x[lori] + x[upri])
    ycen = 0.25 * (y[lole] + y[uple] + y[lori] + y[upri])
    xlef = 0.5  * (x[lole] + x[uple])
    ylef = 0.5  * (y[lole] + y[uple])
    xrig = 0.5  * (x[lori] + x[upri])
    yrig = 0.5  * (y[lori] + y[upri])
    xbot = 0.5  * (x[lole] + x[lori])
    ybot = 0.5  * (y[lole] + y[lori])
    xtop = 0.5  * (x[uple] + x[upri])
    ytop = 0.5  * (y[uple] + y[upri])

    # Velocity and geometry
    width = 0.5 * (w_lef + w_rig)
    q = (Qin / ntube) / width
    # q = q.reshape(ntube, nsec)

    # Hydraulic conductivity and effective grain size
    lengthel = 0.5 * (w_bot + w_top)
    deltaphi = net.phi[0, 0] - net.phi[0, 1]
    K = np.abs(q * lengthel / deltaphi)
    d_eff = np.sqrt(100 * K)/ 1000
    # Peclet number in each cell
    Pe = d_eff * q / por / Dm

    # transverse dispersion coefficient times porosity in each cell
    if Dttype == 1:   # standard Scheidegger model with constant at
        Dt = at*q + Dm*por**2
    elif Dttype == 2: # standard Scheidegger model with at = d_eff/10
        Dt = 0.1*d_eff*q + Dm*por**2
    elif Dttype == 3: # Chiogna model
        Dt = d_eff/np.sqrt(123 + Pe)*q + Dm*por**2
    else:
        raise ValueError("Invalid Dttype")

    # CONNECTION TO LEFT CELL (flux across left edge)
    # all cells that have a left neighbor
    here   = all_el[:,1:].reshape(ntube*(nsec-1))
    # all left neighbors
    left   = all_el[:,:-1].reshape(ntube*(nsec-1))
    # smallest index of addition to sparse matrix touched here
    ii_min = 0                         
    # largest index of addition to sparse matrix touched here + 1
    ii_max = ii_min + ntube*(nsec-1) 
    # length of line from cell center via left-egde center to 
    # center of left neighbour cell
    length = np.sqrt((xlef[here]-xcen[left])**2 + 
                     (ylef[here]-ycen[left])**2) + \
             np.sqrt((xlef[here]-xcen[here])**2 + 
                     (ylef[here]-ycen[here])**2)
    # porosity at the edge
    poredge  = 0.5 * (por[here] + por[left])
    # longitudinal dispersive flux across left edge
    aha      = (Qin/ntube*al + Dm*w_lef[here]*poredge**2)/length
    # preparing sparse matrix
    itot[ii_min:ii_max] = here
    jtot[ii_min:ii_max] = left
    Atot[ii_min:ii_max] = -Qin/ntube-aha # advective and long.-dispersive flux
    # summing up all edge terms
    huhu       = np.zeros(nel)
    huhu[here] = aha
    
    # CONNECTION TO LOWER CELL (flux across lower edge)
    # all cells that have a lower neighbor
    here   = all_el[1:,:].reshape((ntube-1)*nsec)
    # all lower neighbors
    belo   = all_el[:-1,:].reshape((ntube-1)*nsec)      
    # smallest index of addition to sparse matrix touched here
    ii_min = ii_max
    # largest index of addition to sparse matrix touched here + 1
    ii_max = ii_min + (ntube-1)*nsec
    # length of line from cell center to lower-egde center in neighbor cell
    lenbelo = np.sqrt((xbot[here]-xcen[belo])**2 + (ybot[here]-ycen[belo])**2)
    # length of line from cell center to lower-egde center in this cell
    lenhere = np.sqrt((xbot[here]-xcen[here])**2 + (ybot[here]-ycen[here])**2)
    # transverse dispersive flux across lower edge with harmonic weighting of Dt
    aha = w_bot[here]/(lenhere/Dt[here]+lenbelo/Dt[belo])
    # preparing sparse matrix
    itot[ii_min:ii_max] = here
    jtot[ii_min:ii_max] = belo
    Atot[ii_min:ii_max] = -aha # only transverse dispersive flux
    # summing up all edge terms
    huhu[here] += aha

    # CONNECTION TO UPPER CELL (flux across upper edge)
    # all cells that have an upper neighbor
    here   = all_el[:-1,:].reshape((ntube-1)*nsec)
    # all upper neighbors
    abov   = all_el[1:,:].reshape((ntube-1)*nsec) 
    # smallest index of addition to sparse matrix touched here
    ii_min = ii_max
    # largest index of addition to sparse matrix touched here + 1
    ii_max = ii_min + (ntube-1)*nsec
    # length of line from cell center to upper-egde center in neighbor cell
    lenabov = np.sqrt((xtop[here]-xcen[abov])**2 + (ytop[here]-ycen[abov])**2)
    # length of line from cell center to upper-egde center in this cell
    lenhere = np.sqrt((xtop[here]-xcen[here])**2 + (ytop[here]-ycen[here])**2)
    # transverse dispersive flux across lower edge with harmonic weighting of Dt
    aha     = w_top[here]/(lenhere/Dt[here]+lenabov/Dt[abov])
    # preparing sparse matrix
    itot[ii_min:ii_max] = here
    jtot[ii_min:ii_max] = abov
    Atot[ii_min:ii_max] = -aha # only transverse dispersive flux
    # summing up all edge terms
    huhu[here] += aha
    
    # CONNECTION TO RIGHT CELL (flux across right edge)
    # all cells that have a right neighbor
    here   = all_el[:,:-1].reshape(ntube*(nsec-1))
    # all right neighbors
    righ   = all_el[:,1:].reshape(ntube*(nsec-1)) 
    # smallest index of addition to sparse matrix touched here
    ii_min = ii_max
    # largest index of addition to sparse matrix touched here + 1
    ii_max = ii_min + ntube*(nsec-1)
    # length of line from cell center via left-egde center 
    # to center of left neighbour cell
    length = np.sqrt((xrig[here]-xcen[righ])**2 + 
                     (yrig[here]-ycen[righ])**2) + \
             np.sqrt((xrig[here]-xcen[here])**2 + 
                     (yrig[here]-ycen[here])**2)
    # longitudinal dispersive flux across left edge
    poredge = 0.5*(por[here]+por[righ])
    aha     = (Qin/ntube*al+Dm*w_rig[here]*poredge**2)/length
    # preparing sparse matrix
    itot[ii_min:ii_max] = here
    jtot[ii_min:ii_max] = righ
    Atot[ii_min:ii_max] = -aha # only longitudinal dispersive flux
    # summing up all edge terms
    huhu[here]  += aha
    
    # MAIN DIAGONAL
    #  smallest index of addition to sparse matrix touched here
    ii_min = ii_max
    # largest  index of addition to sparse matrix touched here
    ii_max = ii_min + nel
    itot[ii_min:ii_max] = all_el.reshape(nel)
    jtot[ii_min:ii_max] = all_el.reshape(nel)
    Atot[ii_min:ii_max] = Qin/ntube+huhu


    # Construct sparse matrix - left, bottom, top, right, and diagonal
    # Note: Due to space and clarity, sparse construction logic is omitted here
    # Let me know if you'd like the full matrix assembly section added!

    # Final sparse matrix assembly
    Mmob = sp.csr_matrix((Atot[:ii_max], (itot[:ii_max], jtot[:ii_max])), 
                         shape=(nel, nel))
    return Mmob
