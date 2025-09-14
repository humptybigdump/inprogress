#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
UH: Code taken from Nicoguaro, Nelder-Mead_Rosenbrock.gif, CC BY 4.0, https://commons.wikimedia.org/w/index.php?title=File:Nelder-Mead_Rosenbrock.gif&oldid=260874010, with different initial simplex and 50 instead of 20 steps

Animation of the Nelder-Mead method for the Rosenbrock function.
"""

import numpy as np
import matplotlib as mpl
mpl.use("Agg")
from scipy.optimize import rosen
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rcParams

# In Windows the next line should provide the full path to convert.exe
# since convert is a Windows command
#rcParams['animation.convert_path'] = "C:\Program Files\ImageMagick-6.9.3-Q16\convert.exe"

# UH: for ImageMagick installation with MacPorts on macOS
rcParams['animation.convert_path'] = "/opt/local/bin/convert"
rcParams['font.size'] = 12

def nelder_mead_step(fun, verts, alpha=1, gamma=2, rho=0.5,
                     sigma=0.5):
    """Nelder-Mead iteration according to Wikipedia _[1]
    
    
    References
    ----------
     .. [1] Wikipedia contributors. "Nelder–Mead method." Wikipedia,
         The Free Encyclopedia. Wikipedia, The Free Encyclopedia,
         1 Sep. 2016. Web. 20 Sep. 2016. 
    """
    nverts, _ = verts.shape         
    f = fun(verts.T)
    # 1. Order
    order = np.argsort(f)
    verts = verts[order, :]
    f = f[order]
    # 2. Calculate xo, the centroid"
    xo = verts[:-1, :].mean(axis=0)
    # 3. Reflection
    xr = xo + alpha*(xo - verts[-1, :])
    fr = fun(xr)
    if f[0]<=fr and fr<f[1]:
        new_verts = np.vstack((verts[:-1, :], xr))
    # 4. Expansion
    elif fr<f[0]:
        xe = xo + gamma*(xr - xo)
        fe = fun(xe)
        if fe < fr:
            new_verts = np.vstack((verts[:-1, :], xe))
        else:
            new_verts = np.vstack((verts[:-1, :], xe))
    # 5. Contraction
    else:
        xc = xo + rho*(verts[-1, :] - xo)
        fc = fun(xc)
        if fc < f[-1]:
            new_verts = np.vstack((verts[:-1, :], xc))
    # 6. Shrink
        else:
            new_verts = np.zeros_like(verts)
            new_verts[0, :] = verts[0, :]
            for k in range(1, nverts):
                new_verts[k, :] = sigma*(verts[k,:] - verts[0,:])
 
    return new_verts

# Contour data
npts = 201
x, y = np.mgrid[-2:2:npts*1j, -1:3:npts*1j]
x.shape = (npts**2)
y.shape = (npts**2)
z = rosen(np.vstack((x, y)))
x.shape = (npts, npts)
y.shape = (npts, npts)
z.shape = (npts, npts)

# Simplices data
def data_gen(num):
    #x0 = np.array([1, 0])
    #x1 = np.array([2, 0])
    #x2 = np.array([1, 1])
    # UH: larger initial simplex
    x0 = np.array([0, 0])
    x1 = np.array([2, 0])
    x2 = np.array([0, 2])
    
    verts = np.vstack((x0, x1, x2))
    for k in range(num):
        verts = nelder_mead_step(rosen, verts)
    # Plots
    levels = np.logspace(0.35, 3.2, 5)
    plt.cla()
    plt.contour(x, y, z, levels, colors="k")
    poly = plt.Polygon(verts, facecolor="none", edgecolor="r",
                       linewidth=1.5)
    plt.gca().add_patch(poly)
    plt.xlabel(r"$x_1$", fontsize=14)
    plt.ylabel(r"$x_2$", fontsize=14)
    plt.xticks([-2, -1, 0, 1, 2])
    plt.yticks([-1, 0, 1, 2, 3])
    plt.xlim([-2, 2])
    plt.ylim([-1, 3])

fig = plt.figure(figsize=(5, 5))
ani = animation.FuncAnimation(fig, data_gen, range(50), blit=False)
ani.save("Nelder-Mead_Rosenbrock.gif", writer='imagemagick', fps=2,
         dpi=200)
