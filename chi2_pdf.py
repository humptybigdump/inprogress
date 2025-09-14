""" display chi2 probability and chi2 probability normalized to number of degrees of freedom"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

fig,ax = plt.subplots( 1, 2, figsize=(10,5) )

S = np.linspace( 0, 25, 250 )
ndof = np.array( [ 2, 4, 6, 8, 10 ] )
for n in ndof:
    ax[0].plot( S, 1.-chi2.cdf( S, n ), label=r'$n_\mathsf{dof}$ = %d' % n  )
    ax[1].plot( S/n, (1.-chi2.cdf( S, n ) ) )

ax[0].set_xlabel( r'$\chi^2$' )
ax[0].set_ylabel( r'$P_{\chi^2}$' )
ax[0].set_ylim( 0., 1.05 )
ax[0].legend()

ax[1].vlines( 1, 0, 1, linestyles="dashed", colors="red" )
ax[1].set_xlabel( r'$\chi^2/n_\mathsf{dof}$' )
ax[1].set_ylabel( r'$P_{\chi^2}$' )
ax[1].set_xlim( 0, 3 )
ax[1].set_ylim( 0., 1.05 )

plt.savefig( 'chi2_pdf.pdf' )
plt.show()
    
