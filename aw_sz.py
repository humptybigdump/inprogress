# -*- coding: mbcs -*-
#
# Abaqus/Viewer Release 6.13-1 replay file
# Internal Version: 2013_05_16-01.56.28 126354
# Run by som on Mon Jan 13 19:12:33 2014
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
from viewerModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
#: Executing "onCaeStartup()" in the site directory ...
o1 = session.openOdb(name='scherzug.odb')
odb = session.odbs['scherzug.odb']

## retrieve data of interest
rf1 = session.XYDataFromHistory(name='RF1', odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10306 in NSET SZ_MPC', 
    steps=('Step-1', ), )
u1 = session.XYDataFromHistory(name='U1', odb=odb, 
    outputVariableName='Spatial displacement: U1 at Node 10306 in NSET SZ_MPC', 
    steps=('Step-1', ), )
xy1 = session.xyDataObjects['U1']
xy2 = session.xyDataObjects['RF1']
xy3 = combine(xy1, xy2)
xy3.setValues(sourceDescription='combine ( "U1", "RF1" )')
tmpName = xy3.name
if 'kw_sz' in session.xyDataObjects:
	del session.xyDataObjects['kw_sz']
session.xyDataObjects.changeKey(tmpName, 'kw_sz')

## plot resulting curve
if 'XYPlot-1' in session.xyPlots:
	del session.xyPlots['XYPlot-1']
xyp = session.XYPlot('XYPlot-1')
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
xy1 = session.xyDataObjects['kw_sz']
c1 = session.Curve(xyData=xy1)
chart.setValues(curvesToPlot=(c1, ), )
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)

## increase font size
fontstyle = "-*-arial-medium-r-normal-*-*-160-*-*-p-*-*-*"
session.xyPlots['XYPlot-1'].charts[chartName].axes1[0].titleStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].axes2[0].titleStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].axes1[0].labelStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].axes2[0].labelStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].legend.textStyle.setValues(font=fontstyle )