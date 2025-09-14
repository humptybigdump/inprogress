# -*- coding: utf-8 -*-

# Hier importieren


import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import time



def funcAnalytischeLoesung(x):
	x_laenge = 1000.0
	y_laenge = 100.0
	z_laenge = 100.0
	EMod     = 210000.0
	Kraft    = 10000.0
	Flaechentragheit = y_laenge * (z_laenge**3) / 12
	Loesung  = Kraft / (EMod * Flaechentragheit) * (x_laenge * x**2/2 - x**3/6)
	return Loesung
    
# Definition der relevanten Arrays
elementGroesse     = (1000.0,500.0,200.0,100.0,50.0,20.0)
abaqusLoesung      = []
plotLoesung        = []
analytischeLoesung = []
varLoop            = 0

# Erstellung der Modelle und Berechnung

# Speichern der Verschiebungen im Array abaqusLoesung

# Berechnung der anayltischen Loesung

# Darstellung der anayltischen Loesung
time.sleep(5)   
xyp = session.XYPlot('Plot-Biegung')
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
plotLoesung += [ session.Curve(xyData=xyPlot.XYData(name="Analystische Loesung", data=analytischeLoesung)) ]
chart.setValues(curvesToPlot=plotLoesung, )
chart.axes2[0].axisData.setValues(useSystemTitle=False, title='Verschiebung-Z [mm]')
chart.axes1[0].axisData.setValues(useSystemTitle=False, title='Laengskoordinate [m]')
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
time.sleep(5)

# Darstellung der numerischen Loesung
varLoop = 0
for i in abaqusLoesung:
    groesse = elementGroesse[varLoop]
    nameVerlauf = 'Elementgroesse %6.4f mm' %groesse
    a = xyPlot.XYData(name=nameVerlauf, data=i)
    plotLoesung += [session.Curve(xyData=a)]
    varLoop += 1
    chart.setValues(curvesToPlot=plotLoesung, )
    time.sleep(5)