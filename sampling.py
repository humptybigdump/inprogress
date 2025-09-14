import numpy as np, matplotlib.pyplot as plt
from  scipy import interpolate

# illustrate principle of signal sampling and interpolation
# UH after G. Quast's example code

mnx = 0.
mxx = 1.5*np.pi
nbins = 7
xplt = np.linspace(mnx, mxx, nbins+1) # range in x
nplt = nbins * (xplt-mnx)/(mxx-mnx)   # sample number - 1

xana = np.linspace( mnx, mxx, 200 )   # analog values
nana = nbins * (xana-mnx)/(mxx-mnx)
yana = np.sin( xana )

yplt = np.sin(xplt)

miny = min(yplt)
maxy = max(yplt)

# quantization
nbits = 4
step  = ( maxy - miny ) / 2**nbits
quant = step * np.round( yplt/step )

fig,ax = plt.subplots( figsize=(6,5) )
minyp = miny - 0.05*( maxy - miny )
maxyp = maxy + 0.05*( maxy - miny )
ax.set_xlim( 0., nbins+2 )
ax.set_ylim( minyp, maxyp )

# plot sampled curve
ax.plot( nana+1, yana, 'r--', label='Analog Signal')

# plot individual measurements as markers
ax.plot( nplt+1, quant, 'o', color='steelblue', label='Measurements (%d bits)' % nbits ) 

# connect points by straight line
#ax.plot( nplt+1, quant, 'b--', label = 'Linear Interpolation' )  

# cubic spline interpolation
cs_y = interpolate.UnivariateSpline( nplt, quant, s=0 )
xplt2 = np.linspace( -0.5, nbins+0.5, 200 )
ax.plot(xplt2+1, cs_y(xplt2), 'g-.', lw=2, label = 'Spline Interpolation')  

# indicate sampling points as vert. lines
ax.vlines( nplt+1, minyp, yplt, colors='steelblue', linestyles='--' )
    
# axis labels and legend
ax.set_xlabel( r'Sampling, $n = t \,\nu_s$', size='large' )
ax.set_ylabel( 'Value', size='large' )
ax.legend( numpoints=1, loc='best', prop={'size':12} )

plt.savefig( "sampling.pdf" )
plt.show()
