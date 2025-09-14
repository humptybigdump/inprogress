from abaqus import *
from abaqusConstants import *

from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *


# Definition des Arrays lst in dem Ergebnisse gespeichert werden
lst                = []
anzahlQuerschnitte = 5


for i in range(0,anzahlQuerschnitte):
    # Oeffnen der ODB
    Datei = 'Querschnitt%i.odb' %(i)
    odb = openOdb(path=Datei)  
    lastFrame = odb.steps["Elastostatik"].frames[-1]
	
	# Auswahl der groesssten Verschiebung
    Verschiebungen = lastFrame.fieldOutputs['U'].values
    maxVerschiebung = 0
    for ElementVerschiebung in Verschiebungen:
        U3 = ElementVerschiebung.data[2]
        if abs(U3) > maxVerschiebung:
            maxVerschiebung = abs(U3)
			
	# Auswahl der groessten Spannung
    Spannungen = lastFrame.fieldOutputs['S'].values
    maxSpannung = 0
    for ElementSpannung in Spannungen:
        S11 = ElementSpannung.data[0]
        if S11 > maxSpannung:
            maxSpannung = S11
	
	# Berechnung des Gesamtvolumens durch Summe ueber alle Elementvolumina
    Volumen = lastFrame.fieldOutputs['EVOL'].values
    GesamtVolumen = 0
    for ElementVolumen in Volumen:
        GesamtVolumen += ElementVolumen.data
		
	# Ablegen alle Groesssen im Array lst
    lst += ['%6.2f %6.2f %6.2f' %((GesamtVolumen/(10**6)), maxVerschiebung , maxSpannung) ]

# Ausgabe der Ergebnisse ueber print Befehl    
print ("Bauteilvolumen [cm^3] , maximale vertikale Verscheibung [mm] , maximale Normalspannung [MPA]")
for i in lst:
    print i
