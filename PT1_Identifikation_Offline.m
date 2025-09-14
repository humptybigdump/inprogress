%% Messdaten erfassen/simulieren
PT1_Generiere_Messdaten_Zustandsraum; %simulation mit Anfangswert verschiedene Ruhelagen möglich


%% Parameteridentifikation allgemein Arbeitspunkt/Ruhelage (Kleinsignalverhalten)!
%1. Arbeitspunkt/Ruhelage abziehen
y = y_mess - y_e;
u = u_mess - u_e;

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich)  PT1 ohne Anfangswertschätzung
% Modell DGL: dy/dt = - 1/T*y + K/T*u
% theta = [1/T, K/T]

% Zustandsvariablenfilter (ZVF) initialisieren
T_filter = 10;
f_0 = 1/T_filter^2;
f_1 = 2/T_filter;
A = [0 1; -f_0 -f_1];
b = [0; f_0];
C = eye(2);
d = 0;
ZVF = ss(A,b,C,d);

% zeitdiskrete Realisierung des ZVF für Eingang
ZVFdu = c2d(ZVF, T_A, 'zoh'); %'zoh' wegen Annahme, u ist stückweise konstant

% zeitdiskrete Realisierung des ZVF für Ausgang
ZVFdy = c2d(ZVF, T_A, 'foh'); %'foh' wegen Annahme, y ist glatt

% ZVF anwenden
% Problem hier, Anfangswert des Systems muss bekannt, wenn Experiment nicht aus Ruhelage, dann Fehler 
% (Alternativ kann Systemanfangswert mitgeschätzt werden s.u.)
y_f = lsim(ZVFdy,y,t,[0; 0]);
%y_f = lsim(ZVF,y(:,1),t,[0; 0]); %evtl. etwas besser, da akausale
%Signalrekonstruktion durch lsim möglich
u_f = lsim(ZVFdu,u,t,[0; 0]);


% gefilteret Signale für Least-Squares nutzen
y_N = y_f(:,2);                %Messvektor 
S_N = [-y_f(:,1) u_f(:,1)];    %Datenmatrix
theta = pinv(S_N)*y_N;    %Least-Squares-Lösung  

disp('Gleichungsfehlerbasierte Least-Squares zeitkontinuierlich ohne Anfangswertschätzung:')
K_est = theta(2)/theta(1)    %Geschätzte Strecken-Verstärkung
T_est = 1/theta(1)           %Geschätzte Strecken-Zeitkonstante

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich)  PT1 mit Anfangswertschätzung

% für Schätzung Anfangswert y_0
eins_f = lsim(ZVFdu,ones(size(y)),t,[0; 0]);

% gefilteret Signale für Least-Squares nutzen
y_N = y_f(:,2);                %Messvektor 
S_N = [-y_f(:,1) u_f(:,1) eins_f(:,2)];    %Datenmatrix erweitert
theta = pinv(S_N)*y_N;    %Least-Squares-Lösung  

disp('Gleichungsfehlerbasierte Least-Squares zeitkontinuierlich mit Anfangswertschätzung:')
K_est = theta(2)/theta(1)    %Geschätzte Strecken-Verstärkung
T_est = 1/theta(1)           %Geschätzte Strecken-Zeitkonstante
y_0_est = theta(3)           %Geschätzter Anfangswert


 %% Parameteridentifikation LS-Gleichungsfehler (zeit-diskret)
% Modell Differenzengleichung: y[k] = a*y[k-1] + b*u[k-1]
% a = exp(-T_A/T)
% b = (1-a)*K
% theta = [a, b]

y_v = y(2:length(y));
S = [y(1:length(y)-1) u(1:length(y)-1)];

theta = pinv(S)*y_v;    %Least-Squares-Lösung   
a = theta(1);
b = theta(2);

disp('Gleichungsfehlerbasierte Least-Squares zeitdiskret:')
% Physikalische Parameter K,T müssen aus den geschätzten berechnet werden
K_est = b/(1-a)      %Geschätzte Strecken-Verstärkung 
T_est = -T_A/log(a)  %Geschätzte Strecken-Zeitkonstante

% Schätzung bei vorliegen von Messrauschen i.Allg. schlechter als bei
% zeitkontinuierlich

% Schätzung wird schlechter, wenn mit höherer Abtastfrequenz (kleiners T_A)
% gemessen wird

%% Parameteridentifikation über Ausgangsfehlerminimierung
% Strukturell bekannte zeitkontinuierliche Lösung: y = K*(1-exp(-t/T))
% theta = [K, T]
%separate Funktion implementieren, die zu einem gegebenen Parametersatz theta den
%Fehler zwischen Modell und Messung zurückliefert:


%PT1
 theta_0=[5,100]; %Startwert für Optimierung muss ungefähr stimmen, sonst lokales Minimum
 disp('Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich unter Annahme Anfangswert x_0 = 0:')
 theta_opt = fminsearch(@PT1_Model_Error, theta_0)
 
 disp('Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich mit Schätzung des Anfangswerts:')
 theta_opt = fminsearch(@PT1_Model_Error_x0, [theta_0, 5])
  


