this_program= "UI-Auswertung.py-20140424-1000"
print( "This is <",this_program,">!")
# =========================================================
#	Karlsruher Institut fuer Technologie - Institut fuer Technische Physik (ITEP)
#
#	T.Arndt
#
# 	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 	INPUT: 	HTS_Bi2223.dat
# 	OUTPUT:	none
# 	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
def view_log_plot():													#Zeige log-log-plot des Bereichs der n-Wert-Bestimmung
	print( "view_log_plot()...")										#report
	x_pvals=	np.arange( 0., no_xy, 1.)								#initialisiere plot-Felder
	y1_pvals=	np.arange( 0., no_xy, 1.)								#
	y2_pvals=	np.arange( 0., no_xy, 1.)								#
	for i in range( 0, no_xy):											#scanne alle Wertepaare
		x_pvals[i]=  Xdata[ i]											#setze plot-Felder
		y1_pvals[i]= Ydata[ i]											#
		y2_pvals[i]= y_ordinate_n_dev[ 0] + y_slope_n_dev[ 0]*Xdata[ i]	#
	plt.xlabel( 'log(I [A])')											#log-Strom auf x-Achse
	plt.ylabel( 'log(E [µV/cm])')										#log-E-Feld auf y-Achse
	plt.title( "log-log-plot")											#setze Titel
	plt.plot( x_pvals, y1_pvals, label='data')							#zeichne Datenpunkte
	plt.plot( x_pvals, y2_pvals, label='fit for n')						#zeichne fit-Gerade
	plt.legend( loc='upper left')										#positioniere Legende
	plt.show()															#Erstelle Grafik
	print( "...OK")														#report
	return()
def Linear_Regression( X_lr, Y_lr, y_ordinate_n_dev, y_slope_n_dev, i_lo, i_hi): #Lineare Regression (allgemeines Modul)
	print( "Linear_Regression...")										#report
	no_flashes= i_hi-i_lo+1												#berechne Anzahl zu berücksichtigender Datenpaare
	if no_flashes < 3 :													#LinReg macht keinen Sinn für weniger als 3 Datenpaare!
		print( "I doubt you want to do a linear regression on less than 3 data-pairs!")
		printf( "<ENTER> to leave");
		input()
		return( -1);

	print( "*****Computing sums...")									#report
	Sx= Sy= Sxx= Syy= Sxy= 0.0											#Initialisiere Summen
	for i in range( i_lo, i_hi+1) :										#scanne alle relevanten Datenpaare
		Sxx+= X_lr[i]*X_lr[i]											#Bilde Summen...
		Syy+= Y_lr[i]*Y_lr[i]											#
		Sx+=  X_lr[i]													#
		Sy+=  Y_lr[i]													#
		Sxy+= X_lr[i]*Y_lr[i]											#

	print( "*****Computing line parms...");								#report
	slope= 		( no_flashes*Sxy - Sx*Sy ) / ( no_flashes*Sxx - Sx*Sx )	#Berechne Steigung
	ordinate=   ( Sxx*Sy         - Sx*Sxy) / ( no_flashes*Sxx - Sx*Sx )	#Berechne Ordinatenabschnitt
	correlation= Sxy / math.sqrt(Sxx*Syy)								#Berechne Korrelationswert

	print( "*****Computing deviations...")								#report
	deviation= 0.														#Initialisier Abweichung
	for i in range( i_lo, i_hi+1):										#scanne alle relevanten Datenpaare
		deviation+= ( Y_lr[i] - slope*X_lr[i] - ordinate ) * ( Y_lr[i] - slope*X_lr[i] - ordinate )	#addiere Fehlerquadrate
	deviation=     math.sqrt( deviation / (no_flashes - 2.0) )			#ziehe Wurzel
	slope_dev=     deviation*math.sqrt( no_flashes / ( no_flashes*Sxx - Sx*Sx ))	#berechne Abweichung der Steigung
	ordinate_dev=  deviation*math.sqrt( Sxx        / ( no_flashes*Sxx - Sx*Sx ))	#berechne Abweichung der Ordinate

	print( "*****Computing mean values...");							#report
	x_mean= Sx/no_flashes												#berechne Mittelwert x
	y_mean= Sy/no_flashes												#berechne Mittelwert y

	#Put values into parms...											#Werte in Übergabeparameter, da sonst keine Rückgabe erfolgt
	y_ordinate_n_dev[ 0]= 	ordinate									#
	y_ordinate_n_dev[ 1]= 	ordinate_dev								#
	y_slope_n_dev[ 0]=      slope										#
	y_slope_n_dev[ 1]=   	slope_dev									#
	#correlation: see above
	print( "report results...")											#report
	print( "n       : ", no_flashes)
	print( "<X>     : ", x_mean)
	print( "<Y>     : ", y_mean)
	print( "correl. : ", correlation)
	print( "Ordinate: ", y_ordinate_n_dev[ 0])
	print( "dev     : ", y_ordinate_n_dev[ 1])
	print( "Slope:    ", y_slope_n_dev[ 0])
	print( "dev     : ", y_slope_n_dev[ 1])
	print("LINEAR REGRESSION OK<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	return( correlation)												#retourniere den Korrelationswert
def compute_n():														#berechne den n-Wert
	global Ecn_lo, Ecn_hi, tap_distance, Ic_result, n_result, no_xy, y_ordinate_n_dev, y_slope_n_dev	#globale Variablen
	print( "compute_n()...")											#report
	Ucn_lo= Ecn_lo*1E-6*tap_distance									#berechne untere Spannungsschranke des Berechnungsintervals
	Ucn_hi= Ecn_hi*1E-6*tap_distance									#...obere...
	print( "Ucn_lo [V]=", Ucn_lo)										#report
	print( "Ucn_hi [V]=", Ucn_hi)										#
	y_r= 0.																#initialisiere den Korrelationskoeffizienten

	#search for i_n_hi.............
	i_n_hi= no_flashes;													#setze den index der oberen Schranke des Berechnungsintervals auf das letze Wertepaar
	while i_n_hi >= 0:													#schleife zum Indexvermindern
		print( "i_n_hi:", i_n_hi)										#report
		if ( Udata[ i_n_hi] <= Ucn_hi and Idata[ i_n_hi] >= 0.9 * Ic_result ) : break	#wenn obere Spannungsschranke unterschritten, dann entsprechenden index bestimmt
		i_n_hi-= 1														#ansonsten nächstkleineren index
	print( "i_n_hi=", i_n_hi)											#report

	#search for i_n_lo...
	i_n_lo= i_n_hi														#nun ähnlich für den unteren index...
	while i_n_lo >= 0 :													#
		print( "i_n_lo:", i_n_lo)										#
		if Udata[ i_n_lo] <= Ucn_lo : break								#
		i_n_lo-= 1														#
	print( "i_n_lo=", i_n_lo);											#report

	print( "convert to log-log...")										#report
	i_xy= 0																#initialisiere die Anzahl der relevanten Wertepaare
	for i in range( i_n_lo, i_n_hi+1):									#scanne das Berechnungsintervall
		if Udata[ i] >0 :												#Spannungen <=0 verträgt der Log10 nicht!
			Xdata[ i_xy]= math.log10( Idata[ i])						#setze X für Fit
			Ydata[ i_xy]= math.log10( Udata[ i])						#setze Y für Fit
			i_xy += 1													#erhöhe Anzahl der relevanten wertepaare
	print( "...OK")														#report
	no_xy= i_xy -1														#einer war zu viel

	print( "Linear regression...");										#report
	y_r= Linear_Regression( Xdata, Ydata, y_ordinate_n_dev, y_slope_n_dev, 0, no_xy)	#führe die LinReg aus
	print( "OK. RC=", y_r);												#report, auch den Korrelationskoeffizienten

	print( "LINE description...")										#report
	print( "index        : %i -> %i\n", i_n_lo, i_n_hi)
	print( "Line         : Y=", y_slope_n_dev[ 0], "*X+", y_ordinate_n_dev[1])
	print( "Correlation  : ", y_r)
	print( "Dev.of slope : ", y_slope_n_dev[1])
	print( "Dev.of ord.  : ", y_ordinate_n_dev[1])
	print( " ")
	print( "<ENTER> to continue")
	n_result= 	y_slope_n_dev[ 0]										#setze n
	n_dev=		y_slope_n_dev[ 1]										#setze Abweichung
	print( "=====================================================")
	print( "=> n= ", n_result, " +/- ", n_dev)
	print( "=====================================================")
	print( "...OK")
	input()																#Warte auf Benutzer
	return()
def view_EI_fast():														#Schnelles Anschauen der Messdaten
	print( "view_EI_fast()...")											#report
	print( "create_simple_2D_plot...")									#
	x_pvals=	np.arange( 0., no_flashes, 1.)							#initialisiere plot-Variablen
	y1_pvals=	np.arange( 0., no_flashes, 1.)							#
	for i in range( 0, no_flashes):										#scanne alle Wertepaare
		x_pvals[i]=  Idata[i]											#setze x-Achsen-Werte
		y1_pvals[i]= Udata[i] * 1E6 / tap_distance						#setze y-Achsen-Werte
	plt.xlabel( 'I [A]')												#setze x-Achsen-Label
	plt.ylabel( 'E [µV/cm]')											#setze y-Achsen-Label
	plt.title( "E-I-data")												#setze Titel
	plt.plot( x_pvals, y1_pvals, label='E [µV/cm]')						#zeichne
	plt.legend( loc='upper left')										#positioniere Legende
	plt.show()															#zeige Grafik
	print( "...OK")														#report
	return()
def search_for_Ics():													#Schnelles Suchen nach Ic per linearer Interpolation zwischen Messpunkten
	global Idata, Udata, Bdata, E_criterion, tap_distance, no_flashes, Ic_result, B_result, T_result	#globale Variablen
	print( "search_for_Ics()...")										#report
	Uc= E_criterion * 1E-6 * tap_distance								#konvertiere Kriterium Elektrisches Feld in Spannung
	print( "critical voltage Uc [V]:", Uc)								#report
	Ic_result= 0;                                                       #Initialisiere Ergebnis
	for i in range(0, no_flashes):										#scanne alle Wertepaare
		print( "U(", i, ")=", Udata[i]," V")							#report
		print( "I(", i, ")=", Idata[i]," A")							#
		if ( Udata[ i] < Uc) and ( Udata[ i+1] >= Uc) :					#wenn Spannung kleiner Kriterium und nächste Spannung oberhalb, dann interpoliere Werte linear...
			I= Idata[ i] + (Idata[ i+1] - Idata[ i]) / (Udata[ i+1] - Udata[ i]) * (Uc - Udata[ i])
			B= Bdata[ i] + (Bdata[ i+1] - Bdata[ i]) / (Udata[ i+1] - Udata[ i]) * (Uc - Udata[ i])
			T= Tdata[ i] + (Tdata[ i+1] - Tdata[ i]) / (Udata[ i+1] - Udata[ i]) * (Uc - Udata[ i])
			print( i,": Ic(", Uc, " V, ", B, " T, ", T, " K)=", I, " A")#report
			if ( I >= Ic_result and i < no_flashes) :                   #wenn das der größte Stromwert bisher ist, dann nimm diese Werte als Ergebnisse...
				Ic_result= I;
				B_result= B;
				T_result= T;
		if ( ( Udata[ i] >= Uc) and ( Udata[ i+1] <  Uc) ) :			#wenn Spannung größer Kriterium und nächste Spannung kleiner, dann interpoliere Werte linear...
			I= Idata[ i] - ( Idata[ i+1] - Idata[ i]) / ( Udata[ i+1] - Udata[ i]) * ( Uc - Udata[ i])
			B= Bdata[ i] - ( Bdata[ i+1] - Bdata[ i]) / ( Udata[ i+1] - Udata[ i]) * ( Uc - Udata[ i])
			T= Tdata[ i] - ( Tdata[ i+1] - Tdata[ i]) / ( Udata[ i+1] - Udata[ i]) * ( Uc - Udata[ i])
			print( i,": Ic(", E_criterion*1E-6*tap_distance, " V, ", B, " T, ", T, " K)=", I, " A")
			if ( I >= Ic_result and i < no_flashes) :					#wenn das der größte Stromwert bisher ist, dann nimm diese Werte als Ergebnisse...
				Ic_result= I
				B_result= B
				T_result= T
	print( "...OK")														#report
	return()
def read_dat_file():													#Einlesen der Messdaten aus Datei
	global no_flashes, no_rems											#globale Variablen
	print( "read_dat_file()...")										#report
	fp_dat= open( filename_dat, "r")									#öffne Datenfile
	no_flashes= 0														#initialisiere Anzahl Wertepaare
	for row in fp_dat:													#scanne alle Zeilen der Datei
		if row[0]== '#':												#Wenn die Zeile mit '#' beginnt, dann ist es ein Kommentar
			print( "Remark:", row)										#report
		else:															#andernfalls lese Werte ein...
			Idata[ no_flashes]= eval( row[ 0: row.find( ',')]);	print( "I [A]: ", Idata[ no_flashes]); row= row[ row.find( ',') + 1: ]
			Udata[ no_flashes]= eval( row[ 0: row.find( ',')]); print( "U [V]: ", Udata[ no_flashes]); row= row[ row.find( ',') + 1: ]
			Bdata[ no_flashes]= eval( row[ 0: row.find( ',')]); print( "B [T]: ", Bdata[ no_flashes]); row= row[ row.find( ',') + 1: ]
			Tdata[ no_flashes]= eval( row[ 0: row.find( ',')]); print( "T [K]: ", Tdata[ no_flashes]); row= row[ row.find( ',') + 1: ]
			no_flashes+= 1												#erhöhe Wertepaarzahl
		print( row)														#report
	fp_dat.close()														#schliesse Datei
	print( "...OK")														#report
	return( 0)
def init_vars():														#Initialisiere die Variablen
	no_rems= 0															#initialisiere Anzahl der Bemerkungen
	no_flashes= 0														#Initialisiere Anzahl der wertepaare
	sample_ID= "sample"													#Initialisiere Probenbezeichnung
	E_criterion= 1.														#Kriterium für das elektrische Feld [µV/cm]
	tap_distance= 2.													#Abstand der Spannungsabgriffe [cm]
	return()
def my_keypress():														#OS-specifisches Funktion, um einen Tastendruck abzuholen (falls nicht kompatibel: durch "key=input()" ersetzen; dann braucht man halt ein zusätzliches "ENTER")
	key= ms.getch()														#get from ms the sequence of the keypress
	key= key.decode( 'utf-8')											#convert byte-representation of char to char
	print( key)															#echo die gedrückte Taste
	return( key)														#return single letter
def my_cls(): 															#Säubere Anzeige (primitiv, aber kompatibel!)
	for i in range( 0, 40): print( " ")									#
	return()
def x_transform(x):														#transformiere ggf. x
	return( x)															#return transformed x
def y_transform( y):													#transformiere ggf. y
	return( math.log10(y) )												#return transformed y
def y_back_transform( y):												#rücktransformiere ggf. y
	return( math.pow( 10, y))
def y_fitted( x):														#compute fitted real y
	global a, b															#use global vars
	result= a * x_transform( x) + b										#fit in linearized form
	result= y_back_transform( result)									#back transformation
	return( result)														#return result
#main routine###########################################################
# vars...
no_rems= 0																#initialisiere Anzahl der Bemerkungen
no_flashes= 0															#initialisiere Anzahl der Wertepaare
no_xy= 0																#Initialisiere Anzahl der xy-Wertepaare
Idata= np.arange( 0., 1000., 1.)										#Probenstrom [A]
Udata= np.arange( 0., 1000., 1.)										#Probenspannung [V]
Bdata= np.arange( 0., 1000., 1.)										#Magnetfeld [T]
Tdata= np.arange( 0., 1000., 1.)										#Temperatur [K]
tdata= np.arange( 0., 1000., 1.)										#Zeit
Xdata= np.arange( 0., 1000., 1.)										#X-Werte für Berechnungen
Ydata= np.arange( 0., 1000., 1.)										#Y-Werte für Berechnungen
y_ordinate_n_dev= np.array( [ 0., 0.] )									#initialisiere Variable für Fit (y-Achsen-Abschnitt und Abweichung)
y_slope_n_dev= np.array( [ 0., 0.] )									#initialisiere Variable für Fit (Geradensteigung und Abweichung)
Rem= ' '																#Bemerkungen
sample_ID= "sample"														#Probenbezeichnung
E_criterion= 1.															#Kriterium für das elektrische Feld [µV/cm]
tap_distance= 4.	  													#Abstand der Spannungsabgriffe [cm]
Ic_result= 0.															#Ic [A]
B_result= 0.                         									#Magnetfeld [T] bei Ic
T_result= 0.															#Temperatur [K] bei Ic
Ecn_lo= 0.																#unteres E-Kriterium für n-Bestimmung
Ecn_hi= 0.																#oberes...
n_result= 0.															#n-Wert
n_dev= 0.																#Standardabweichung des n-Wertes
filename_dat= "HTS_Bi2223.dat"											#setze Dateinamen
# prepare global vars...
init_vars()																#ist immer geschickt, die Initialisierung nochmal in einer Funktion aufrufbar zu haben
while True:																#Hauptschleife des Programms
	my_cls()															#clear screen
	print( "This is <",this_program,">!")								#Welches Programm wird benutzt
	print( "==========================================================")#Menue...
	print( "0=quit")													#verlassen
	print( "f-filename                  :", filename_dat)				#Anzeige und Eingabe des Dateinamens
	print( "r=read data      ( flashes ):", no_flashes )				#Starte Einlesen der Datei und zeige Anzahl der Daten-Tupel an
	print( "t-voltage tap distance  [cm]:", tap_distance )				#Anzeige und Eingabe des Abstandes der Spannungsabgriffe
	print( "e-E-criterion Ec     [µV/cm]:", E_criterion )				#Anzeige und Eingabe des E-Feld-Kriteriums
	print( "i=search for Ic(Uc,T,B)")									#Starte suche nach Ic
	print( "v=view E(I) fast")											#Starte schnellen Plot E(I) (Messwerte)
	print( "n=compute n-value between       Ec and 10 x Ec")			#Starte Berechnung des n-Wertes im angegebenen Bereich des elektrischen Feldes
	print( "m=compute n-value between 0.1 x Ec and      Ec")			#Starte Berechnung des n-Wertes im angegebenen Bereich des elektrischen Feldes
	print( "w=compute n-value between ", Ecn_lo, " uV/cm (X) and ", Ecn_hi, " uV/cm (Y)") #Starte Berechnung des n-Wertes im angegebenen Bereich des elektrischen Feldes (X- und Y-Taste zur Eingabe eigener Grenzen)
	print( "RESULTS...................................................")#report
	print( "  Ic                     [A]:", Ic_result)					#Anzeige ermittelter Ic-Wert
	print( "  n                         :", n_result)					#Anzeige ermittelter n-Wert
	print( "b-magnetic field         [T]:", B_result )					#Anzeige und Eingabe des zugehörigen interpolierten B-Wertes
	print( "  temperature T          [K]:", T_result)					#Anzeige ermittelte Temperatur
	print( "l=log-plot");												#Starte log-log-plot im Fit-Bereich für n-Wert
	if opsys == "WINDOWS":
		key= my_keypress()												#warte auf Tatendruck (falls nicht kompatibel, dann durch "key= input()" ersetzen; braucht dann nur ein zusätzliches Drücken von "ENTER")
	else:
		key= input()
	if key =='0': break													#verlassen
	elif key == 'f': filename_dat= input()								#Eingabe Dateiname
	elif key == 'r': read_dat_file()									#Einlesen Daten aus Datei
	elif key == 't': tap_distance= input()								#Eingabe Abstand Spannungsabgriffe
	elif key == 'e': E_criterion= input()								#Eingabe Kriterium des elektrischen Feldes
	elif key == 'X': Ecn_lo= input()									#Eingabe unterer Wert des Intervalls im elektrischen Feld zur n-Wert-Bestimmung
	elif key == 'Y': Ecn_hi= input()									#...oberer...
	elif key == 'b': B_result= input()									#Eingabe zugehöriges B-Feld (zum "Glätten")
	elif key == "i": search_for_Ics()									#suche und interpoliere Ic und zugehörige Werte
	elif key == 'v': view_EI_fast()										#schnelle Ansicht der Messdaten
	elif key == 'm':													#fit für n-Wert...
		Ecn_lo= 0.1 * E_criterion										#passe Intervall an
		Ecn_hi= 1.0 * E_criterion										#...
		compute_n()														#starte Berechnng
	elif key == 'n':													#fit für n-Wert...
		Ecn_lo= 1.0 * E_criterion										#passe Intervall an
		Ecn_hi= 10. * E_criterion										#...
		compute_n()														#starte Berechnung
	elif key == 'w':													#fit für n-Wert...
		compute_n()														#starte Berechnung
	elif key == 'l': view_log_plot()									#starte log-log-Plot im n-Berechnungs-Bereich
########################################################################
#EOF
