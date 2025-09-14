"""Illustration of hypothesis testing"""
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import norm

def double_gaussian_model( x, mu=0., sigma1=1., sigma2=2. ):
	'''Normal distributions with different sigmas left and right of mu:'''
	fac=2./(sigma1+sigma2)
	return np.where( x < mu, fac*sigma1*norm.pdf( x, loc=mu, scale=sigma1), fac*sigma2*norm.pdf( x, loc=mu, scale=sigma2) )

# range of values
tmin, tmax, t0, t1 = 0, 10, 7, 5.2
t = np.linspace( tmin, tmax, 200 )

# PDFs of hypotheses H0 and H1
g0 = double_gaussian_model( t, 3, 1, 2 )
g1 = double_gaussian_model( t, 8.5, 1.5, 1)

fig,ax = plt.subplots(figsize=(5,5))

# plot null hypothesis
ax.plot( t, g0, label="$H_0$" )
ax.set_xlabel( "Test Statistic $t$" )
ax.set_ylabel( "$g(t|H_i)$")
ax.set_ylim( 0, 0.4 )
ax.legend()
plt.savefig( "testing_null_hypothesis.pdf" )

# plot significance level
ax.vlines( t0, 0, 0.3, colors="green" )
ax.text( t0, -0.02, "$t_0$", color="green", ha="center" )
ax.fill_between( t[t>t0], 0, g0[t>t0], facecolor="green", alpha=0.3 )
ax.annotate( r"$\alpha$", xy=(t0+0.25,0.02), xytext=(t0+1,0.07), arrowprops=dict(facecolor="black", width=1, headwidth=5) )
plt.savefig( "testing_significance_level.pdf" )

# plot measurement
line1 = ax.vlines( t1, 0, 0.2, colors="red" )
text1 = ax.text( t1, -0.02, "$t_1$", color="red", ha="center" )
plt.savefig( "testing_measurement.pdf" )

# remove measurement and plot alternative hypothesis
line1.remove()
text1.remove()
ax.plot( t, g1, label="$H_1$" )
ax.legend()
plt.savefig( "testing_alternative.pdf" )

# plot test power beta
ax.fill_between( t[t<t0], 0, g1[t<t0], facecolor="red", alpha=0.3 )
ax.annotate( r"$\beta$", xy=(t0-1.5,0.02), xytext=(t0-2.5,0.07), arrowprops=dict(facecolor="black", width=1, headwidth=5) )
plt.savefig( "testing_test_power.pdf" )

plt.show()