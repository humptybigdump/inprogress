from abaqus import *
from abaqusConstants import *

from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *

# Ergebnisse in ABAQUS nicht in der richtigen Reihenfolge, kann durch bubbleSort angepasst werden
def bubbleSort (lst):
    for i in range(0, len(lst)):
        for j in range( 0, len(lst)-i-1):
            if lst[j][0] >lst[j+1][0]:
                tempVar = lst[j+1]
                lst[j+1] = lst[j]
                lst[j] = tempVar
    return lst

# Funktion gibt das Array lst mit der x-Koordinate in m und der Verschiebung in z-Richtung in mm zurueck
# Bei Bedarf Step-Name und .odb Name anpassen
def getVerlauf(varLoop):
    Datei = 'Biegung%i.odb' %varLoop
    odb = openOdb(path=Datei)  
    lastFrame = odb.steps["Elastostatik"].frames[-1]
    Verschiebungen = lastFrame.fieldOutputs['U'].values
    lst = []
    for KnotenVerschiebung in Verschiebungen:
        U = KnotenVerschiebung.data[2]
        varNode = KnotenVerschiebung.nodeLabel
        x = KnotenVerschiebung.instance.nodes[varNode-1].coordinates[0]
        y = KnotenVerschiebung.instance.nodes[varNode-1].coordinates[1]
        z = KnotenVerschiebung.instance.nodes[varNode-1].coordinates[2]
		
		# Welche Nodes liegen auf der Mittelachse? Deren Verschiebung und X-Koordinate in lst speichern
        
		# Sortieren der Nodes mithilfe von bubbleSort
        
    return lst
