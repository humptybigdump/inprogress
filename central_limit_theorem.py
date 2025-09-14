"""demonstration of central limit theorem with random numbers"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# initialize random number generator with a seed
rng = np.random.default_rng( 42 )

# prepare plot
fig, ax = plt.subplots()

# generate n=1000 exponential distributions of N=10000 entries each
# each distribution gets a different random tau from uniform distribution
N = 10000
n = 1000
tau = rng.uniform( 0, 10, size=n )
tau = np.repeat(tau,N).reshape(n,N)
expo = rng.exponential( scale=tau )

# exponential distribution: expected value and standard deviation = tau
mu  = tau
std = tau

# NumPy style summation
normalization = 1. / (np.sqrt(N)*std) 
sume = np.sum( ( expo - mu ) * normalization, axis=1 )

# remark 1: instead of the NumPy one-line, an enumeration would work, too
# for i, u in enumerate( uniform ):
#	sume[i] = np.sum( ( expo - mu ) * normalization )
	
# remark 2: this can als be achieve in one line using list comprehension
# sume = [ np.sum( ( e - mu ) * normalization ) for e in expo ]

# remark: an explicit iterator for numpy arrays would also be possible
# for e, it in zip( expo, np.nditer( sume, op_flags=['writeonly']) ):
#	it[...] = np.sum( ( e - mu ) * normalization )

# histogram of sums
bins = np.linspace( -5, 5, 51 ) # bin width: 0.2
ax.hist( sume, bins )
ax.set_xlabel( "$x$")
ax.set_ylabel( "Frequency" )

# normal distribution for comparison
x = np.linspace( -5, 5, 200 )
pdfnorm = n*0.2 # proper normalization: entries * bin width
ax.plot( x, pdfnorm*norm.pdf(x) )

plt.savefig( "central_limit_theorem.pdf" )
plt.show()