"""
2-D generation of random conductivity field  
nx (2x1):     number of cells in x- and y-directions
dx (2x1):     associated grid spacing
lx (2x1):     correlation length
ang (scalar): rotation angle
sigY(scalar): variance of log-field
Ctype:        1: exponential, all others: Gaussian
Kg(scalar):   geometric mean of the field
"""

import numpy as np

def randomK(nx, dx, lx, ang, sigY, Ctype, Kg):
    # ============== BEGIN AUTO-COVARIANCE BLOCK ======================================
    nx_ex = np.array(nx) + np.round(5 * np.array(lx) / np.array(dx)).astype(int)
    ntot = np.prod(nx_ex)  # total number of nodes

    # Define the physical grid
    x = np.linspace(-nx_ex[0] / 2 * dx[0], (nx_ex[0] - 1) / 2 * dx[0], nx_ex[0])
    y = np.linspace(-nx_ex[1] / 2 * dx[1], (nx_ex[1] - 1) / 2 * dx[1], nx_ex[1])
    X, Y = np.meshgrid(x, y)

    # Rotation into Longitudinal/Transverse Coordinates
    X2 = np.cos(ang) * X + np.sin(ang) * Y
    Y2 = -np.sin(ang) * X + np.cos(ang) * Y
    
    # scaled distance
    H = np.sqrt((X2 / lx[0])**2 + (Y2 / lx[1])**2)
    print("Calculate Auto-Covariance")
    
    # Covariance Matrix of Log-Conductivities
    if Ctype == 1:
        RYY = sigY * np.exp(-np.abs(H))
    else:
        RYY = sigY * np.exp(-H**2)
    # ============== END AUTO-COVARIANCE BLOCK ========================================

    # ============== BEGIN POWER-SPECTRUM BLOCK =======================================
    # Fourier Transform (Origin Shifted to Node (1,1))
    SYY = np.fft.fftn(np.fft.fftshift(RYY)) / ntot
    # Remove Imaginary Artifacts
    SYY = np.abs(SYY)
    SYY[0, 0] = 0
    # ============== END POWER-SPECTRUM BLOCK =========================================

    # ============== BEGIN FIELD GENERATION BLOCK =====================================
    ran = np.sqrt(SYY) * (1j * np.random.randn(*SYY.shape) + np.random.randn(*SYY.shape))
    K = Kg * np.exp(np.real(np.fft.ifftn(ran * ntot)))
    
    return K[:nx[1], :nx[0]]
