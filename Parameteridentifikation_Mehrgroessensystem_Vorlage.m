clear all

% Parameter zur Steuerung der Simulation
Rauschen = 1;                           % 1 für Rauschen, 0 ohne Rauschen
Eingangssignal = 1;                     % 1 = Sprung
                                        % 2 = Sinus
                                        % 3 = PRBS
                                        
% Parameterdefinition der Strecke: Initialisierne Sie die Verstärkungen und Zeitkonstanten des Systems
K11 = 
T11 = 
K22 = 
T22 =
K12 = 
K21 =

% Signale definieren
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

% Simulation der Ausgänge y1 und y2
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

%% LS für die Ausgänge

% Zustandsvariablenfilter (ZVF) initialisieren: Achten Sie auf die Dimension des Zustandsvariablenfilters
% für eine PT3-Strecke.
% A,b,C und d müssen von Ihnen implementiert werden

ZVF = ss(A,b,C,d);

% zeitdiskrete Realisierung des ZVF für Eingang. Achten Sie auf die korrekte Wahl des Halteglieds
ZVFdu = 

% zeitdiskrete Realisierung des ZVF für Ausgang
ZVFdy = 

% ZVF anwenden
% Problem hier, Anfangswert des Systems muss bekannt sein, wenn Experiment nicht aus Ruhelage, dann Fehler 
y1_f = 
y2_f = 
u1_f = 
u2_f = 


% LS für y1
y_N =                                       % Messvektor 
S_N =                                       % Datenmatrix
theta =                                     % Least-Squares-Lösung  

T11_est =                                   % Geschätzte Strecken-Zeitkonstante T11
K11_est =                                   % Geschätzte Strecken-Verstärkung K11
K12_est =                                   % Geschätzte Verstärkung K12

% LS für y2
y_N =                                       % Messvektor 
S_N =                                       % Datenmatrix
theta =                                     % Least-Squares-Lösung  

T22_est =                                   % Geschätzte Strecken-Zeitkonstante T11
K22_est =                                   % Geschätzte Strecken-Verstärkung K11
K21_est =                                   % Geschätzte Verstärkung K12

% Ergebnisse
Ergebnis = table;
Ergebnis.Parameter = {'K11'; 'T11'; 'K12'; 'K22'; 'T22'; 'K21'};
Ergebnis.Originale_Werte = [K11; T11; K12; K22; T22; K21];
Ergebnis.Gleichungsfehlerbasierte_Parameteridentifikation = [K11_est; T11_est; K12_est; K22_est; T22_est; K21_est];


%% Ausgangssfehlerbasierte Parameteridentifikation

theta_0 = [4, 25, 0.25, 20, 0.1, 2];% [K11, T11, K22, T22, K12, K21] Startwert für Optimierung muss ungefähr stimmen, sonst lokales Minimum
%theta_0 = [3, 24, 0.3, 21, 0.3, 2.4]; 

disp('Starte Optimierung. Das kann dauern. Evtl. Kaffeekochen :-)');
theta_opt = ...
Ergebnis.Ausgangsfehlerbasierte_Parameteridentifikation = [theta_opt(1); theta_opt(2); theta_opt(5); theta_opt(3);...
                                    theta_opt(4); theta_opt(6)];
Ergebnis