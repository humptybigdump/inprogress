#MyCryogenics-WiP.py
#
#T.Arndt
#
#20250302-1000
########################################################################

import matplotlib.pyplot as plt											# using plot-function
import numpy as np														# using arange
from CoolProp.CoolProp import PropsSI									# using PropsSI (coolprop-install: python -m pip install -U coolprop)

#References...
#http://www.coolprop.org/coolprop/HighLevelAPI.html#vapor-liquid-and-saturation-states

#Neon...................................................................
print( "Neon.............................")
# 1 atm...
print( "for p= 1 atm...")
H_V = PropsSI('H','P',101325,'Q',1,'Neon'); print(H_V)					# Saturated vapor enthalpy at 1 atm in J/kg
H_L = PropsSI('H','P',101325,'Q',0,'Neon'); print(H_L)					# Saturated liquid enthalpy at 1 atm in J/kg
rho= PropsSI('D','P',101325,'Q',0,'Neon'); print(rho)					# density
print( "Latent heat of vaporization (J/kg)  :", H_V - H_L)				# report vaporization latent heat [J/kg]
print( "Latent heat of vaporization (kJ/g)  :", (H_V - H_L)/1E6)		# report vaporization latent heat [kJ/g]
print( "Latent heat of vaporization (kWh/kg):", (H_V - H_L)/1E3/60/60)	# report vaporization latent heat [kWh/kg]
print( "density (kg/m³)                     :", rho)					# report density
temperatures = np.arange( 24.46, 44.4, 0.5)								# 24.46 K bis 44.4 K
es = [PropsSI('H', 'T', T, 'Q', 0, 'Neon') for T in temperatures]
plt.plot( temperatures, es); plt.title('H-T Diagram Ne'); plt.xlabel('temperature (K)'); plt.ylabel('H (J/kg)')
plt.grid(True)
plt.show()

#Hydrogen...............................................................
print( "Hydrogen.........................")
H_V = PropsSI('H','P',101325,'Q',1,'Hydrogen'); print(H_V)				# Saturated vapor enthalpy at 1 atm in J/kg
H_L = PropsSI('H','P',101325,'Q',0,'Hydrogen'); print(H_L)				# Saturated liquid enthalpy at 1 atm in J/kg
print( "Latent heat of vaporization (J/kg):", H_V - H_L)				# report vaporization latent heat [J/kg]
print( "Latent heat of vaporization (kJ/g):", (H_V - H_L)/1E6)			# report vaporization latent heat [kJ/g]
print( "Latent heat of vaporization (kWh/kg):", (H_V - H_L)/1E3/60/60)	# report vaporization latent heat [kWh/kg]
#Definiere ein Temperaturintervall von 13.857 K bis 33.145 K
temperatures = np.arange( 13.857, 33.145, 0.5)
pressures = [PropsSI(	'P', 'T', T, 'Q', 0, 'Hydrogen')/1E5 for T in temperatures]  
#						output pressure
#							 input quantity: temperature
#								  value
#									 input quantity: saturation (1: vapor; 0: liquid)
#										  value
#											  fluid
# documentation: http://www.coolprop.org/coolprop/HighLevelAPI.html
plt.plot(temperatures, pressures); plt.title('P-T Diagram H2'); plt.xlabel('temperature (K)'); plt.ylabel('pressure (bar)')
plt.grid(True)
plt.show()


#Helium.................................................................
print( "Helium...........................")
H_V = PropsSI('H','P',101325,'Q',1,'Helium'); print(H_V)				# Saturated vapor enthalpy at 1 atm in J/kg
H_L = PropsSI('H','P',101325,'Q',0,'Helium'); print(H_L)				# Saturated liquid enthalpy at 1 atm in J/kg
print( "Latent heat of vaporization (J/kg):", H_V - H_L)				# report vaporization latent heat [J/kg]
print( "Latent heat of vaporization (kJ/g):", (H_V - H_L)/1E6)			# report vaporization latent heat [kJ/g]
print( "Latent heat of vaporization (kWh/kg):", (H_V - H_L)/1E3/60/60)	# report vaporization latent heat [kWh/kg]
temperatures = np.arange( 2.0768, 5.1953, 0.5)							# 24.46 K bis 44.4 K
pressures = [PropsSI('P', 'T', T, 'Q', 0, 'Helium')/1E5 for T in temperatures]  # create P-T-array
plt.plot(temperatures, pressures); plt.title('P-T Diagram He'); plt.xlabel('temperature (K)'); plt.ylabel('pressure (bar)')
plt.grid(True)
plt.show()

T_H2= PropsSI( 'T', 'P', 6*1E5, 'Q', 0, 'Hydrogen')
print( "T(H2,P,liquid)=", T_H2)
P_Ne= PropsSI( 'P', 'T', T_H2, 'Q', 0, 'Neon')/1E5
print( "P(Ne,T,liquid)=", P_Ne)
