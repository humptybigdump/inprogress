
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
    versatzH = elementGroessse
    while (versatzH < 0.2*h):
        versatzH += elementGroessse
    versatzB = i*elementGroessse
    returnPoints = ((0.0,0.0), (versatzH, 0.0), (versatzH, versatzB) , (h-versatzH,versatzB), (h-versatzH , 0.0), (h,0.0), (h,b),
                    (h-versatzH,b), (h-versatzH,b-versatzB), (versatzH,b-versatzB), (versatzH,b), (0.0,b), (0.0,0.0) )
    return returnPoints

# Funktion die die Netzgroesse anpasst
def fktElementGroessse(b, AnzahlIteration):
    AnzahlElemente = (AnzahlIteration)*2.0
    elementGroessse = (b*1.0) / AnzahlElemente
    return elementGroessse

h               = 100.0
b               = 100.0
depth           = 1000.0
AnzahlIteration = 5
elementGroessse = fktElementGroessse (b=b,AnzahlIteration=AnzahlIteration)

for i in range(0, AnzahlIteration):
    #---------------------------------PART------------------------------------------------------
    # 2D-Skizze
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
	# Berechnung der Lage der Punkte 0-11
    Punkte = sketchQuerschnitt(h=h,b=b, elementGroessse=elementGroessse, i=i)
	# Skizze mit den berechneten Punkten
    for j in range(0,len(Punkte)-1):
        mdb.models['Model-1'].sketches['__profile__'].Line(point1=Punkte[j], point2=Punkte[j+1])
		
    # Extrusion zu 3D Bauteil
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Balken', type=DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Balken'].BaseSolidExtrude(depth=1000.0, sketch=mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    
	# Definition des Kraftsangriffspunkts
    cells = mdb.models['Model-1'].parts['Balken'].cells.findAt(((0.0, 0.0, 0.0), ))
    mdb.models['Model-1'].parts['Balken'].PartitionCellByPlaneThreePoints(cells=cells, point1=(0.0,50.0,0.0), point2=(100.0,50.0,0.0), point3=(100.0,50.0,1000.0))
    cells = mdb.models['Model-1'].parts['Balken'].cells.findAt(((0.0, 49.5, 0.0), ),)
    mdb.models['Model-1'].parts['Balken'].PartitionCellByPlaneThreePoints(cells=cells, point1=(50.0,0.0,0.0), point2=(50.0,50.0,0.0), point3=(50.0,50.0,1000.0))
    cells = mdb.models['Model-1'].parts['Balken'].cells.findAt(((0.0, 50.5, 0.0), ),)
    mdb.models['Model-1'].parts['Balken'].PartitionCellByPlaneThreePoints(cells=cells, point1=(50.0,100.0,0.0), point2=(50.0,50.0,0.0), point3=(50.0,50.0,1000.0))    
	
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
    mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 1.0, 0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('Balken-1', ))
	
#---------------------------------STEP------------------------------------------------------
    # Step
    mdb.models['Model-1'].StaticStep(name='Elastostatik', previous='Initial')
	
    # Field Output
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('E', 'U', 'EVOL', 'S'))
	
#---------------------------------LOAD------------------------------------------------------
    # Dirichlet-Randbedingung
    mdb.models['Model-1'].rootAssembly.Set(faces=mdb.models['Model-1'].rootAssembly.instances['Balken-1'].faces.findAt(((0.0, 49.5, -49.5), ), ((0.0, 50.5, -49.5), ), ((0.0, 49.5, -50.5), ), ((0.0, 50.5, -50.5), ) ,) , name='EinspannFlaeche')
    mdb.models['Model-1'].EncastreBC(createStepName='Initial', localCsys=None, name='Einspannung', region=mdb.models['Model-1'].rootAssembly.sets['EinspannFlaeche'])
	
    # Neumann-Randbedingung
    mdb.models['Model-1'].rootAssembly.Set(name='Angriffspunkt', vertices=mdb.models['Model-1'].rootAssembly.instances['Balken-1'].vertices.findAt(((1000.0, 50.0, -50.0), ), ))
    mdb.models['Model-1'].ConcentratedForce(cf3=10000.0, createStepName='Elastostatik', distributionType=UNIFORM, field='', localCsys=None, name='Kraft', region=mdb.models['Model-1'].rootAssembly.sets['Angriffspunkt'])
	
#---------------------------------MESH------------------------------------------------------
    # Aufruf der ABAQUS internen Funktion seedPart
    # elementGroesse wird als 'seed size' uebergeben   
    mdb.models['Model-1'].parts['Balken'].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=elementGroessse)
	
    # Aufruf der ABAQUS internen Funktion setElementType, die den Elementtyp festlegt
    mdb.models['Model-1'].parts['Balken'].setElementType(elemTypes=(ElemType(elemCode=C3D8, elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(mdb.models['Model-1'].parts['Balken'].cells.getSequenceFromMask(('[#f ]', ), ), ))
	
    #Aufruf einer Funktion setMeshControls, die das anzuwendenden Algorithm festlegt
    mdb.models['Model-1'].parts['Balken'].setMeshControls(algorithm=MEDIAL_AXIS, regions=mdb.models['Model-1'].parts['Balken'].cells.getSequenceFromMask(('[#f ]', ), ))
    
	# Aufruf der ABAQUS internen Funktion generateMesh, die das Netz erzeugt
    mdb.models['Model-1'].parts['Balken'].generateMesh()
    mdb.models['Model-1'].rootAssembly.regenerate()
	
#---------------------------------JOB------------------------------------------------------
    Aufgabe = 'Querschnitt%i' %i
    mdb.Job(name=Aufgabe, model='Model-1', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB)
    mdb.jobs[Aufgabe].submit(consistencyChecking=OFF)
    mdb.jobs[Aufgabe].waitForCompletion()


