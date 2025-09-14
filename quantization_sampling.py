"""illustration of sampling and quantization of an analog signal"""
import numpy as np
import matplotlib.pyplot as plt

fig, ax =  plt.subplots( 2, 2, figsize=(12,8) )
tmin, tmax = -0.5, 6.5 

# analog signal is a sine wave
t = np.linspace( 0, 2*np.pi, 200 )
wave = np.sin(t)
ax[0][0].hlines( 0, tmin, tmax, linestyle="dashed" )
ax[0][0].plot( t, wave, label="Analog Signal" )
ax[0][0].set_xlabel( "$t$" )
ax[0][0].set_ylabel( "Continuous Signal Value" )
ax[0][0].set_xlim( tmin, tmax )
ax[0][0].legend()

# time discrete signal
n = np.linspace( 0, 6, 12 )
sample = np.sin(n)
ax[0][1].hlines( 0, tmin, tmax, linestyle="dashed" )
ax[0][1].stem( n, sample, label="Time Discrete Signal" )
ax[0][1].set_xlabel( "$n$" )
ax[0][1].set_ylabel( "Continuous Signal Value" )
ax[0][1].set_xlim( tmin, tmax )
ax[0][1].legend()

# analog signal quantized
step=0.2
quant = step*np.round( np.sin(t)/step )
ax[1][0].hlines( 0, tmin, tmax, linestyle="dashed" )
ax[1][0].stairs( quant[:-1], edges=t, label="Quantized Signal" )
ax[1][0].set_xlabel( "$t$" )
ax[1][0].set_ylabel( "Discrete Signal Value" )
ax[1][0].set_xlim( tmin, tmax )
ax[1][0].legend()

# time discrete signal quantized
discrete_quant = step*np.round( sample/step )
ax[1][1].hlines( 0, tmin, tmax, linestyle="dashed" )
ax[1][1].stem( n, discrete_quant, label="Time Discrete Quantized Signal" )
ax[1][1].set_xlabel( "$n$" )
ax[1][1].set_ylabel( "Discrete Signal Value" )
ax[1][1].set_xlim( tmin, tmax )
ax[1][1].legend()

plt.savefig("quantization_sampling.pdf")
plt.show()