close all

if ~exist('Eingangssignal','var') || ~exist('Rauschen','var')
    Rauschen = 0;     % 1 fuer Rauschen, 0 ohne Rauschen
    Eingangssignal = 1;                 % 1 = Sprung
                                        % 2 = Sinus
                                        % 3 = PRBS
end

%% Erzeugen der Messwerte (durch Simulation)
% PT3 - Strecke
% T3*d^3y/dt^3 + T2*d^2y/dt^2 + T1*dy/dt + y = K*u

y_e = 20;                      % Arbeitspunkt (Ruhelage)
u_e = 1;                       % Arbeitspunkt (Ruhelage)
x_0_mess = [y_e + 0.1; 0; 0];  % Experiment nicht aus Arbeitspunkt, sondern aus [0.1 0 0] um Arbeitspunkt


global T_A;             % Abtastzeit
global t;               % Zeitvektor
global u;               % Vektor des Eingangssignals (Kleinsignal)
global y;               % Vektor des Ausgangssignals (Kleinsignal)

% Signale erzeugen
T_A = 0.01;             % Abtastzeit in Sekunden
t = (0:T_A:500)';       % Vorgabe der Messzeitpunkte für Simulation
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

% Zustandsraumdarstellung PT3
% Umschreiben der Gleichung für das Zustandsraumsystem:
% d^3y/dt^3 = - (T2 / T3) * d^2y/dt^2  - (T1 / T3) * dy/dt  -  (1 / T3) * y  +  (K / T3) * u

% Festlegung der Parameter
global K;                       % (als global definieren, da später für Variante mit bekanntem K in Fehlerfunktion benötigt)
K = 20;                         % Verstärkung
T1 = 100;                       % Zeitkonstante 1
T2 = 50;                        % Zeitkonstante 2
T3 = 20;                        % Zeitkonstante 3

% Bestimmung des Zustandsraummodells ausgehend von der DGL und den
% Parametern (hier Regelungsnormalform)
A = [0 1 0; 0 0 1; -(1/T3) -(T1/T3) -(T2/T3)];
B = [0 0 K/T3]';
C = [1 0 0];
D = 0;
system = ss(A,B,C,D);

% Anfangswert Großsignalverhalten ist x_0_mess. Wenn x_0_mess = [y_e; 0; 0] dann Erregung aus der Ruhelage

% Anfangswert Kleinsignalverhalten (um die Ruhelage)
x_0 = x_0_mess - [y_e; 0; 0];

% Simulation Kleinsignalverhalten
y = lsim(system, u, t, x_0);

% Großsignalverhalten inklusive Messrauschen berechnen
y_mess = y + y_e;                                       % Arbeitspunkt addieren
if Rauschen == 1
    y_mess = y_mess + 0.1*randn(size(t,1),1);           % Messrauschen
end
u_mess = u + u_e;                                       % Arbeitspunkt addieren

%% Plotten

figure;
subplot(2,1,1);
plot(t,u_mess,'r','LineWidth',2);
xlabel('t');
ylabel('u_{mess}');

subplot(2,1,2);
plot(t,y_mess,'blue','LineWidth',2);
xlabel('t');
ylabel('y_{mess}');

