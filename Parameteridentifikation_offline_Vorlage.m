%% Vorlage fuer Parameteridentifikation im Offline-Betrieb
close all;
clear all;
%% Variabelen zur Steuerung 
% Parameter zum veraendern: Hier koennen Sie Rauschen, Eingangssignal, Zeitkonstante des ZVF und Anfangswerte einstellen.
% Probieren Sie verschiedene Varianten aus!

Rauschen = 0;                           % 1 fuer Rauschen, 0 ohne Rauschen
Eingangssignal = 1;                     % 1 = Sprung
                                        % 2 = Sinus
                                        % 3 = PRBS
T_filter = 10;                          % Filterkonstante ZVF

    
%% Messdaten erfassen/simulieren
% In folgendem Skript werden die Messdaten (y und u) fuer die Parameteridentifikation generiert. Versuchen Sie, 
% das Skript in dem die Messwerte generiert werden, zu verstehen. 
% Untersuchen Sie, wie sich Veraenderungen der Parameter auf das Ausgangssignal auswirken.
PT3_Generiere_Messdaten_offline;       

x_0_mess = [y_e + 0.1; 0; 0];           % Anfangswert in folgender Form [0. Ableitung; 1. Ableitung; 2. Ableitung], entspricht Anfangswert x_0 Kleinsignalverhalten = 0.1 

%% Parameteridentifikation allgemein Arbeitspunkt/Ruhelage (Kleinsignalverhalten)!
% 1. Arbeitspunkt/Ruhelage von Eingangs- und Ausgangssignal abziehen

y = 
u = 

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0])

% Zustandsvariablenfilter (ZVF) initialisieren: Achten Sie auf die Dimension des Zustandsvariablenfilters
% fuer eine PT3-Strecke.
% A,b,C und d muessen von Ihnen implementiert werden

ZVF = ss(A,b,C,d);         

% Zeitdiskrete Realisierung des ZVF fuer Eingang. 
% Achten Sie auf die korrekte Wahl des Halteglieds in Abhaenigkeit des Eingangssignals (glatt oder stueckweise kosntant?)
ZVFdu = 

% Zeitdiskrete Realisierung des ZVF fuer Ausgang
ZVFdy = 

% ZVF anwenden: Simulieren sie das gefilterte Eingangs- und Ausgangssignal mit dem ZVF, 
% dem ursprueunglichen Eingangs- bzw. Ausgangssignal und den geschaetzen Anfangswerten.
% Problem: Anfangswert des Systems muss bekannt sein, wenn Experiment nicht aus Ruhelage startet gibt es Fehler 
y_f = 
u_f = 

% Gefilterte Signale fuer Least-Squares nutzen: Erstellen Sie den Messvektor, die Datenmatrix und berechnen Sie
% die Parameter
y_N =                                                       % Messvektor 
S_N =                                                       % Datenmatrix
theta =                                                     % Least-Squares-Loesung  

% Rechnen Sie die Parameter des Least-Squares in die Parameter der Strecke um:
disp('Gleichungsfehlerbasierte Least-Squares zeitkontinuierlich ohne Anfangswertschaetzung:')
T3_est =                                % Geschaetzte Strecken-Zeitkonstante T3
T2_est =                                % Geschaetzte Strecken-Zeitkonstante T2
T1_est =                                % Geschaetzte Strecken-Zeitkonstante T1
K_est =                                 % Geschaetzte Verstaerkung K


%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 OHNE Anfangswertschaetzung 


% Fuer Schaetzung Anfangswert y_0 mit Zustandsvariablenfilter simulieren:
eins_f = 

% Gefilterete Signale fuer Least-Squares nutzen mit Beruecksichtigung des Anfangswertes
y_N =                                               % Messvektor 
S_N =                                               % Datenmatrix
theta =                                             % Least-Squares-Loesung  

% Rechnen Sie die Parameter des Least-Squares in die Parameter der Strecke um:
% (Vergessen Sie die Anfangswerte nicht!)
disp('Gleichungsfehlerbasierte Least-Squares zeitkontinuierlich mit Anfangswertschaetzung:')
T3_est =                                % Geschaetzte Strecken-Zeitkonstante T3
T2_est =                                % Geschaetzte Strecken-Zeitkonstante T2
T1_est =                                % Geschaetzte Strecken-Zeitkonstante T1
K_est =                                 % Geschaetzte Verstaerkung K
y_0_est =                               % Geschaetzter Anfangswert y
dy_0_est =                              % Geschaetzter Anfangswert dy
ddy_0_est =                             % Geschaetzter Anfangswert ddy


 

%% Parameteridentifikation ueber Ausgangsfehlerminimierung
% Implementieren Sie eine separate Funktion (siehe Vorlage "PT3_Model_Error.m und "PT3_Model_Error_x0"), die zu
% einem gegebenen Parametersatz theta den Fehler zwischen dem Modell und der Messung zurueckliefert. Minimieren 
% Sie dann den Fehler um ein optimalen Parametersatz zu bekommen (Stickwort "fminsearch").

%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0])
theta_0 =               % Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum

disp('Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich unter Annahme Anfangswert x_0 = 0:')
theta_opt = 

%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich MIT Anfangswertschaetzung (Annahme x_0 = [y_0;0;0])
% Geben Sie nun auch eine Anfangsschaetzung des Anfangswertes in dem Parametersatz an, 
% um diesen auch mitschaetzen zu lassen
theta_0 =              
disp('Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich mit Schaetzung des Anfangswerts:')
theta_opt_x0 = 
  

%% Weitere Untersuchungen
% Fuehren Sie die obigen Untersuchungen auch fuer die anderen Modellansaetze durch, die in der Aufgabenstellung aufgelistet sind.
% Achten Sie dabei auf die Wahl des richtigen ZVF in Abhaengigkeit des Grades des Modellansatzes. Sie koennen den obigen Code
% einfach fuer jeden Aufgabenteil kopieren und weiter unten einfuegen und jeweils fuer den verwendeten Modellansatz veraendern.
% Fuer die Ausgangsfehlerbasierte Parameteridentifikation muss je nach Modellansatz eine eigene Funktion zur Optimierung erstellt
% werden. Dabei koennen Sie sich an der Vorlage fuer die PT3 Strecke orientieren und das ganze analog fuer eine PT4 oder PT2
% Strecke erstellen.

