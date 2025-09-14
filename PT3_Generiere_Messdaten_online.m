close all;


%% Erzeugen der Messwerte (durch Simulation)
% PT3 - Strecke 
% T3*d^3/dt^3 + T2*d^2/dt^2 + T1*dy/dt + y = K*u

y_e = 0;                % Arbeitspunkt
u_e = 0;                % Arbeitspunkt

global T_A;             % Abtastzeit
global t;               % Zeitvektor
global u;               % Vektor des Eingangssignals
global y;               % Vektor des Ausgangssignals


% Signale
T_A = 0.1;                  % Abtastzeit in Sekunden
t = (0:T_A:2000)';          % Zeitvektor
t1 = (0:T_A:500)';          % Zeitabschnitt 1
t2 = (500:T_A:2000)';       % Zeitabschnitt 2


%% Berechnung des Ausngangssignals
% Für die Online-Parameteridentifikation mit exponentiellem Vergessen werden während dem Betrieb ein oder mehrere
% Parameter geändert. Daher wird das Eingangs- und Ausgangssignal aus zwei Teilen zusammengesetzt.
% Zustandsraumdarstellung PT3
% Umschreiben der Gleichung für das Zustandsraumsystem:
% d^3/dt^3 = - (T2 / T3) * d^2/dt^2  - (T1 / T3) * dy/dt  -  (1 / T3) * y  +  (K / T3) * u

% Parameter im 1. Anteil
K(1) = 20;                             % Verstärkung 
T1(1) = 100;                           % Zeitkonstante 1
T2(1) = 50;                            % Zeitkonstante 2
T3(1) = 20;                            % Zeitkonstante 3

% Parameter im 2. Anteil
K(2) = 20;                             % Verstärkung 
T1(2) = 100;                           % Zeitkonstante 1
T2(2) = 30;                            % Zeitkonstante 2 hat sich geändert
T3(2) = 20;                            % Zeitkonstante 3

for i = 1:2
    
    % Bestimmung des Zustandsraummodells ausgehend von der DGL und den Parametern
    A = [0 1 0; 0 0 1; -(1/T3(i)) -(T1(i)/T3(i)) -(T2(i)/T3(i))];
    B = [0 0 K(i)/T3(i)]';
    C = [1 0 0];
    D = 0;
    system = ss(A,B,C,D);

    % Auswahl des Eingangssignals, kann durch Variable "Eingangssignal" verändert werden
    if i == 1
        if Eingangssignal == 1
            u1 = [zeros(100,1); ones(size(t1,1)-100,1)];                            % Sprung
        elseif (Eingangssignal == 2)
            u1 = sin(t1/200);                                                       % Sinus
        elseif Eingangssignal == 3
            u1 = frest.PRBS('Order',20,'NumPeriods',1,'Amplitude',2,'Ts',T_A);      % PRBS
            u1 = generateTimeseries(u1);
            u1 = u1.Data;
            u1 = u1(1:length(t1));
        end
        % Simulation des Ausgangs für den 1. Zeitabschnitt
        [y1, t1, x1] = lsim(system, u1, t1, [0,0,0]');
        % Hier auch Zustand x zurückgeben lassen, da wir ihn als Anfangswert
        % für den zweiten Zeitabschnitt benötigen
        
    elseif i == 2
        if Eingangssignal == 1
            u2 = [ones(100,1); zeros(size(t2,1)-100,1)];                            % Sprung
        elseif (Eingangssignal == 2)
            u2 = sin(t2/200);                                                       % Sinus
        elseif Eingangssignal == 3
            u2 = frest.PRBS('Order',20,'NumPeriods',1,'Amplitude',2,'Ts',T_A);      % PRBS
            u2 = generateTimeseries(u2);
            u2 = u2.Data;
            u2 = u2(1:length(t2));
        end
        % Simulation des Ausgangs für den 2. Zeitabschnitt
        % Als Anfangswert letzten Zustand aus 1. Zeitabschnitt verwenden
        y2 = lsim(system, u2, t2, x1(end,:)'); 
    end 
end
T1_soll_1 = [ones(size(t1,1),1)*T1(1)];
T2_soll_1 = [ones(size(t1,1),1)*T2(1)];
T3_soll_1 = [ones(size(t1,1),1)*T3(1)];
K_soll_1 = [ones(size(t1,1),1)*K(1)];
T1_soll_2 = [ones(size(t2,1),1)*T1(2)];
T2_soll_2 = [ones(size(t2,1),1)*T2(2)];
T3_soll_2 = [ones(size(t2,1),1)*T3(2)];
K_soll_2 = [ones(size(t2,1),1)*K(2)];


%% Plots 

u = [u1; u2(2:length(u2))];                     % Zusammensetzten des Eingangssignals
y = [y1; y2(2:length(y2))];                     % Zusammensetzten des Ausgangssignals
t = [t1; t2(2:length(t2))];                     % Zusammensetzten des Zeitsignals

y_mess = y + y_e;                               % Arbeitspunkt addieren
if Rauschen == 1
    y_mess = y_mess + 0.1*randn(size(t,1),1);   % Messrauschen
end
u_mess = u + u_e;                               % Arbeitspunkt addieren

% Plot für das Eingangssignal
figure;
plot(t,u_mess,'Linewidth',2);
xlabel('t');
ylabel('u');
ylim([-1 2]);
xlim([0 2001]);

% Plot für das Ausgangssignal
figure;
plot(t,y_mess,'Linewidth',2);
xlabel('t');
ylabel('y');

% Sollwerte für die Parameter in Vektorform
T1_soll = [T1_soll_1; T1_soll_2(1:end-1)];
T2_soll = [T2_soll_1; T2_soll_2(1:end-1)];
T3_soll = [T3_soll_1; T3_soll_2(1:end-1)];
K_soll = [K_soll_1; K_soll_2(1:end-1)];

clear T1_soll_1 T1_soll_2 T2_soll_1 T2_soll_2 T3_soll_1 T3_soll_2 K_soll_1 K_soll_2


