clear all, clc
disp('-------------------------------------------------------------------------------------- ')
disp('                               RECHNERGESTÜTZTE DYNAMIK')
disp('                             Prof.Dr.-Ing. Carsten Proppe')
disp('-------------------------------------------------------------------------------------- ')
disp('                                 INHALT DES PROGRAMMS:')
disp('             1. Finite-Elemente-Approximation vs analytische Berechnung')
disp('             2. Modale Analyse (Modale Berechnung) für 2-3-4 Freiheitsgrade')
disp('             3. Ritzsches Verfahren')
disp('             4. Modellreduktion für die Struktur')
disp('             5. Finite-Elemente in die Rotordynamik')
disp('-------------------------------------------------------------------------------------- ')
disp(' ')
%-----------------------------------------------------------------------------------

%-----------------------------------------------------------------------------------
n1=input(['Ihr Auswahl?  [1/2/3/4/5]  >>  ']);
n =round(n1);
if n1 > 5 | n1 < 1
    disp('     Geben Sie bitte die Anzahl 1,2,3,4 oder 5 !!')
    n1 = input('Ihr Auswahl?  [1/2/3/4/5]  >>  ');
    if n1 > 5 | n1 < 1
        disp('Sie haben schon zweimal Fehler gemacht. Versuchen Sie nochmal von Anfang an!')
        return
    end
end

if n == 1;
    run PROGRAMM1
elseif n == 2;
    run PROGRAMM2
elseif n == 3;
    run PROGRAMM3
else
    disp('Leider! 4. Modellreduktion und 5. FE in Rotordynamik noch in Bearbeitung')
    return
end
disp(' ')
