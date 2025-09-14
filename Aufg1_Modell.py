from abaqus import *
from abaqusConstants import *
import __main__

def modellErstellung(elementGroesse, varLoop):
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

#---------------------------------PART------------------------------------------------------
    
#---------------------------------MATERIAL------------------------------------------------------
    
#---------------------------------ASSEMBLY------------------------------------------------------    

#---------------------------------LOAD------------------------------------------------------

#---------------------------------MESH------------------------------------------------------

#---------------------------------JOB------------------------------------------------------
    # Definition des Jobs, Modellbezeichnung bei Bedarf anpassen
    jobName = 'Biegung%i' %varLoop
    mdb.Job(name=jobName, model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB)
    mdb.jobs[jobName].submit(consistencyChecking=OFF)
	
	# Die Funktion waitForCompletion haelt die Ausfuehrung des Skripts so lange an, bis der Job 'completed' ist
    mdb.jobs[jobName].waitForCompletion()

