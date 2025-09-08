"""
Numerical inverse Laplace transform using de Hoog's method.

de Hoog, F. R., Knight, J. H., and Stokes, A. N. (1982). An improved 
method for numerical inversion of Laplace transforms. S.I.A.M. J. Sci. 
and Stat. Comput., 3, 357-366.

The time vector is split in segments of equal magnitude
which are inverted individually. This gives a better overall accuracy.

Transferred from matlab to python. Matlab file by 
Karl Hollenbeck
Department of Hydrodynamics and Water Resources
Technical University of Denmark
DK-2800 Lyngby
    
Parameters:
    fhandle: function
        Function handle for the Laplace-space function F(s, *args)
    t: array-like
        Time points where the inverse transform is computed
    alpha: float, optional
        Largest pole of F (default is 0)
    tol: float, optional
        Tolerance level for numerical inversion (default is 1e-9)
    *args: additional arguments
        Extra parameters to pass to F(s)

Returns:
    f: ndarray
        Real-space values of f(t)
"""

import numpy as np

def invlap(fhandle, t, alpha=0, tol=1e-9, *args):
    t = np.asarray(t).flatten()  # Ensure t is a 1D array
    allt = t.copy()
    logallt = np.log10(allt)
    iminlogallt = np.floor(np.min(logallt))
    imaxlogallt = np.ceil(np.max(logallt))
    f_values = []
    
    for ilogt in range(int(iminlogallt), int(imaxlogallt) + 1):
        t_segment = allt[(logallt >= ilogt) & (logallt < ilogt + 1)]
        if len(t_segment) == 0:
            continue  # Skip if no elements in the segment
        
        T = max(t_segment) * 2
        gamma = alpha - np.log(tol) / (2 * T)
        nt = len(t_segment)
        M = 20
        run = np.arange(0, 2 * M + 1)[:, None]  # Column vector
        
        # Compute function values at shifted Laplace domain points
        s = gamma + 1j * np.pi * run / T
        a = np.array([fhandle(si, *args) for si in s.flatten()]).reshape(s.shape)
        a[0] /= 2  # Adjust first term
        
        # Compute quotient-difference table (de Hoog method)
        e = np.zeros((2 * M + 1, M + 1), dtype=complex)
        q = np.zeros((2 * M, M + 1), dtype=complex)
        q[:, 1] = a[1:2 * M + 1, 0] / a[:2 * M, 0]
        
        for r in range(1,M+1):  
            e[:2 * (M - r) + 1, r] = \
                q[1:2 * (M - r)+2, r] - q[:2 * (M - r) + 1, r] \
              + e[1:2 * (M - r)+2, r - 1]
            if r < M:
                q[:2 *(M - r-1) +2, r + 1] = \
                q[1:2*(M - r-1) +3, r] * e[1:2 * (M - r-1)+3, r] / e[:2 * (M - r-1) +2, r]
        
        # Compute continued fraction coefficients
        d = np.zeros(2 * M + 1, dtype=complex)
        d[0] = a[0, 0]
        d[1::2] = -q[0, 1:M + 1]
        d[2::2] = -e[0, 1:M + 1]
        
        # Compute the recurrence relations for A and B
        A = np.zeros((2 * M + 2, nt), dtype=complex)
        B = np.ones((2 * M + 2, nt), dtype=complex)
        A[1, :] = d[0]
        z = np.exp(1j * np.pi * t_segment / T)
        
        for n in range(2, 2 * M + 2):
            A[n, :] = A[n - 1, :] + d[n - 1] * z * A[n - 2, :]
            B[n, :] = B[n - 1, :] + d[n - 1] * z * B[n - 2, :]
        
        # Apply double acceleration step
        h2M = 0.5 * (1 + (d[2 * M - 1] - d[2 * M]) * z)
        R2Mz = -h2M * (1 - np.sqrt(1 + d[2 * M] * z / (h2M ** 2)))
        A[2 * M + 1, :] += R2Mz * A[2 * M, :]
        B[2 * M + 1, :] += R2Mz * B[2 * M, :]
        
        # Compute inverse Laplace transform
        f_segment = (1 / T * np.exp(gamma * t_segment) * np.real(A[2 * M + 1, :] / B[2 * M + 1, :]))
        f_values.extend(f_segment)
    
    return np.array(f_values).flatten()
