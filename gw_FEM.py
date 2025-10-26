import numpy as np
import scipy.sparse as sp
# import time

"""
Evaluate mobility matrix for groundwater flow equation using 
linear conforming Finite Elements
Numbering of nodes according to numpy standard (row-wise) 
"""
def mat(K,dx,dy):
    ny, nx = K.shape
    nnod = (ny+1)*(nx+1)
    row, col = np.zeros(ny*nx*16).astype(int), np.zeros(ny*nx*16).astype(int) 
    data     = np.zeros(ny*nx*16)
    """ node indices of element matrix
        (mm,mm) (mm,pm) (mm,mp) (mm,pp)
        (pm,mm) (pm,pm) (pm,mp) (pm,pp)
        (mp,mm) (mp,pm) (mp,mp) (mp,pp)
        (pp,mm) (pp,pm) (pp,mp) (pp,pp)"""
    M_h_el  = dy/dx/6. *  \
              np.array([[+2., +1., -2., -1.], \
                        [+1., +2., -1., -2.], \
                        [-2., -1., +2., +1.], \
                        [-1., -2., +1., +2.]]) + \
              dx/dy/6. * \
              np.array([[+2., -2., +1., -1.], \
                        [-2., +2., -1., +1.], \
                        [+1., -1., +2., -2.], \
                        [-1., +1., -2., +2.]])
    counter=0
    for i in range(ny):       # row index
        for j in range(nx):   # column index
            # indices of nodes
            mm = i*(nx+1) +j  # lower left node
            pm = mm+nx+1      # upper left node
            mp = mm+1         # lower right node
            pp = pm+1         # upper right node
            row[counter:counter+16] = [mm,mm,mm,mm,\
                                       pm,pm,pm,pm,\
                                       mp,mp,mp,mp,\
                                       pp,pp,pp,pp]
            col[counter:counter+16] = [mm,pm,mp,pp,\
                                       mm,pm,mp,pp,\
                                       mm,pm,mp,pp,\
                                       mm,pm,mp,pp]
            data[counter:counter+16]= M_h_el.reshape(16)*K[i,j] 
            counter=counter+16
    M = sp.csc_matrix((data, (row, col)), shape=(nnod, nnod))

    return M

"""
Set Dirichlet boundary for groundwater flow
"""
def diri(M,r,nodes,values):
#    tic = time.time()
    rmod = np.copy(r)
    Mmod = M.tolil()
    for i in range(len(nodes)):
        nod = nodes[i]
        nz_indices = M.getcol(nod).nonzero()[0]
        for j in nz_indices:
            rmod[j] -= M[j,nod]*values[i]
            Mmod[j,nod] = 0.
            Mmod[nod,j] = 0.
        Mmod[nod,nod] = 1.
    rmod[nodes]=np.reshape(values,len(values))
#    toc = time.time()
#    print(f"Elapsed time: {toc - tic:.4f} seconds")
    return Mmod.tocsc(), rmod    