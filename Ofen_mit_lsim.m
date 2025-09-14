%% Konstanten definieren

P_AP = 50;       %  %    Heizleistung im Arbeitspunkt
theta_AP = 350;  % °C    Temperatur im Arbeitspunkt
T = 30;          % min   Zeitkonstante 
K = 3;           % K/%   statische Verstärkung

%% Zustandsraummodell für Kleinsignalverhalten aufstellen
A = [-1/T];
b = K/T;
c = 1;
d = 0;
sys = ss(A,b,c,d);

%% Simulation des Kleinsignalverhaltens
t = [0:120]';                   % Simulationszeitpunkte in min 
u = 55*ones(size(t)) - P_AP;    % Eingangssignal (Kleinsignal)
x_0 = 330 - theta_AP;           % Anfangswert (Kleinsignal) 
y = lsim(sys,u,t,x_0);          % Simulation (Kleinsignal)

%% Großsignale berechnen
P = u + P_AP;
theta = y + theta_AP;

%% Plots erstellen
subplot(2,1,1);
plot(t,P);
ylim([40,60]);
xlabel('t in min');
ylabel('Heizleistung in %');

subplot(2,1,2);
plot(t,theta);
xlabel('t in min');
ylabel('Ofenteemperatur in °C');
