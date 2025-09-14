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
	
	# Auswahl der groesssten Verschiebung
			
	# Auswahl der groessten Spannung
	
	# Berechnung des Gesamtvolumens durch Summe ueber alle Elementvolumina

	# Ablegen alle Groesssen im Array lst

# Ausgabe der Ergebnisse ueber print Befehl    
print ("Bauteilvolumen [cm^3] , maximale vertikale Verscheibung [mm] , maximale Normalspannung [MPA]")
for i in lst:
    print i
