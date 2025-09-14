# -*- coding: mbcs -*-
#
# ABAQUS/Viewer Version 6.7-PR3D replay file
# Internal Version: 2007_04_19-08.16.06 75488
# Run by som on Tue Jun 12 17:24:46 2007
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
o1 = session.openOdb(name='kzsasz.odb')
odb = session.odbs['kzsasz.odb']

## retrieve data of interest
xy0 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10014 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy1 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10036 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy2 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10055 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy3 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10058 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy4 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10076 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy5 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10097 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy6 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10119 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy7 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10122 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy8 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10142 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy9 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10152 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy10 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10156 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy11 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10164 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy12 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10176 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy13 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10180 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy14 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10225 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy15 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10232 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy16 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10244 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy17 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF1 at Node 10268 in NSET SZ_NO_FEST', 
    steps=('Step-1', ))
xy18 = sum((xy0, xy1, xy2, xy3, xy4, xy5, xy6, xy7, xy8, xy9, xy10, xy11, xy12, 
    xy13, xy14, xy15, xy16, xy17))
session.XYData(name='k_SZ_sum', objectToCopy=xy18, 
    sourceDescription='sum( Reaction force: RF1 at Node 10014 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10036 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10055 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10058 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10076 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10097 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10119 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10122 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10142 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10152 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10156 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10164 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10176 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10180 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10225 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10232 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10244 in NSET SZ_NO_FEST,Reaction force: RF1 at Node 10268 in NSET SZ_NO_FEST )')

xy0 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1352 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy1 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1353 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy2 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1354 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy3 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1355 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy4 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1356 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy5 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1357 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy6 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1358 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy7 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1359 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy8 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1360 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy9 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1361 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy10 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1362 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy11 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1363 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy12 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1364 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy13 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1365 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy14 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1366 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy15 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1367 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy16 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1368 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy17 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1437 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy18 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1438 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy19 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1439 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy20 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1440 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy21 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1441 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy22 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1442 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy23 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1443 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy24 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1444 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy25 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1445 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy26 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1446 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy27 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1447 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy28 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1448 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy29 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1449 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy30 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1450 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy31 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1451 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy32 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1452 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy33 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1453 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy34 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1464 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy35 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1465 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy36 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1474 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy37 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1475 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy38 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1476 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy39 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1477 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy40 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1496 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy41 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1497 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy42 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1521 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy43 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 1526 in NSET KZ_NO_FEST', 
    steps=('Step-1', ))
xy44 = sum((xy0, xy1, xy2, xy3, xy4, xy5, xy6, xy7, xy8, xy9, xy10, xy11, xy12, 
    xy13, xy14, xy15, xy16, xy17, xy18, xy19, xy20, xy21, xy22, xy23, xy24, 
    xy25, xy26, xy27, xy28, xy29, xy30, xy31, xy32, xy33, xy34, xy35, xy36, 
    xy37, xy38, xy39, xy40, xy41, xy42, xy43))
session.XYData(name='k_KZ_sum', objectToCopy=xy44, 
    sourceDescription='sum( Reaction force: RF3 at Node 1352 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1353 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1354 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1355 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1356 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1357 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1358 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1359 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1360 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1361 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1362 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1363 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1364 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1365 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1366 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1367 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1368 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1437 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1438 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1439 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1440 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1441 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1442 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1443 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1444 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1445 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1446 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1447 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1448 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1449 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1450 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1451 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1452 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1453 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1464 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1465 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1474 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1475 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1476 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1477 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1496 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1497 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1521 in NSET KZ_NO_FEST,Reaction force: RF3 at Node 1526 in NSET KZ_NO_FEST )')

xy0 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5431 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy1 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5432 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy2 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5433 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy3 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5434 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy4 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5435 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy5 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5436 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy6 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5437 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy7 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5438 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy8 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5439 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy9 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5440 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy10 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5441 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy11 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5442 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy12 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5443 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy13 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5444 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy14 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5445 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy15 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5446 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy16 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5448 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy17 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 at Node 5466 in NSET SA_NO_FEST', 
    steps=('Step-1', ))
xy18 = sum((xy0, xy1, xy2, xy3, xy4, xy5, xy6, xy7, xy8, xy9, xy10, xy11, xy12, 
    xy13, xy14, xy15, xy16, xy17))
session.XYData(name='k_SA_sum', objectToCopy=xy18, 
    sourceDescription='sum( Reaction force: RF3 at Node 5431 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5432 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5433 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5434 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5435 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5436 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5437 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5438 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5439 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5440 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5441 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5442 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5443 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5444 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5445 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5446 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5448 in NSET SA_NO_FEST,Reaction force: RF3 at Node 5466 in NSET SA_NO_FEST )')

session.XYDataFromHistory(name='u_kz', odb=odb, 
    outputVariableName='Spatial displacement: U3 at Node 1085 in NSET NAUSWERT', 
    steps=('Step-1', ))

session.XYDataFromHistory(name='u_sa', odb=odb, 
    outputVariableName='Spatial displacement: U3 at Node 5190 in NSET NAUSWERT', 
    steps=('Step-1', ))
odb = session.odbs['kzsasz.odb']
session.XYDataFromHistory(name='u_sz', odb=odb, 
    outputVariableName='Spatial displacement: U1 at Node 10306 in NSET NAUSWERT', 
    steps=('Step-1', ))
xy1 = session.xyDataObjects['u_kz']
xy2 = session.xyDataObjects['k_KZ_sum']
xy3 = combine(xy1, xy2*(-0.001))
session.XYData(name='Sim. Kopfzug', objectToCopy=xy3, 
    sourceDescription='combine ( "u_kz", "k_KZ_sum"*(-0.001) )')
xy1 = session.xyDataObjects['u_sa']
xy2 = session.xyDataObjects['k_SA_sum']
xy3 = combine(xy1, xy2*(-0.001))
session.XYData(name='Sim. Schaelzug', objectToCopy=xy3, 
    sourceDescription='combine ( "u_sa", "k_SA_sum"*(-0.001) )')
xy1 = session.xyDataObjects['u_sz']
xy2 = session.xyDataObjects['k_SZ_sum']
xy3 = combine(xy1, xy2*(-0.001))
session.XYData(name='Sim. Scherzug', objectToCopy=xy3, 
    sourceDescription='combine ( "u_sz", "k_SZ_sum"*(-0.001) )')

### Kraft-Zeit
xy2 = session.xyDataObjects['k_KZ_sum']
xy3 = xy2*(-0.001)
session.XYData(name='Sim. Kopfzug, Kraft-Zeit', objectToCopy=xy3, 
    sourceDescription='"k_KZ_sum"*(-0.001)')
	
xy2 = session.xyDataObjects['k_SA_sum']
xy3 = xy2*(-0.001)
session.XYData(name='Sim. Schaelzug, Kraft-Zeit', objectToCopy=xy3, 
    sourceDescription='"k_SA_sum"*(-0.001)')
	
xy2 = session.xyDataObjects['k_SZ_sum']
xy3 = xy2*(-0.001)
session.XYData(name='Sim. Scherzug, Kraft-Zeit', objectToCopy=xy3, 
    sourceDescription='"k_SZ_sum"*(-0.001)')

session.XYDataFromFile(name='Exp. Scherzug, Probe 1', 
    fileName='ex_dp600_kv_scher_MX3_Sz_S3.txt', 
    xField=1, yField=2, 
    sourceDescription='Read from ex_dp600_kv_scher_MX3_Sz_S3.txt', 
    contentDescription='field 1 vs. field 2')
session.XYDataFromFile(name='Exp. Scherzug, Probe 2', 
    fileName='ex_dp600_kv_scher_MX3_Sz_S5.txt', 
    xField=1, yField=2, 
    sourceDescription='Read from ex_dp600_kv_scher_MX3_Sz_S5.txt', 
    contentDescription='field 1 vs. field 2')
session.XYDataFromFile(name='Exp. Scherzug, Probe 3', 
    fileName='ex_dp600_kv_scher_MX3_Sz_S6.txt', 
    xField=1, yField=2, 
    sourceDescription='Read from ex_dp600_kv_scher_MX3_Sz_S6.txt', 
    contentDescription='field 1 vs. field 2')
session.XYDataFromFile(name='Exp. Schaelzug, Probe 2', 
    fileName='ex_dp600_kv_schael_MX3_Sa_S5.txt', 
    xField=1, yField=2, 
    sourceDescription='Read from ex_dp600_kv_schael_MX3_Sa_S5.txt', 
    contentDescription='field 1 vs. field 2')
session.XYDataFromFile(name='Exp. Schaelzug, Probe 1', 
    fileName='ex_dp600_kv_schael_MX3_Sa_S4.txt', 
    xField=1, yField=2, 
    sourceDescription='Read from ex_dp600_kv_schael_MX3_Sa_S4.txt', 
    contentDescription='field 1 vs. field 2')
session.XYDataFromFile(name='Exp. Kopfzug', 
    fileName='ex_dp600_kv_ks2_90_qs.txt', 
    xField=1, yField=2, 
    sourceDescription='Read from ex_dp600_kv_ks2_90_qs.txt', 
    contentDescription='field 1 vs. field 2')

## plot resulting curve
if 'XYPlot-1' in session.xyPlots:
	del session.xyPlots['XYPlot-1']                      
xyp = session.XYPlot('XYPlot-1')

chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
xy1 = session.xyDataObjects['Exp. Kopfzug']
c1 = session.Curve(xyData=xy1)
xy2 = session.xyDataObjects['Sim. Kopfzug']
c2 = session.Curve(xyData=xy2)
xy3 = session.xyDataObjects['Sim. Schaelzug']
c3 = session.Curve(xyData=xy3)
xy4 = session.xyDataObjects['Sim. Scherzug']
c4 = session.Curve(xyData=xy4)
xy5 = session.xyDataObjects['Exp. Schaelzug, Probe 1']
c5 = session.Curve(xyData=xy5)
xy6 = session.xyDataObjects['Exp. Schaelzug, Probe 2']
c6 = session.Curve(xyData=xy6)
xy7 = session.xyDataObjects['Exp. Scherzug, Probe 1']
c7 = session.Curve(xyData=xy7)
xy8 = session.xyDataObjects['Exp. Scherzug, Probe 2']
c8 = session.Curve(xyData=xy8)
xy9 = session.xyDataObjects['Exp. Scherzug, Probe 3']
c9 = session.Curve(xyData=xy9)
chart.setValues(curvesToPlot=(c1, c2, c3, c4, c5, c6, c7, c8, c9, ), )

session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
session.curves['Sim. Kopfzug'].lineStyle.setValues(color='#FF0000')
session.curves['Sim. Kopfzug'].lineStyle.setValues(style=SOLID)
session.curves['Exp. Kopfzug'].lineStyle.setValues(style=DASHED)
session.curves['Sim. Schaelzug'].lineStyle.setValues(color='#0000FF')
session.curves['Exp. Schaelzug, Probe 1'].lineStyle.setValues(thickness=0.8)
session.curves['Exp. Schaelzug, Probe 1'].lineStyle.setValues(style=DASHED)
session.curves['Exp. Schaelzug, Probe 2'].lineStyle.setValues(color='#00FFFF')
session.curves['Exp. Schaelzug, Probe 2'].lineStyle.setValues(style=DOT_DASH)
session.curves['Exp. Schaelzug, Probe 2'].lineStyle.setValues(thickness=0.8)
session.curves['Exp. Kopfzug'].lineStyle.setValues(thickness=0.5)
session.curves['Exp. Kopfzug'].lineStyle.setValues(thickness=0.5)
session.curves['Exp. Scherzug, Probe 3'].lineStyle.setValues(style=DOTTED)
session.curves['Exp. Scherzug, Probe 3'].lineStyle.setValues(color='#00FF00')
session.curves['Exp. Scherzug, Probe 3'].lineStyle.setValues(thickness=0.8)
session.curves['Exp. Scherzug, Probe 3'].lineStyle.setValues(style=DOT_DASH)
session.curves['Exp. Scherzug, Probe 2'].lineStyle.setValues(style=DOT_DASH)
session.curves['Exp. Scherzug, Probe 2'].lineStyle.setValues(color='#008000')
session.curves['Exp. Scherzug, Probe 2'].lineStyle.setValues(thickness=0.8)
session.curves['Exp. Scherzug, Probe 3'].lineStyle.setValues(style=DOT_DASH)
session.curves['Exp. Scherzug, Probe 1'].lineStyle.setValues(color='#008080')
session.curves['Exp. Scherzug, Probe 1'].lineStyle.setValues(style=DOT_DASH)
session.curves['Exp. Scherzug, Probe 1'].lineStyle.setValues(thickness=0.8)
session.curves['Exp. Scherzug, Probe 1'].lineStyle.setValues(style=DASHED)
session.curves['Exp. Scherzug, Probe 3'].lineStyle.setValues(style=DOTTED)
session.charts[chartName].legend.area.setValues(positionMethod=MANUAL, 
    originOffset=(0.769109, 0))
session.viewports['Viewport: 1'].odbDisplay.basicOptions.setValues(
    connectorDisplay=ON)
chartName = xyp.charts.keys()[0]
session.charts[chartName].axes2[1].axisData.setValues(minValue=0, 
    minAutoCompute=False)
session.charts[chartName].axes2[1].axisData.setValues(maxValue=18, 
    maxAutoCompute=False)
session.charts[chartName].axes2[0].axisData.setValues(maxValue=18, 
    maxAutoCompute=False)
session.charts[chartName].axes1[0].axisData.setValues(minValue=0, 
    minAutoCompute=False)
session.charts[chartName].axes1[1].axisData.setValues(minValue=0, 
    minAutoCompute=False)
session.charts[chartName].axes1[1].axisData.setValues(maxValue=13, 
    maxAutoCompute=False)
session.charts[chartName].axes1[0].axisData.setValues(maxValue=13, 
    maxAutoCompute=False)
    
## increase font size
fontstyle = "-*-arial-medium-r-normal-*-*-160-*-*-p-*-*-*"
session.xyPlots['XYPlot-1'].charts[chartName].axes1[0].titleStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].axes2[0].titleStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].axes1[0].labelStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].axes2[0].labelStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].axes1[1].labelStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].axes2[1].labelStyle.setValues(font=fontstyle )
session.xyPlots['XYPlot-1'].charts[chartName].legend.textStyle.setValues(font=fontstyle )

