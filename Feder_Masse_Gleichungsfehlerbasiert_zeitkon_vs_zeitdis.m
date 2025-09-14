close all;
%% Signale simulieren/messen

Feder_Masse_Generiere_Messdaten;

%% Identifikation - Gleichungsfehlerbasiert zeitkontinuierlich mit ZVF 
% Achtung funktioniert nur bei Start aus der Ruhelage, d.h. x_0 = x_e
% i.Allg. größere Schätzfehler durch Rauschen im Vergleich  mit
% ausgangsfehlerbasierter Schätzung

% Zustandsvariablenfilter (ZVF) initialisieren
T_filter = 2;
f_0 = 1/T_filter^3;
f_1 = 3/T_filter^2;
f_2 = 3/T_filter;

A = [0 1 0; 0 0 1; -f_0 -f_1 -f_2];
b = [0; 0; f_0];
C = eye(3);
d = 0;
ZVF = ss(A,b,C,d);

% Arbeitspunkt (Ruhelage) von den Messsignalen abziehen
y = y_mess-y_e;
u = u_mess-u_e;

% ZVF anwenden 
% Annahme: Erregung aus der Ruhelage --> Anfangswerte des Kleinsignalverhalten = 0
y_f_0 = [0; 0; 0];
u_f_0 = [0; 0; 0];
y_f = lsim(ZVF,y(:,1),t,y_f_0);
u_f = lsim(ZVF,u,t,u_f_0);

% Modellansatz E/A DGL 2.Ordnung
% y_dd = -c/m*y_d -k/m*y + 1/m*u 

% ZVF-gefilteret Signale für Least-Squares nutzen
y_N = y_f(:,3);         %Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) u_f(:,1)];    %Datenmatrix

theta = pinv(S_N)*y_N;    %Least-Squares-Lösung  

k = theta(1)/theta(3)
m = 1/theta(3)
c = theta(2)/theta(3)



%% Identifikation - Gleichungsfehlerbasiert zeitdiskrte (zum Vergleich)
% noch ergänzen
