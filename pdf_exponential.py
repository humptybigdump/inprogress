"""PDF of exponential distribution: easily displayed using scipy.stats"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

# range of t values
t = np.linspace( 0, 6, 200 )

# loop over array of different tau values
taus = [ 0.5, 1.0, 2.0, 5.0 ]
for tau in taus:
	pdf = expon.pdf( t, scale=tau )

	# plot PDF
	line, = plt.plot( t, pdf, label=r"$\tau$ = %3.1f" % tau  )

	# plot dashed vertical lines at expected value
	plt.vlines( tau, 0, expon.pdf(tau, scale=tau), linestyles='dashed',color=line.get_color() )

plt.xlim(0,6)
plt.ylim(0,1)
plt.xlabel( "$t$")
plt.ylabel( r"$f(t;\tau)$" )
plt.legend()

plt.savefig( "pdf_exponential.pdf" )
plt.show()

