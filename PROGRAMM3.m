%PROGRAMM3.m
clear all, clc
disp('---------------------------------------------------------------------------------- ')
disp('                                RITZSCHES VERFAHREN ')
disp('                Rechnergestützte Dynamik - Prof.Dr.-Ing. C. Proppe')
disp('---------------------------------------------------------------------------------- ')
disp('Eingang: Länge L, Dicke b, Höhe h des Balken - Elastizitätsmodul E, Dichte rho')
disp('Ausgang: 1.,2.,3.-Eigenform, Animation der Eigenform')
disp(' ')
%-----------------------------------------------------------------------------------
l=input(['Länge des Balken [m]  >>  ']);
if l < 0
    disp('    Geben Sie bitte die Länge positiv !!')
    l = input('Länge des Balken [m] >>  ');
    if l < 0
        disp('Sie haben schon zweimal Fehler gemacht. Versuchen Sie nochmal von Anfang an!')
        return
    end
end
%-----------------------------------------------------------------------------------
b1=input(['Dicke des Balken [cm] >>  ']);
if b1 < 0
    disp('    Geben Sie bitte die Dicke positiv !!')
    b1 = input('Dicke des Balken [m] >>  ');
    if b1 < 0
        disp('Sie haben schon zweimal Fehler gemacht. Versuchen Sie nochmal von Anfang an!')
        return
    end
end
%-----------------------------------------------------------------------------------
h1=input(['Höhe des Balken  [cm] >>  ']);
if h1 < 0
    disp('    Geben Sie bitte die Dicke positiv  !!')
    h1 = input('Höhe des Balken  [m] >>  ');
    if h1 < 0
        disp('Sie haben schon zweimal Fehler gemacht. Versuchen Sie nochmal von Anfang an!')
        return
    end
end
%-----------------------------------------------------------------------------------
disp(' ')
rho=input(['Dichte des Materials [kg/m^3] >>  ']);
if rho < 0
    disp('    Geben Sie bitte die Dichte positiv  !!')
    rho = input('Dichte des Materials [kg/m^3] >>  ');
    if rho < 0
        disp('Sie haben schon zweimal Fehler gemacht. Versuchen Sie nochmal von Anfang an!')
        return
    end
end
%-----------------------------------------------------------------------------------
E1=input(['Elastizitätsmodul    [GPa]    >>  ']);
if E1 < 0
    disp('     Geben Sie bitte die Elastizitätsmodul positiv  !!')
    E1 = input('Elastizitätsmodul [GPa]       >>  ');
    if E1 < 0
        disp('Sie haben schon zweimal Fehler gemacht. Versuchen Sie nochmal von Anfang an!')
        return
    end
end
%-----------------------------------------------------------------------------------

disp('---------------------------------------------------------------------------------- ')
disp('                     Wählen Sie einen folgenden Lager aus');
disp('---------------------------------------------------------------------------------- ')
disp('1. Beidseitig gelenkig gelagerter Balken      ');
disp('2. Einseitig eingespannter Balken             ');
disp('---------------------------------------------------------------------------------- ')
Auswahl = input(['Ihr Wahl [1 oder 2]? >> ']);
disp(' '), disp(' ') 

E = E1*1e9;     % Umrechnen von [GPa] zu [N/m^2]
b = b1*1e-2;    % Umrechnen von [cm] zu [m]
h = h1*1e-2;    % Umrechnen von [cm] zu [m]
I0=h*h*h*b/12;  % Flächenträgsheitsmoment [m^4]
mu0=rho*b*h;    % Massenbelegung [kg/m]

if Auswahl == 1
run Ritz_Beidseitig
elseif Auswahl == 2
    run Ritz_Eingespannt
else
    return
end
   