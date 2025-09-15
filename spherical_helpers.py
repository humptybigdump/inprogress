import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def sample_spherical(n: int, ndim: int) -> np.ndarray:
    pts = stats.norm.rvs(size=(ndim, n))
    pts = pts / np.linalg.norm(pts, axis=0) * np.sqrt(ndim)
    return pts.T


def plot_kde_margin_spherical(n: int, ndim: int, ax: plt.Axes) -> plt.Axes:
    rvs = sample_spherical(n=n, ndim=ndim)
    x = rvs[:, 0]
    kde = stats.gaussian_kde(x)
    x_grid = np.linspace(-np.sqrt(ndim)*1.2, np.sqrt(ndim)*1.2, 500)
    y_grid = kde.evaluate(x_grid)

    ax.plot(x_grid, y_grid, label=f'dim={ndim}')
    ax.set_title(f"KDE des 1. Rands in {ndim} Dimensionen")
    ax.set_xlabel("x1")
    ax.set_ylabel("Dichte")
    ax.grid(True)

    return ax
