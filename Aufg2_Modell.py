
from abaqus import *
from abaqusConstants import *

import regionToolset
import displayGroupMdbToolset as dgm
import xyPlot
import displayGroupOdbToolset as dgo
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

# Funktion die den Querschnitt im Skizzierer zeichnet
def sketchQuerschnitt(h, b, elementGroessse, i):
    
    return returnPoints

# Funktion die die Netzgroesse anpasst
def fktElementGroessse(b, AnzahlIteration):
   
    return elementGroessse

h               = 100.0
b               = 100.0
depth           = 1000.0
AnzahlIteration = 5
elementGroessse = fktElementGroessse (b=b,AnzahlIteration=AnzahlIteration)

for i in range(0, AnzahlIteration):
	
#---------------------------------JOB------------------------------------------------------
    Aufgabe = 'Querschnitt%i' %i
    mdb.Job(name=Aufgabe, model='Model-1', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB)
    mdb.jobs[Aufgabe].submit(consistencyChecking=OFF)
    mdb.jobs[Aufgabe].waitForCompletion()


