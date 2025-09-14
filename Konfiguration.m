%{
Bearbeiter: Niklas Bargen; Pratap Shenoy
Firma:      KIT - Mobima
Erstellt:   2021

Überarbeitet für Simulation mit konzentrierten Parametern 2025 Keller

Mit diesem Skript werden Parameter geladen, welche dann in ein MKS/Hydraulik-Modell
uebernommen werden.

%}

%% Limit Parameter
parameter.Hubzylinder.Offset = 0.450; % in m
parameter.Auslegerzylinder.Offset = 0.200; % in m
parameter.Stielzylinder.Offset = 0.400; % in m
parameter.Loeffelzylinder.Offset = 0.300; % in m


%% Schwereeigenschaftenc

%Oberwagen
parameter.Oberwagen.Masse = 7707; % in kg
parameter.Oberwagen.Dichte = 2797; % in kg/m^3
parameter.Oberwagen.Schwerpunkt = [-0.686, 0.048, 0.45]; % in m 
parameter.Oberwagen.Traegheitsmoment = [1634.1204,7714.4591, 6207.1976]; % in kg*m^2 
parameter.Oberwagen.Deviationsmoment =  [0.000, 0.000, 0.000]; % in kg*m^2

%Unterwagen
parameter.Unterwagen.Masse = 4866; % in kg 
parameter.Unterwagen.Dichte = 2797; % in kg/m^3
parameter.Unterwagen.Schwerpunkt = [-0.0917, 0.000, -0.4192]; % in m 
parameter.Unterwagen.Traegheitsmoment = [1809.1296, 2595.578, 2555.9204]; % in kg*m^2 
parameter.Unterwagen.Deviationsmoment =  [0.000, 0.000, 0.000]; % in kg*m^2

%Hauptarm 
parameter.Masse.Hauptarm = 668; % in kg 
parameter.Dichte.Hauptarm = 2797; % in kg/m^3
parameter.Schwerpunkt.Hauptarm = [1.113, 0.000, -0.071]; % in m 
parameter.Traegheitsmoment.Hauptarm = [3.4682, 855.7413, 852.2731]; % in kg*m^2 
parameter.Deviationsmoment.Hauptarm = [0.000, 171.433, 0.000]; % in kg*m^2

%Verstellausleger 
parameter.Masse.Verstellausleger = 552; % in kg 
parameter.Dichte.Verstellausleger = 2797; % in kg/m^3
parameter.Schwerpunkt.Verstellausleger = [1.418, 0.000, -0.019]; % in m 
parameter.Traegheitsmoment.Verstellausleger = [0.1993, 1110.1189, 1109.9196]; % in kg*m^2 
parameter.Deviationsmoment.Verstellausleger = [0.000, 171.433, 0.000]; % in kg*m^2

%Hubzylinderrohr
parameter.Masse.Hubzylinderrohr = 100; % in kg
parameter.Dichte.Hubzylinderrohr = 4161; % in kg/m^3
parameter.Schwerpunkt.Hubzylinderrohr = [0.000, -0.401, 0.000]; % in m
parameter.Traegheitsmoment.Hubzylinderrohr = [19.341, 0.735, 19.333]; % in kg*m^2
parameter.Deviationsmoment.Hubzylinderrohr = [0.000, 0.000, 0.000]; % in kg*m^2

%Hubzylinderstange
parameter.Masse.Hubzylinderstange = 100; % in kg
parameter.Dichte.Hubzylinderstange = 6227; % in kg/m^3
parameter.Schwerpunkt.Hubzylinderstange = [0.000, 0.862, 0.000]; % in m
parameter.Traegheitsmoment.Hubzylinderstange = [21.254, 0.400, 21.241]; % in kg*m^2
parameter.Deviationsmoment.Hubzylinderstange = [0.000, 0.000, 0.000]; % in kg*m^2

%Verstellzylinderstange
parameter.Masse.Verstellzylinderstange = 100; % in kg
parameter.Dichte.Verstellzylinderstange = 6227; % in kg/m^3
parameter.Schwerpunkt.Verstellzylinderstange = [0.000, 0.862, 0.000]; % in m
parameter.Traegheitsmoment.Verstellzylinderstange = [21.254, 0.400, 21.241]; % in kg*m^2
parameter.Deviationsmoment.Verstellzylinderstange = [0.000, 0.000, 0.000]; % in kg*m^2

%Verstellzylinderrohr
parameter.Masse.Verstellzylinderrohr = 100; % in kg
parameter.Dichte.Verstellzylinderrohr = 4161; % in kg/m^3
parameter.Schwerpunkt.Verstellzylinderrohr = [0.000, -0.401, 0.000]; % in m
parameter.Traegheitsmoment.Verstellzylinderrohr = [19.341, 0.735, 19.333]; % in kg*m^2
parameter.Deviationsmoment.Verstellzylinderrohr = [0.000, 0.000, 0.000]; % in kg*m^2

%Stiel
parameter.Masse.Stiel = 406; % in kg 
parameter.Dichte.Stiel = 2336; % in kg/m^3
parameter.Schwerpunkt.Stiel = [0.794, 0.000, 0.099]; % in m 
parameter.Traegheitsmoment.Stiel = [3.9792, 259.9362, 255.957]; % in kg*m^2 
parameter.Deviationsmoment.Stiel = [0.000, 76.960, 0.000]; % in kg*m^2

%Stielzylinderrohr
parameter.Masse.Stielzylinderrohr = 100; % in kg
parameter.Dichte.Stielzylinderrohr = 4062; % in kg/m^3
parameter.Schwerpunkt.Stielzylinderrohr = [0.000, -0.319, 0.000]; % in m % 
% parameter.Schwerpunkt.Stielzylinderrohr = [0.000, -0.319, 0.000]; % in m % Creo
parameter.Traegheitsmoment.Stielzylinderrohr = [27.015, 0.736, 27.007]; % in kg*m^2
parameter.Deviationsmoment.Stielzylinderrohr = [0.000, 0.000, 0.000]; % in kg*m^2

%Stielzylinderstange
parameter.Masse.Stielzylinderstange = 100; % in kg
parameter.Dichte.Stielzylinderstange = 3991; % in kg/m^3
parameter.Schwerpunkt.Stielzylinderstange = [0.000, 0.860, 0.000]; % in m
parameter.Traegheitsmoment.Stielzylinderstange = [23.936, 0.363, 23.928]; % in kg*m^2
parameter.Deviationsmoment.Stielzylinderstange = [0.000, 0.000, 0.000]; % in kg*m^2

%Loeffel
parameter.Masse.Loeffel = 313; % in kg 
parameter.Dichte.Loeffel = 6006 ; % in kg/m^3
parameter.Schwerpunkt.Loeffel = [0.5125, 0.000, 0.2916]; % in m 
parameter.Traegheitsmoment.Loeffel = [26.6237, 108.8223, 82.1986]; % in kg*m^2 
parameter.Deviationsmoment.Loeffel = [0.000, -20.427, 0.000]; % in kg*m^2

%Loeffelzylinderrohr
parameter.Masse.Loeffelzylinderrohr = 50; % in kg
parameter.Dichte.Loeffelzylinderrohr = 4161; % in kg/m^3
parameter.Schwerpunkt.Loeffelzylinderrohr = [0.000, -0.401, 0.000]; % in m
parameter.Traegheitsmoment.Loeffelzylinderrohr = [19.341, 0.735, 19.333]; % in kg*m^2
parameter.Deviationsmoment.Loeffelzylinderrohr = [0.000, 0.000, 0.000]; % in kg*m^2

%Loeffelzylinderstange
parameter.Masse.Loeffelzylinderstange = 50; % in kg
parameter.Dichte.Loeffelzylinderstange = 6227; % in kg/m^3
parameter.Schwerpunkt.Loeffelzylinderstange = [0.000, 0.862, 0.000]; % in m
parameter.Traegheitsmoment.Loeffelzylinderstange = [21.254, 0.400, 21.241]; % in kg*m^2
parameter.Deviationsmoment.Loeffelzylinderstange = [0.000, 0.000, 0.000]; % in kg*m^2

%Schwinge 
parameter.Masse.Schwinge = 10; % in kg
parameter.Dichte.Schwinge = 2636; % in kg/m^3
parameter.Schwerpunkt.Schwinge = [0.285, 0.000, 0.051]; % in m
parameter.Traegheitsmoment.Schwinge = [0.026, 0.394, 0.372]; % in kg*m^2
parameter.Deviationsmoment.Schwinge = [0.000, 0.000, 0.000]; % in kg*m^2

%Koppel 
parameter.Masse.Koppel = 43.5; % in kg 
parameter.Dichte.Koppel = 2064; % in kg/m^3
parameter.Schwerpunkt.Koppel = [0.3569, 0.000, 0.000]; % in m 
parameter.Traegheitsmoment.Koppel = [0.000, 6.1992, 6.1992]; % in kg*m^2 
parameter.Deviationsmoment.Koppel = [0.000, 0.001, 0.000]; % in kg*m^2

%Gegengewicht
parameter.Masse.Gegengewicht = 3100; % in kg
parameter.Schwerpunkt.Gegengewicht = [-2.400, 0.000, 0.000]; % in m

%% Anschlagsparameter
%Hubzylinder
parameter.Lowerlimit.Hubzylinder = 600 - parameter.Hubzylinder.Offset*1000 - 50; % in mm
parameter.Upperlimit.Hubzylinder = 1300 - parameter.Hubzylinder.Offset*1000 + 50; % in mm
parameter.Springstiffness.HubzylinderUnten = 1.4e8; % in N/m
parameter.Springstiffness.HubzylinderOben = 2.2e8; % in N/m
parameter.Dampingcoefficient.HubzylinderUnten = 2.4e6; % in N/(m/s)
parameter.Dampingcoefficient.HubzylinderOben = 3.0e6; % in N/(m/s)

%Verstellzylinder
parameter.Lowerlimit.Verstellzylinder = 400 - parameter.Auslegerzylinder.Offset*1000 - 50; % in mm
parameter.Upperlimit.Verstellzylinder = 950 - parameter.Auslegerzylinder.Offset*1000 + 50; % in mm
parameter.Springstiffness.VerstellzylinderUnten = 1.4e8; % in N/m
parameter.Springstiffness.VerstellzylinderOben = 2.2e8; % in N/m
parameter.Dampingcoefficient.VerstellzylinderUnten = 2.4e6; % in N/(m/s)
parameter.Dampingcoefficient.VerstellzylinderOben = 3.0e6; % in N/(m/s)

%Stielzylinder
parameter.Lowerlimit.Stielzylinder = 400 - parameter.Stielzylinder.Offset*1000 - 50; % in mm
parameter.Upperlimit.Stielzylinder = 1450 - parameter.Stielzylinder.Offset*1000 + 50; % in mm
parameter.Springstiffness.StielzylinderUnten = 1.5e8; % in N/m
parameter.Springstiffness.StielzylinderOben = 2.5e8; % in N/m
parameter.Dampingcoefficient.StielzylinderUnten = 2.7e6; % in N/(m/s)
parameter.Dampingcoefficient.StielzylinderOben = 3.5e6; % in N/(m/s)

%Loeffelzylinder
parameter.Lowerlimit.Loeffelzylinder = 300 - parameter.Loeffelzylinder.Offset*1000 - 50; % in mm
parameter.Upperlimit.Loeffelzylinder = 1200 - parameter.Loeffelzylinder.Offset*1000 + 50; % in mm
parameter.Springstiffness.LoeffelzylinderUnten = 1.4e8; % in N/m
parameter.Springstiffness.LoeffelzylinderOben = 2.2e8; % in N/m
parameter.Dampingcoefficient.LoeffelzylinderUnten = 2.4e6; % in N/(m/s)
parameter.Dampingcoefficient.LoeffelzylinderOben = 3.0e6; % in N/(m/s)

%% Geometriedaten
%Hauptarm
parameter.Hauptarm.Kopfpunkt = [431.609, 2462.46, 0]; % in mm [431.609, 2462.46, 0]
parameter.Hauptarm.Anlenkpunkt.Zylinder.naechstes.Element = [423.161, 373.598, 0]; % in mm
parameter.Hauptarm.Anlenkpunkt.Zylinder.Eigenantrieb.links = [977.456, 2049.25, -275]; % in mm
parameter.Hauptarm.Anlenkpunkt.Zylinder.Eigenantrieb.rechts = [977.456, 2049.25, 275]; % in mm

% Verstellausleger
parameter.Verstellausleger.Anlenkpunkt.Zylinder.Eigenantrieb = [-895.687, -327.233, 0]; % in mm
parameter.Verstellausleger.Kopfpunkt= [-4826.95, 472.025, 0]; % in mm
parameter.Verstellausleger.Anlenkpunkt.Zylinder.naechste.Element= [-1586.76, 449.257, 0]; % in mm

%Stiel
parameter.Stiel.Kopfpunkt = [2249.95, 14.8872, 0]; % in mm
parameter.Stiel.Anlenkpunkt.Zylinder.naechstes.Element = [131.757, -422.701, 0]; % in mm
parameter.Stiel.Anlenkpunkt.Zylinder.Eigenantrieb = [-576.965, -189.43, 0]; % in mm
parameter.Stiel.Anlenkpunkt.Schwinge.links = [1910.13, 25.4371, 135]; % in mm
parameter.Stiel.Anlenkpunkt.Schwinge.rechts = [1910.13, 25.4371, -135]; % in mm

%Loeffel
parameter.Loeffel.Kopfpunkt = [1400, 0, 0]; % in mm
parameter.Loeffel.Anlenkpunkt.Koppel = [0, 0, 320.156]; % in mm

%Koppel
parameter.Koppel.Kopfpunkt = [170.019, -553.183, 0]; % in mm
parameter.Koppel.Anlenkpunkt.Schwinge.links = [0, 0, 135]; % in mm
parameter.Koppel.Anlenkpunkt.Schwinge.rechts = [0, 0, -135]; % in mm

%Schwinge
parameter.Schwinge.Kopfpunkt = [-540.478, 275.103, 0]; % in mm

%Oberwagen
parameter.Oberwagen.Kopfpunkt = [520, 0, 600]; % in mm
parameter.Oberwagen.Anlenkpunkt.Zylinder.naechstes.Element.links = [970, 275, 192]; % in mm
parameter.Oberwagen.Anlenkpunkt.Zylinder.naechstes.Element.rechts = [970, -275, 192]; % in mm
parameter.Oberwagen.Drehpunkt = [0, 0, -210]; % in mm

%Unterwagen
parameter.Unterwagen.Drehpunkt = [0, 0, 400]; % in mm
parameter.Unterwagen.Unterseite = [0, 0, -400]; % in mm

%Hubzylinderrohr
parameter.Hubzylinderrohr.Kopfpunkt = [0, 1440, 0]; % in mm (Abstand zwischen Drehpunkt und Rohrboden)

%Hubzylinderstange
parameter.Hubzylinderstange.Kolbenboden = [0, 150, 0]; % in mm (Abstand zwischen Drehpunkt und Kolbenboden)

%Verstellzylinderrohr
parameter.Verstellzylinderrohr.Fusspunkt= [0,150,0]; % in mm

%Verstellzylinderstange
parameter.Verstellzylinderstange.Kolbenboden= [0, 1260, 0]; %in mm

%Stielzylinderrohr
parameter.Stielzylinderrohr.Fusspunkt = [0, 265, 0]; % in mm (Abstand zwischen Drehpunkt und Rohrboden)

%Stielzylinderstange
parameter.Stielzylinderstange.Kolbenboden = [0, 2040, 0]; % in mm (Abstand zwischen Drehpunkt und Kolbenboden)

%Loeffelzylinderrohr
parameter.Loeffelzylinderrohr.Fusspunkt = [0, 150, 0]; % in mm (Abstand zwischen Drehpunkt und Rohrboden)

%Loeffelzylinderstange
parameter.Loeffelzylinderstange.Kolbenboden = [0, 1230, 0]; % in mm (Abstand zwischen Drehpunkt und Kolbenboden)

%% Internal Mechanics
Cr = 10; %10
Dr = 300; %300
RevJoint_Stiffness = Cr;
RevJoint_Damping = Dr;
RevJoint_Stiffness_OberwagenHauptarm = Cr;
RevJoint_Damping_OberwagenHauptarm = Dr;
RevJoint_Stiffness_HauptarmAusleger = Cr;
RevJoint_Damping_HauptarmAusleger = Dr;
RevJoint_Stiffness_AuslegerStiel = Cr;
RevJoint_Damping_AuslegerStiel = Dr;
RevJoint_Stiffness_AuslegerLoeffel = Cr;
RevJoint_Damping_AuslegerLoeffel = Dr;

Cs = 0;
Ds = 300; %20000
Schubgelenk_Stiffness_Hubzylinder = Cs;
Schubgelenk_Damping_Hubzylinder = Ds;
Schubgelenk_Stiffness_Auslegerzylinder = Cs;
Schubgelenk_Damping_Auslegerzylinder = Ds;
Schubgelenk_Stiffness_Stielzylinder = Cs;
Schubgelenk_Damping_Stielzylinder = Ds;
Schubgelenk_Stiffness_Loeffelzylinder = Cs;
Schubgelenk_Damping_Loeffelzylinder = Ds;

%% Internal Mechanics
parameter.Internal_Mechanics.Cr = 0; %10
parameter.Internal_Mechanics.Dr = 100; %100
parameter.Internal_Mechanics.RevJoint_Stiffness = parameter.Internal_Mechanics.Cr;
parameter.Internal_Mechanics.RevJoint_Damping = parameter.Internal_Mechanics.Dr;
parameter.Internal_Mechanics.RevJoint_Stiffness_OberwagenHauptarm = parameter.Internal_Mechanics.Cr;
parameter.Internal_Mechanics.RevJoint_Damping_OberwagenHauptarm = parameter.Internal_Mechanics.Dr;
parameter.Internal_Mechanics.RevJoint_Stiffness_HauptarmAusleger = parameter.Internal_Mechanics.Cr;
parameter.Internal_Mechanics.RevJoint_Damping_HauptarmAusleger = parameter.Internal_Mechanics.Dr;
parameter.Internal_Mechanics.RevJoint_Stiffness_AuslegerStiel = parameter.Internal_Mechanics.Cr;
parameter.Internal_Mechanics.RevJoint_Damping_AuslegerStiel = parameter.Internal_Mechanics.Dr;
parameter.Internal_Mechanics.RevJoint_Stiffness_AuslegerLoeffel = parameter.Internal_Mechanics.Cr;
parameter.Internal_Mechanics.RevJoint_Damping_AuslegerLoeffel = parameter.Internal_Mechanics.Dr;

parameter.Internal_Mechanics.Cs = 0; %0
parameter.Internal_Mechanics.Ds = 100; %100
parameter.Internal_Mechanics.Schubgelenk_Stiffness_Hubzylinder = parameter.Internal_Mechanics.Cs;
parameter.Internal_Mechanics.Schubgelenk_Damping_Hubzylinder = parameter.Internal_Mechanics.Ds;
parameter.Internal_Mechanics.Schubgelenk_Stiffness_Auslegerzylinder = parameter.Internal_Mechanics.Cs;
parameter.Internal_Mechanics.Schubgelenk_Damping_Auslegerzylinder = parameter.Internal_Mechanics.Ds;
parameter.Internal_Mechanics.Schubgelenk_Stiffness_Stielzylinder = parameter.Internal_Mechanics.Cs;
parameter.Internal_Mechanics.Schubgelenk_Damping_Stielzylinder = parameter.Internal_Mechanics.Ds;
parameter.Internal_Mechanics.Schubgelenk_Stiffness_Loeffelzylinder = parameter.Internal_Mechanics.Cs;
parameter.Internal_Mechanics.Schubgelenk_Damping_Loeffelzylinder = parameter.Internal_Mechanics.Ds;

%% Hydraulikkomponenten

% Hubzylinder
parameter.Hubzylinder.PistonAreaA = 9162; % in mm^2 (berechnet)
parameter.Hubzylinder.PistonAreaB = 5313; % in mm^2 (berechnet)
parameter.Hubzylinder.PistonStroke = parameter.Upperlimit.Hubzylinder; % in mm (input)
parameter.Hubzylinder.PistonDeadVolumeA = 100; % in mm^3
parameter.Hubzylinder.PistonDeadVolumeB = 100; % in mm^3
parameter.Hubzylinder.InitialDistance = 0.7; %
parameter.Hubzylinder.InitialPressureA = 111; % in bar (input)
parameter.Hubzylinder.InitialPressureB = 48; % in bar (input)
parameter.Hubzylinder.BreakawayFrictionForce = 1; % in N
parameter.Hubzylinder.BreakawayFrictionVelocity = 0.060623; % in m/s
parameter.Hubzylinder.CoulombFrictionForce = 1; % in N
parameter.Hubzylinder.ViscousFrictionCoefficient = 1; % in N/(m/s)

% Auslgerzylinder
parameter.Auslegerzylinder.PistonAreaA = 15572; % in mm^2 (berechnet)
parameter.Auslegerzylinder.PistonAreaB = 10545; % in mm^2 (berechnet)
parameter.Auslegerzylinder.PistonStroke = parameter.Upperlimit.Verstellzylinder; % in mm (input) 
parameter.Auslegerzylinder.PistonDeadVolumeA = 100; % in mm^3
parameter.Auslegerzylinder.PistonDeadVolumeB = 100; % in mm^3
parameter.Auslegerzylinder.InitialDistance = 0.74; %(Bagger_90Grad.Wege.Ausleger(1)-parameter.Auslegerzylinder.Offset); % in m
parameter.Auslegerzylinder.InitialPressureA = 6; % in bar (input)
parameter.Auslegerzylinder.InitialPressureB = 6; % in bar (input)
parameter.Auslegerzylinder.BreakawayFrictionForce = 10000; % in N
parameter.Auslegerzylinder.BreakawayFrictionVelocity = 0.060623; % in m/s
parameter.Auslegerzylinder.CoulombFrictionForce = 10000; % in N
parameter.Auslegerzylinder.ViscousFrictionCoefficient = 10000; % in N/(m/s)

% Stielzylinder
parameter.Stielzylinder.PistonAreaA = 9811; % in mm^2 (berechnet)
parameter.Stielzylinder.PistonAreaB = 5393; % in mm^2 (berechnet)
parameter.Stielzylinder.PistonStroke = parameter.Upperlimit.Stielzylinder; % in mm (input)
parameter.Stielzylinder.PistonDeadVolumeA = 100; % in mm^3
parameter.Stielzylinder.PistonDeadVolumeB = 100; % in mm^3
parameter.Stielzylinder.InitialDistance = 0.7 ; %Bagger_90Grad.Wege.Stiel(1)-parameter.Stielzylinder.Offset; % in m
parameter.Stielzylinder.InitialPressureA = 13; % in bar (input)
parameter.Stielzylinder.InitialPressureB = 7; % in bar (input)
parameter.Stielzylinder.BreakawayFrictionForce = 10000; % in N
parameter.Stielzylinder.BreakawayFrictionVelocity = 0.060623; % in m/s
parameter.Stielzylinder.CoulombFrictionForce = 10000; % in N
parameter.Stielzylinder.ViscousFrictionCoefficient = 10000; % in N/(m/s)

% Loeffelzylinder
parameter.Loeffelzylinder.PistonAreaA = 6835; % in mm^2 (berechnet)
parameter.Loeffelzylinder.PistonAreaB = 4007; % in mm^2 (berechnet)
parameter.Loeffelzylinder.PistonStroke = parameter.Upperlimit.Loeffelzylinder; % in mm (input)
parameter.Loeffelzylinder.PistonDeadVolumeA = 100; % in mm^3
parameter.Loeffelzylinder.PistonDeadVolumeB = 100; % in mm^3
parameter.Loeffelzylinder.InitialDistance = 0.2213; % in m 
parameter.Loeffelzylinder.InitialPressureA = 21; % in bar (input)
parameter.Loeffelzylinder.InitialPressureB = 30; % in bar (input)
parameter.Loeffelzylinder.BreakawayFrictionForce = 1; % in N
parameter.Loeffelzylinder.BreakawayFrictionVelocity = 0.060623; % in m/s
parameter.Loeffelzylinder.CoulombFrictionForce = 1; % in N
parameter.Loeffelzylinder.ViscousFrictionCoefficient = 10; % in N/(m/s)

% Steuerventile
parameter.Steuerventile.Hubzylinder.MaximumOpening = 5; % in mm
parameter.Steuerventile.Hubzylinder.MaximumOpeningArea = 200; % in mm^2 0.4*200
parameter.Steuerventile.Auslegerzylinder.MaximumOpening = 5; % in mm
parameter.Steuerventile.Auslegerzylinder.MaximumOpeningArea = 200; % in mm^2 0.5*200
parameter.Steuerventile.Stielzylinder.MaximumOpening = 5; % in mm
parameter.Steuerventile.Stielzylinder.MaximumOpeningArea = 200; % in mm^2 0.3*200
parameter.Steuerventile.Loeffelzylinder.MaximumOpening = 5; % in mm
parameter.Steuerventile.Loeffelzylinder.MaximumOpeningArea = 200; % in mm^2 0.25*200
parameter.Steuerventile.Drehwerk.MaximumOpening = 5; % in mm
parameter.Steuerventile.Drehwerk.MaximumOpeningArea = 25; % 20 in mm^2 0.5*25

% Drehwerk 
parameter.Drehwerk.Displacement = 45.6; % in cm^3/rev
parameter.Drehwerk.NominalShaftAngVel = 188; % in red/s
parameter.Drehwerk.InitialAngle = 270; % in deg
parameter.Drehwerk.InitialPressureA = 21; % in bar (input)
parameter.Drehwerk.InitialPressureB = 30; % in bar (input)
parameter.Drehwerk.pressure_drop_coefficient= 2.5e-06; %0.6e-6; 1.8947e-06 N*m/Pa
parameter.Drehwerk.Nominal_Pressure_Drop = 60; % 100 bar

% % LS-Pumpe 
% parameter.Pumpe.MaxStroke = 0.009; % in m
% parameter.Pumpe.Displacement = 140.2; % in cm^3/rev
% parameter.Pumpe.NominalShaftAngVelocity = 188; % in rad/s
% parameter.Pumpe.NominalPressureGain = 10000000; % in Pa
% parameter.Pumpe.NominalKinematicVelocity = 18; % in cSt
% parameter.Pumpe.FluidDensity = 900; % in kg/m^3
% parameter.Pumpe.TotalEfficiency = 0.80;
% parameter.Pumpe.VolumetricEfficiency = 0.92;
% parameter.Pumpe.NoLoadTorque = 0; % in Nm
% 
% % DBV (vorläufig)
% parameter.DBV.MaximumArea = 0.002; % in m^2
% parameter.DBV.ValvePressureSetting = 27579000; % in Pa
% parameter.DBV.ValveRegulationRange = 2757900; % in Pa
% parameter.DBV.FlowDischargeCoefficient = 0.7;
% parameter.DBV.LeckageArea = 1*10^(-9); % in m^2
% parameter.DBV.CriticalReynoldsNumber = 12;

