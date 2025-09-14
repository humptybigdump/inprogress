"""Plot PDF of chi-square distribution for different numbers of degrees of freedom"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

S  = np.linspace( 0, 20, 200 )

# plot PDF for an array of four values for n (number of degrees for freedom)
ns = [ 1, 2, 5, 10 ]
for n in ns:
	pdf = chi2.pdf( S, df=n )
	plt.plot( S, pdf, label=r"$n$ = %3.1f" % n  )

plt.xlim(0,20)
plt.ylim(0,1)
plt.xlabel( "$S$")
plt.ylabel( r"$\chi^2(S)$" )
plt.legend()

plt.savefig( "pdf_chi2_distribution.pdf" )
plt.show()

