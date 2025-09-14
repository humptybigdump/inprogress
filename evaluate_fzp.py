import visualization
import xyPlot
import displayGroupOdbToolset as dgo

#from abaqus import *
from abaqusConstants import *
#from viewerModules import *

odb = session.openOdb(name='fzp_shells.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=odb)

for key in session.xyDataObjects.keys():
    del session.xyDataObjects[key]


## Meshsize 0.5 mm
xy_result = session.XYDataFromHistory(name='rf2_05', odb=odb, 
    outputVariableName='Total force on the surface: SOF2  on surface SEC_05', 
    steps=('Step-1', ), )
xy_result = session.XYDataFromHistory(name='u2_05_1', odb=odb, 
    outputVariableName='Spatial displacement: U2 at Node 273 in NSET NUY5_05', 
    steps=('Step-1', ), )
xy_result = session.XYDataFromHistory(name='u2_05_2', odb=odb, 
    outputVariableName='Spatial displacement: U2 at Node 696 in NSET NUY5_05', 
    steps=('Step-1', ), )
xy1 = session.xyDataObjects['u2_05_1']
xy2 = session.xyDataObjects['u2_05_2']
xy3 = session.xyDataObjects['rf2_05']
xy4 = combine((xy1-xy2)/10., xy3/(1.5*5.))
xy4.setValues(
    sourceDescription='combine(("u2_05_1"-"u2_05_2")/10., "rf2_05"/(1.5*5.))')
tmpName = xy4.name
session.xyDataObjects.changeKey(tmpName, 'stress-strain_05')
xQuantity = visualization.QuantityType(type=STRAIN)
yQuantity = visualization.QuantityType(type=STRESS)
session.xyDataObjects['stress-strain_05'].setValues(
    axis1QuantityType=xQuantity, axis2QuantityType=yQuantity, )


## Meshsize 1.25 mm
xy_result = session.XYDataFromHistory(name='rf2_125', odb=odb, 
    outputVariableName='Total force on the surface: SOF2  on surface SEC_125', 
    steps=('Step-1', ), )
xy_result = session.XYDataFromHistory(name='u2_125_1', odb=odb, 
    outputVariableName='Spatial displacement: U2 at Node 5 in NSET NUY5_125', 
    steps=('Step-1', ), )
xy_result = session.XYDataFromHistory(name='u2_125_2', odb=odb, 
    outputVariableName='Spatial displacement: U2 at Node 140 in NSET NUY5_125', 
    steps=('Step-1', ), )
xy1 = session.xyDataObjects['u2_125_1']
xy2 = session.xyDataObjects['u2_125_2']
xy3 = session.xyDataObjects['rf2_125']
xy4 = combine((xy1-xy2)/10., xy3/(1.5*5.))
xy4.setValues(
    sourceDescription='combine(("u2_125_1"-"u2_125_2")/10., "rf2_125"/(1.5*5.))')
tmpName = xy4.name
session.xyDataObjects.changeKey(tmpName, 'stress-strain_125')
xQuantity = visualization.QuantityType(type=STRAIN)
yQuantity = visualization.QuantityType(type=STRESS)
session.xyDataObjects['stress-strain_125'].setValues(
    axis1QuantityType=xQuantity, axis2QuantityType=yQuantity, )


## Meshsize 2.5 mm
xy_result = session.XYDataFromHistory(name='rf2_25', odb=odb, 
    outputVariableName='Total force on the surface: SOF2  on surface SEC_25', 
    steps=('Step-1', ), )
xy_result = session.XYDataFromHistory(name='u2_25_2', odb=odb, 
    outputVariableName='Spatial displacement: U2 at Node 1744 in NSET NUY5_25', 
    steps=('Step-1', ), )
xy_result = session.XYDataFromHistory(name='u2_25_1', odb=odb, 
    outputVariableName='Spatial displacement: U2 at Node 2879 in NSET NUY5_25', 
    steps=('Step-1', ), )
xy1 = session.xyDataObjects['u2_25_1']
xy2 = session.xyDataObjects['u2_25_2']
xy3 = session.xyDataObjects['rf2_25']
xy4 = combine((xy1-xy2)/10., xy3/(1.5*5.))
xy4.setValues(
    sourceDescription='combine(("u2_25_1"-"u2_25_2")/10., "rf2_25"/(1.5*5.))')
tmpName = xy4.name
session.xyDataObjects.changeKey(tmpName, 'stress-strain_25')
xQuantity = visualization.QuantityType(type=STRAIN)
yQuantity = visualization.QuantityType(type=STRESS)
session.xyDataObjects['stress-strain_25'].setValues(
    axis1QuantityType=xQuantity, axis2QuantityType=yQuantity, )


## Experimental Data
session.XYDataFromFile(name='stress-strain_exp_1', 
    fileName='MY3-GW-Fz-S3L.txt', 
    xField=1, yField=2, 
    sourceDescription='Read from MY3-GW-Fz-S3L.txt',
    contentDescription='field 1 vs. field 2')
xQuantity = visualization.QuantityType(type=STRAIN)
yQuantity = visualization.QuantityType(type=STRESS)
session.xyDataObjects['stress-strain_exp_1'].setValues(
    axis1QuantityType=xQuantity, axis2QuantityType=yQuantity, )

# clean temporary Data
for key in session.xyDataObjects.keys():
    if key not in ['stress-strain_05',
                   'stress-strain_125', 'stress-strain_25',
                   'stress-strain_exp_1']:
        del session.xyDataObjects[key]
    
# Plot Results
try:
    xyp = session.XYPlot('XYPlot-1')    
except:
	xyp = session.xyPlots['XYPlot-1']
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
xy2 = session.xyDataObjects['stress-strain_05']
c2 = session.Curve(xyData=xy2)
xy3 = session.xyDataObjects['stress-strain_125']
c3 = session.Curve(xyData=xy3)
xy4 = session.xyDataObjects['stress-strain_25']
c4 = session.Curve(xyData=xy4)
xy5 = session.xyDataObjects['stress-strain_exp_1']
c5 = session.Curve(xyData=xy5)
chart.setValues(curvesToPlot=(c2, c3, c4, c5 ), )
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
session.charts['Chart-1'].legend.textStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
session.charts['Chart-1'].legend.titleStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
session.charts['Chart-1'].axes2[0].labelStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
session.charts['Chart-1'].axes1[0].labelStyle.setValues(
    font='-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
session.curves['stress-strain_05'].lineStyle.setValues(thickness=0.5)
session.curves['stress-strain_25'].lineStyle.setValues(thickness=0.5)
session.curves['stress-strain_125'].lineStyle.setValues(thickness=0.5)
session.curves['stress-strain_exp_1'].lineStyle.setValues(thickness=0.8)
session.curves['stress-strain_exp_1'].lineStyle.setValues(style=DOT_DASH)
session.curves['stress-strain_exp_1'].lineStyle.setValues(color='#000000')   
