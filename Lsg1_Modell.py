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
    # Skizze in der xy-Ebene
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0, 0), point2=(100.0, 100.0))
	
    # Extrusion zu 3D Bauteil
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Balken', type=DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Balken'].BaseSolidExtrude(depth=1000.0, sketch=mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
	
    # Definition des Kraftsangriffspunkts
    mdb.models['Model-1'].parts['Balken'].PartitionCellByPlanePointNormal(cells=mdb.models['Model-1'].parts['Balken'].cells.getSequenceFromMask(('[#1 ]', ), ), normal=mdb.models['Model-1'].parts['Balken'].edges[4], point=mdb.models['Model-1'].parts['Balken'].InterestingPoint(mdb.models['Model-1'].parts['Balken'].edges[4], MIDDLE))
    mdb.models['Model-1'].parts['Balken'].PartitionCellByPlaneNormalToEdge(cells=mdb.models['Model-1'].parts['Balken'].cells.getSequenceFromMask(('[#3 ]', ), ), edge=mdb.models['Model-1'].parts['Balken'].edges[14], point=mdb.models['Model-1'].parts['Balken'].InterestingPoint(mdb.models['Model-1'].parts['Balken'].edges[14], MIDDLE))
	
#---------------------------------MATERIAL------------------------------------------------------
    # Material
    mdb.models['Model-1'].Material(name='Stahl')
    mdb.models['Model-1'].materials['Stahl'].Elastic(table=((210000.0, 0.3), ))
	
    # Section
    mdb.models['Model-1'].HomogeneousSolidSection(material='Stahl', name='Stahlschnitt', thickness=None)
	
    # Zuweisung
    mdb.models['Model-1'].parts['Balken'].Set(cells=mdb.models['Model-1'].parts['Balken'].cells.getSequenceFromMask(('[#f ]', ), ), name='Gesamtbalken')
    mdb.models['Model-1'].parts['Balken'].SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=mdb.models['Model-1'].parts['Balken'].sets['Gesamtbalken'], sectionName='Stahlschnitt', thicknessAssignment=FROM_SECTION)
	
#---------------------------------ASSEMBLY------------------------------------------------------    
	
	# Erzeugung der Assembly
    mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Balken-1', part=mdb.models['Model-1'].parts['Balken'])
	
    # Drehung des KOS
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 10.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Balken-1', ))
	
#---------------------------------LOAD------------------------------------------------------
    # Step
    mdb.models['Model-1'].StaticStep(name='Elastostatik', previous='Initial')
	
    # Field Output
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('E', 'U', 'EVOL', 'S'))
	
    # Dirichlet-Randbedingung
    mdb.models['Model-1'].rootAssembly.Set(faces=mdb.models['Model-1'].rootAssembly.instances['Balken-1'].faces.getSequenceFromMask(('[#80460 ]', ), ), name='EinspannFlaeche')
    mdb.models['Model-1'].EncastreBC(createStepName='Initial', localCsys=None, name='Einspannung', region=mdb.models['Model-1'].rootAssembly.sets['EinspannFlaeche'])
	
    # Neumann-Randbedingung
    mdb.models['Model-1'].rootAssembly.Set(name='Angriffspunkt', vertices=mdb.models['Model-1'].rootAssembly.instances['Balken-1'].vertices.getSequenceFromMask(('[#1 ]', ), ))
    mdb.models['Model-1'].ConcentratedForce(cf3=10000.0, createStepName='Elastostatik', distributionType=UNIFORM, field='', localCsys=None, name='Kraft', region=mdb.models['Model-1'].rootAssembly.sets['Angriffspunkt'])
	
#---------------------------------MESH------------------------------------------------------
    # Aufruf der ABAQUS internen Funktion seedPart
    # elementGroesse wird als 'seed size' uebergeben    
    mdb.models['Model-1'].parts['Balken'].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=elementGroesse)
	
    # Aufruf der ABAQUS internen Funktion setElementType, die den Elementtyp festlegt
    mdb.models['Model-1'].parts['Balken'].setElementType(elemTypes=(ElemType(elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(mdb.models['Model-1'].parts['Balken'].cells.getSequenceFromMask(('[#f ]', ), ), ))
	
    # Aufruf der ABAQUS internen Funktion generateMesh, die das Netz erzeugt    
    mdb.models['Model-1'].parts['Balken'].generateMesh()
    mdb.models['Model-1'].rootAssembly.regenerate()
	
#---------------------------------JOB------------------------------------------------------
    # Definition des Jobs
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

