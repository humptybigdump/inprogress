from typing import Union

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
from scipy.integrate import quad


def sample_norm(rv: stats.rv_continuous, p: int, n: int=100000):
    """ Compute l_p norm of random variable rv based on n samples."""
    p = check_p(p)
    rvs = rv.rvs(n)
    return ( np.mean(np.abs(rvs) ** p) ) ** (1 / p) # (a ** b) means 'a to the power of b'


def compute_norm_numerically(rv: stats.rv_continuous, p: int):
    """Compute the l_p norm of random variable rv based on numerical integration"""
    p = check_p(p)

    def integrand(x: np.ndarray):
        return np.abs(x) ** p * rv.pdf(x)

    support = rv.interval(1)
    integral = quad(integrand, support[0], support[1])[0]
    norm = integral ** (1 / p)
    return norm


def compute_standard_normal_norm(p: Union[int, np.ndarray]) -> np.ndarray:
    """Compute the l_p norm of a standard normal random variable."""
    p = check_p(p)

    def compute_single_norm(p_single: int):
        if p_single % 2 == 0:  # p even
            factor = 1
        else:  # p uneven
            factor = np.sqrt(2 / np.pi)
        exponent = (1 / p_single.astype(np.float64))
        norm = np.prod( np.array(range(p_single - 1, 0, -2)) ** exponent ) * factor ** exponent
        return norm

    if p.size > 1:
        norms = np.array([compute_single_norm(ip) for ip in p])
    else:
        norms = compute_single_norm(p)
    return norms


def compute_uniform_norm(p: Union[int, np.ndarray]):
    """Compute the l_p norm of a (0, 1)-uniform random variable."""
    p = check_p(p)
    return (1 / (p + 1)) ** (1 / p)


# Plotting functions
def histogram_of_norm_samples(rv: stats.rv_continuous, p: int, m: int, ax: plt.Axes):
    """"Plot histogram of m estimates for l_p norm of rv in ax"""
    p = check_p(p)
    estimates = [sample_norm(rv, p) for i in range(0, m)]
    ax.hist(estimates, density=True)
    return ax


# Helper functions
def check_p(p: int):
    """Check if p is valid for l_p norm"""
    p = np.array(p)
    if np.any(p < 1):
        raise ValueError('All elements have to be >= 1')
    p = p.astype(np.int32)
    return p
