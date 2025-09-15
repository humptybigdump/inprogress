from typing import Tuple, Callable, Union

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import rv_continuous
from scipy import stats
from scipy.integrate import quad
from statsmodels.distributions.empirical_distribution import ECDF

# random_gen: np.random.Generator = np.random.default_rng(42)
N_POINTS_TO_DRAW = 1000


def sample_sum_of_rv_type(n_samples: int, n_per_sample: int, rv: rv_continuous) -> np.ndarray:
    """ Compute a sample of means of random variables of the specified type.

    Parameters
    ----------
    n_samples: Number of means to sample
    n_per_sample: Number of terms in one mean
    rv: Scipy random variable to sample from

    Returns
    -------
        Array with sampled sums
    """
    rvs = rv.rvs(size=(n_samples, n_per_sample))
    return np.sum(rvs, axis=1)


def compute_rho(rv: stats.rv_continuous) -> float:
    """ Numerically compute rho = E |rv - mu(rv)|^3 / sigma(rv)^3"""
    mu, var, skew = rv.stats(moments='mvs')
    is_nan_or_inf = lambda x: np.isnan(x) + np.isinf(x)
    if np.any([is_nan_or_inf(m) for m in [mu, var, skew]]):
        return None
    func = lambda x: np.abs(x - mu) ** 3 / var ** (3 / 2) * rv.pdf(x)
    return quad(func, a=-np.inf, b=np.inf)[0]


def empirical_dist_zn(n_samples: int, n_per_sample: int, rv: rv_continuous) -> Tuple[Callable, float]:
    """Compute empirical distribution of Z_n of sum of random variables of the specified type.

    Parameters
    ----------
    n_samples: Number of means to sample
    n_per_sample: Number of terms in one mean
    rv: Scipy random variable to sample from

    Returns
    -------
        Array with sampled sums
        rho
    """
    mu = rv.stats()[0]
    sd = np.sqrt(rv.stats()[1])
    zns = (sample_sum_of_rv_type(n_samples, n_per_sample, rv) - n_per_sample * mu) / (np.sqrt(n_per_sample) * sd)
    ecdf = ECDF(zns)
    rho = compute_rho(rv)
    return ecdf, rho


def plot_zn_g(emp_dist_zn: Callable, rho: float, n_per_sum: int, ax: plt.Axes = None):
    """ Draw figure for Berry Essen central limit theorem

    Parameters
    ----------
    ax: Axes in which to draw
    emp_dist_zn: Empirical distribution function of Z_n
    rho: rho from Berry Essen theorem
    n_per_sum: Number of terms in sum

    Returns
    -------
        Axes with figure
    """
    if ax is None:
        fig, ax = plt.subplots()
    x = np.linspace(-stats.norm.stats()[1] * 3, stats.norm.stats()[1] * 3, N_POINTS_TO_DRAW)
    ax.plot(x, emp_dist_zn(x), label=r'$Z_n$')
    ax.plot(x, stats.norm.cdf(x), label=r'$g$')
    ax.legend()
    return ax


def plot_diff_zn_g(emp_dist_zn: Callable, rho: Union[float, None] = None,
                   n_per_sum: Union[int, None] = None, ax: plt.Axes = None):
    """ Draw deviation between emp. dist. of zn and g

    Parameters
    ----------
    ax: Axes in which to draw
    emp_dist_zn: Empirical distribution function of Z_n
    rho: rho from Berry Essen theorem
    n_per_sum: Number of terms in sum

    Returns
    -------

    """
    if ax is None:
        fig, ax = plt.subplots()
    x = np.linspace(-stats.norm.stats()[1] * 3, stats.norm.stats()[1] * 3, N_POINTS_TO_DRAW)
    ax.set_title(r'$Z_n - g$')
    ax.plot(x, emp_dist_zn(x) - stats.norm.cdf(x), label=r'$Z_n - g$')
    if rho is not None:
        ax.axhline(xmin=-stats.norm.stats()[1] * 3,xmax=stats.norm.stats()[1] * 3, y=rho / np.sqrt(n_per_sum), c='g',
                   label=r'$\rho / \sqrt{N}$')
        ax.axhline(xmin=-stats.norm.stats()[1] * 3,xmax=stats.norm.stats()[1] * 3, y=-rho / np.sqrt(n_per_sum), c='g',
                   label=r'$- \rho / \sqrt{N}$')
    # ax.legend()
    return ax