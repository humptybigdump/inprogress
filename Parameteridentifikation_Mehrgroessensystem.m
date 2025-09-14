close all
clear all

%% Parameter zur Steuerung der Simulation
Rauschen = 0;                           % 1 für Rauschen, 0 ohne Rauschen
Eingangssignal = 1;                     % 1 = Sprung
                                        % 2 = Sinus
                                        % 3 = PRBS
                                        
%% Globale Variablen
global u1 u2 y1 y2 t
global K11 T11 K22 T22 K12 K21

%% Parameterdefinition der Strecke
K11 = 4;
T11 = 25;
K22 = 0.25;
T22 = 20;
K12 = 0.1;
K21 = 2;

%% Ergebnistabelle initialisieren
Ergebnis = table;
Ergebnis.Parameter = {'K11'; 'T11'; 'K12'; 'K22'; 'T22'; 'K21'};
Ergebnis.Originale_Werte = [K11; T11; K12; K22; T22; K21];

%% Signale definieren
T_A = 0.1;                                      % Abtastzeit in Sekunden
t = (0:T_A:1000)';                              % Vorgabe der Messzeitpunkte für Simulation
if Eingangssignal == 1
    u = [zeros(100,1); ones(size(t,1)-100,1)];  % Eingangssprung (Achtung für Identifikation ist Sprungantwort nicht ideal, wegen persistent excitation!)
elseif Eingangssignal == 2
    u = sin(0.1*t);
elseif Eingangssignal == 3
    u = frest.PRBS('Order',20,'NumPeriods',1,'Amplitude',2,'Ts',T_A);
    u = generateTimeseries(u);
    u = u.Data;
    u = u(1:length(t));
end

u1 = [t, u];
u2 = u1;

%% Simulation der Ausgänge y1 und y2 (Eigentlich Messwerte aber hier aus Simulink)
simOut = sim('Parameteridentifikation_Mehrgroessensystem_V_kanonisch','StartTime','0','StopTime','1000','FixedStep','0.1','SimulationMode','normal','AbsTol','1e-5',...
            'SaveOutput','on','OutputSaveName','yout','SaveFormat','Dataset');
outputs = simOut.get('yout');
y1 = (outputs{1}.Values); 
y1 = y1.Data;
y2 = (outputs{2}.Values); 
y2 = y2.Data;

% Messrauschen
if Rauschen == 1
    y1 = y1 + 0.1*randn(size(t,1),1);   
    y2 = y2 + 0.1*randn(size(t,1),1); 
end

figure
plot(t,y1); hold on;
plot(t,y2);
title('Ausgangsgrößen y1 und y2')
xlabel('Time'); legend('y1','y2')


%% Gleichungsfehlerbasierte Parameteridentifikation

% Zustandsvariablenfilter (ZVF) initialisieren:
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
% Problem hier, Anfangswert des Systems muss bekannt sein, wenn Experiment nicht aus Ruhelage, dann Fehler 
y1_f = lsim(ZVFdy,y1,t,[0; 0]);
y2_f = lsim(ZVFdy,y2,t,[0; 0]);
u1_f = lsim(ZVFdu,u,t,[0; 0]);
u2_f = lsim(ZVFdu,u,t,[0; 0]); % beide Eingänge bekommen hier im Beispiel das gleiche Signal


% LS für y1
y_N = y1_f(:,2);                            % Messvektor 
S_N = [-y1_f(:,1) u1_f(:,1) y2_f(:,1)];     % Datenmatrix
theta = pinv(S_N)*y_N;                      % Least-Squares-Lösung  

T11_est = 1/theta(1);                       % Geschätzte Strecken-Zeitkonstante T11
K11_est = theta(2)*T11_est;                 % Geschätzte Strecken-Verstärkung K11
K12_est = theta(3)*T11_est/K11_est;         % Geschätzte Verstärkung K12

% LS für y2
y_N = y2_f(:,2);                            % Messvektor 
S_N = [-y2_f(:,1) u2_f(:,1) y1_f(:,1)];     % Datenmatrix
theta = pinv(S_N)*y_N;                      % Least-Squares-Lösung  

T22_est = 1/theta(1);                       % Geschätzte Strecken-Zeitkonstante T11
K22_est = theta(2)*T22_est;                 % Geschätzte Strecken-Verstärkung K11
K21_est = theta(3)*T22_est/K22_est;         % Geschätzte Verstärkung K12


% Ergebnisse
Ergebnis = table;
Ergebnis.Parameter = {'K11'; 'T11'; 'K12'; 'K22'; 'T22'; 'K21'};
Ergebnis.Originale_Werte = [K11; T11; K12; K22; T22; K21];
Ergebnis.GF = [K11_est; T11_est; K12_est; K22_est; T22_est; K21_est];

%% Ausgangssfehlerbasierte Parameteridentifikation

theta_0 = [4, 25, 0.25, 20, 0.1, 2];
%theta_0 = [3, 24, 0.3, 21, 0.3, 2.4]; % [K11, T11, K22, T22, K12, K21] Startwert für Optimierung muss ungefähr stimmen, sonst lokales Minimum

% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich unter Annahme Anfangswert x_0 = 0
disp('Starte Optimierung. Das kann dauern. Suche in 6-dimensionalem Raum. Evtl. Kaffeekochen/-trinken :-)');
theta_opt = fminsearch(@V_kanonisch_Model_Error, theta_0);
Ergebnis.AF = [theta_opt(1); theta_opt(2); theta_opt(5); theta_opt(3);...
                                    theta_opt(4); theta_opt(6)];
Ergebnis