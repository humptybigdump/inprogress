this_program= "Helium-20200524-1400.py"
print( "This is <",this_program,">!")
# =========================================================
#	T.Arndt
#	KIT
#	ITEP
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INPUT: 	none
# OUTPUT:	none
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# =========================================================
#libs####################################################################
import math                                     						#fuer e-Funktion, PI,...
import numpy as np                              						#needed for array-operations
import matplotlib.pyplot as plt                 						#plotting library: muss üblicherweise zum Python-System einmalig hinzugefügt werden, z.B. mit "PIP install matplotlib" o.ä.
opsys= "WINDOWS"														#zur späteren Selektion von Spezifika wird das Betriebssystem angegeben
#opsys= "OTHER"															#
if opsys == "WINDOWS": import msvcrt as ms								#works for ms-windows only (get better access to terminal, especially keypress); if no equivalent "keypress" has to be substituted (see below)
#functions###############################################################
def create_simple_plot():														#Schnelles Anschauen der Messdaten
	print( "create_simple_plot...")										#
	x_pvals=	np.arange( 0., no_flashes, 1.)							#initialisiere plot-Variablen
	y1_pvals=	np.arange( 0., no_flashes, 1.)							#
	for i in range( 0, no_flashes):										#scanne alle Wertepaare
		x_pvals[i]=  Xdata[i]/1000.										#setze x-Achsen-Werte
		y1_pvals[i]= Ydata[i] 											#setze y-Achsen-Werte
	fig= plt.subplot()													#definiere fig als subplot
	plt.xlabel( 'P [kPa]')												#setze x-Achsen-Label
	plt.ylabel( 'T [K]')												#setze y-Achsen-Label
	plt.title( "Dampfdruckkurve von 4He")								#setze Titel
	#plt.legend( loc='upper left')										#positioniere Legende
	fig.scatter( x_pvals, y1_pvals)
	fig.plot( x_pvals, y1_pvals)
	fig.set_ylim( 0., 5.)
	fig.grid( axis='both')
	plt.show()
	key=input()
	print( "...OK")														#report
	return()
def T4He( p):
	A_sf=	[ 	1.392408,	0.527153,	0.166756,	0.050988,	0.026514,	0.001975,	-0.017976,	0.005409,	0.013259]
	B_sf= 	5.6
	C_sf=	2.9
	A_nf=	[	3.146631,	1.357655,	0.413823,	0.091159,	0.016349,	0.001826,	-0.004325,	-0.004973,	0.]
	B_nf= 	10.3
	C_nf=	1.9
	result_sf= A_sf[ 0]
	result_nf= A_nf[ 0]
	for i in range( 1, 9):
		result_sf+=A_sf[ i] * math.pow( ( (math.log( p) - B_sf) /C_sf), i)
		result_nf+=A_nf[ i] * math.pow( ( (math.log( p) - B_nf) /C_nf), i)
	if result_nf >= 2.1768:
		result= result_nf
	else:
		result= result_sf
	return(result)
#main routine###########################################################
# vars...
no_flashes= 1000
Xdata= np.arange( 0., no_flashes*1., 1.)										#X-Werte für Berechnungen
Ydata= np.arange( 0., no_flashes*1., 1.)										#Y-Werte für Berechnungen
for i in range( 0, no_flashes):
	Xdata[i]=	(0.500+i/no_flashes*200.)*1000.
	Ydata[i]=	T4He( Xdata[i])
	print( Xdata[i],";", Ydata[i])
create_simple_plot()
print( "All done!")
key= input()
########################################################################
#EOF
