%HAUPTPROGRAMM.m
clear all, clc
disp('-------------------------------------------------------------------------------------- ')
disp('                                 MODALE BERECHNUNG')
disp('                  Rechnergestützte Dynamik - Prof.Dr.-Ing. C. Proppe')
disp('-------------------------------------------------------------------------------------- ')
disp('Eingang: Masse M, Steifigkeit C, Anfangsbedingung: x1(0)=1, und die Andere sind null')
disp('Ausgang: Eigenfrequenzen, -vektoren, diagonale Massen- und Steifigkeitsmatrix')
disp(' ')
%-----------------------------------------------------------------------------------

%-----------------------------------------------------------------------------------
kmax1=input(['Anzahl der Freiheitsgraden [2/3/4]  >>  ']);
kmax =round(kmax1);
if kmax1 > 4 | kmax1 < 2
    disp('     Geben Sie bitte die Anzahl 2 oder 3 oder 4 und positiv  !!')
    kmax1 = input('Anzahl der Freiheitsgraden [2/3/4]  >>  ');
    if kmax1 > 4 | kmax1 < 2
        disp('Sie haben schon zweimal Fehler gemacht. Versuchen Sie nochmal von Anfang an!')
        return
    end
end

if kmax < 3;
disp('-------------------------------------------------------------------------------------- ')
disp('                               2-FREIHEITSGRADE')
disp('        Massenmatrix M=[m 0;0 m] - Steifigkeitsmatrix C=[2c -c;-c 2c]')
disp('-------------------------------------------------------------------------------------- ')
elseif kmax < 4
disp('-------------------------------------------------------------------------------------- ')
disp('                               3-FREIHEITSGRADE')
disp('           M = [m 0 0;0 m 0;0 0 m]    C = [2c -c 0;-c 2c -c;0 -c 2c]')
disp('-------------------------------------------------------------------------------------- ')
else
disp('-------------------------------------------------------------------------------------- ')
disp('                               4-FREIHEITSGRADE')
disp(' M=[m 0 0 0;0 m 0 0;0 0 m 0;0 0 0 m]    C=[2c -c 0 0;-c 2c -c 0;0 -c 2c -c;0 0 -c 2c]')
disp('-------------------------------------------------------------------------------------- ')   
end


m1=input(['Masse m [kg]          >>  ']);
c1=input(['Steifigkeit c [N/m]   >>  ']);
ts=input(['Simulationszeit t [s] >>  ']);

t  = 0:0.001:ts;           %Simulationszeit
%=========================================================================
% m   : Diagonale Massenmatrix
% c   : Diagonale Steifigkeitsmatrix
% w   : Diagonale Eigenfrequenzen-Matrix
% phi : Modalmatrix (Eigenvektor des Systems)
%
% Generalisierte Koordinaten y(t):  x=phi*y -> y=inv(phi)*x
% Diagonalmatrizen m = phi'*M*phi und  c = phi'*C*phi
% Entkoppelte DGL    :  my'' + cy = 0
% Anfangsbedingungen :  y(0)=inv(phi)*x(0)
% Originalkoordinaten:  x(t) = phi*y(t)

if kmax < 3;
  M  = [m1 0;0 m1];                %Massenmatrix 2x2
  C  = [2*c1 -c1;-c1 2*c1];        %Steifigkeitsmatrix 2x2
  x0 = [1 0; 0 0]';                %Anfangbedingungen [x1(0) x2(0); x1'(0) x2'(0)]
  [m,c,w,phi]= ModaleAnalyse2(M,C,x0,t);
elseif kmax < 4
  M  = [m1 0 0;0 m1 0;0 0 m1];               %Massenmatrix [m 0 0;0 m 0;0 0 m]
  C  = [2*c1 -c1 0;-c1 2*c1 -c1;0 -c1 2*c1]; %Steifigkeitsmatrix [2c -c 0;-c 2c -c;0 -c 2c]
  x0 = [1 0 0; 0 0 0]';                      %Anfangbedingungen [x1(0) x2(0) x3(0); x1'(0) x2'(0) x3'(0)]    
  [m,c,w,phi]= ModaleAnalyse3(M,C,x0,t);
else
  M  = [m1 0 0 0;0 m1 0 0;0 0 m1 0; 0 0 0 m1]; 
  C  = [2*c1 -c1 0 0;-c1 2*c1 -c1 0;0 -c1 2*c1 -c1;0 0 -c1 2*c1]; 
  x0 = [1 0 0 0; 0 0 0 0]';                           
  [m,c,w,phi]= ModaleAnalyse4(M,C,x0,t);
end


format bank
disp('     ------------------------------------------------------')
disp('        EIGENFREQUENZEN     ')
disp('     ------------------------------------------------------')
disp(w )
disp('     ------------------------------------------------------')
disp('        EIGENVEKTOREN        ')
disp('     ------------------------------------------------------')
disp(phi )
disp('     ------------------------------------------------------')
disp('        DIAGONALE MASSENMATRIX m      ')
disp('     ------------------------------------------------------')
disp(m )
disp('     ------------------------------------------------------')
disp('        DIAGONALE STEIFIGKEITSMATRIX c      ')
disp('     ------------------------------------------------------')
disp(c )
disp('     ------------------------------------------------------')
disp('        Lösung x(t)-t finden Sie an Diagramm      ')
format short e

