close all;
clear all;

%% Variablen zur Steuerung
% Parameter zum verändern:
Rauschen = 0;                           % 1 für Rauschen, 0 ohne Rauschen
Eingangssignal = 3;                     % 1 = Sprung
                                        % 2 = Sinus
                                        % 3 = PRBS
T_filter = 10;                          % Filterkonstante ZVF

% Generierung der Messdaten
PT3_Generiere_Messdaten_online;

%% Leere Vektoren für späteres Plotten definieren
y_zvf_plot = zeros(length(t), 3);
y_zvf_dot_plot = zeros(length(t), 3);
u_zvf_plot = zeros(length(t), 3);
K_est_plot = zeros(length(t), 3);
T1_est_plot = zeros(length(t), 3);
T2_est_plot = zeros(length(t), 3);
T3_est_plot = zeros(length(t), 3);
T4_est_plot = zeros(length(t), 3);
K_est_exp_plot = zeros(length(t), 3);
T1_est_exp_plot = zeros(length(t), 3);
T2_est_exp_plot = zeros(length(t), 3);
T3_est_exp_plot = zeros(length(t), 3);
T4_est_exp_plot = zeros(length(t), 3);


%% Parameteridentifikation allgemein Arbeitspunkt!
% 1. Arbeitspunkt abziehen
y = y_mess - y_e;
u = u_mess - u_e;


%% Parameteridentifikation rekursive MKQ-Gleichungsfehler DGL (zeit-kontinuierlich) für korrekten Modellansatz 3. Ordnung

% Zustandsvariablenfilter (ZVF) initialisieren. Wird hier über eine Funktion "zvf" gemacht.
[ZVFdu, ZVFdy] = zvf(3, T_filter, T_A, Eingangssignal);
[Ad, bd, Cd, dd] = ssdata(ZVFdu);
[Ad2, bd2, Cd2, dd2] = ssdata(ZVFdy);

% Anfangszustände des ZVF für u und y
xy = [0; 0; 0; 0];
xu = [0; 0; 0; 0];

% Startwerte für rekursive LS
P = 100*eye(4);
theta = [1/T3_soll(1); T1_soll(1)/T3_soll(1); T2_soll(1)/T3_soll(1); K_soll(1)/T3_soll(1)];
% Auch wenn mit den exakt richtigen Parametern theta gestartet wird,
% kann sich theta von den exakten Werten zwischenzeitlich entfernen!
% Es sollte aber auch mit falschen Startwerten experimentiert werden.

% Für rekursive LS mit exponentiellem Vergessen
P_exp = 100*eye(4);
q = 0.98;                       % Gedächtnisfaktor 0.9 .. 0.995
theta_exp = [1/T3_soll(1); T1_soll(1)/T3_soll(1); T2_soll(1)/T3_soll(1); K_soll(1)/T3_soll(1)];
% Auch wenn mit den exakt richtigen Parametern theta gestartet wird,
% kann sich theta von den exakten Werten zwischenzeitlich entfernen!
% Es sollte aber auch mit falschen Startwerten experimentiert werden.

% In jedem Zeitschritt j mit dem neu erfassten Wert y(j) den ZVF
% aktualisieren und mit rekursiver least squares Update für Parametervektor
% berechnen
% Achtung: Lösung der rekursiven LS ist nicht identisch mit Lösung direkte
% LS! Evtl. mit Unterschied in den Gütewerten nach fester Anzahl
% Rekursionen


for j=1:length(t)
    
    % ZVF für Eingang u:
    u_zvf = xu(1) + dd * u(j);
    xu = Ad * xu + bd * u(j);
    
    % ZVF für Ausgang y
    y_zvf = Cd2*xy + dd2 * y(j);                        % dd2 ungleich 0 wegen 'first order hold'
    xy = Ad2 * xy + bd2 * y(j);
    
    y_v = y_zvf(4);                                     % Messwert (höchste Anleitung,linke Seite)
    s = [-y_zvf(1); -y_zvf(2); -y_zvf(3); u_zvf(1)];    % Datenvektor
    
    
    % Rekursive Least Squares OHNE Vergessen:
    k = P*s/(1 + s'*P*s);
    P = P - k*s'*P;
    theta = theta + k*(y_v - s'*theta);
    
    T3_est = 1 / theta(1);                          % Geschätzte Strecken-Zeitkonstante T3
    T2_est = theta(3) * T3_est;                     % Geschätzte Strecken-Zeitkonstante T2
    T1_est = theta(2) * T3_est;                     % Geschätzte Strecken-Zeitkonstante T1
    K_est = theta(4) * T3_est;                      % Geschätzte Verstärkung K
    
    
    % Rekursive Least Squares MIT exponentiellem Vergessen:
    k_exp = P_exp*s/(q + s'*P_exp*s);
    P_exp = 1/q*(P_exp - k_exp*s'*P_exp);
    %eig(P_exp);
    theta_exp = theta_exp + k_exp*(y_v - s'*theta_exp);
    
    T3_est_exp = 1 / theta_exp(1);                  % Geschätzte Strecken-Zeitkonstante T3
    T2_est_exp = theta_exp(3) * T3_est_exp;         % Geschätzte Strecken-Zeitkonstante T2
    T1_est_exp = theta_exp(2) * T3_est_exp;         % Geschätzte Strecken-Zeitkonstante T1
    K_est_exp = theta_exp(4) * T3_est_exp;          % Geschätzte Verstärkung K
    
    
    % Werte Merken für Plot
    y_zvf_plot(j,1) = y_zvf(1);
    % y_zvf_dot_plot(j) = y_zvf(2);
    u_zvf_plot(j,1) = u_zvf(1);
    K_est_plot(j,1) = K_est;
    T1_est_plot(j,1) = T1_est;
    T2_est_plot(j,1) = T2_est;
    T3_est_plot(j,1) = T3_est;
    K_est_exp_plot(j,1) = K_est_exp;
    T1_est_exp_plot(j,1) = T1_est_exp;
    T2_est_exp_plot(j,1) = T2_est_exp;
    T3_est_exp_plot(j,1) = T3_est_exp;
    
end

%% Parameteridentifikation rekursive MKQ-Gleichungsfehler DGL (zeit-kontinuierlich) für falschen Modellansatz 2. Ordnung

% Zustandsvariablenfilter (ZVF) initialisieren. Wird hier über eine Funktion "zvf" gemacht.
[ZVFdu, ZVFdy] = zvf(2, T_filter, T_A, Eingangssignal);
[Ad, bd, Cd, dd] = ssdata(ZVFdu);
[Ad2, bd2, Cd2, dd2] = ssdata(ZVFdy);

% Anfangszustände des ZVF für u und y
xy = [0; 0; 0];
xu = [0; 0; 0];

% Startwerte für rekursive LS
P = 100*eye(3);
theta = [1/T2_soll(1); T1_soll(1)/T2_soll(1); K_soll(1)/T2_soll(1)];
% Auch wenn mit den exakt richtigen Parametern theta gestartet wird,
% kann sich theta von den exakten Werten zwischenzeitlich entfernen!

% Für rekursive LS mit exponentiellem Vergessen
P_exp = 100*eye(3);
q = 0.98;                       % Gedächtnisfaktor 0.9 .. 0.995
theta_exp = [1/T2_soll(1); T1_soll(1)/T2_soll(1); K_soll(1)/T2_soll(1)];


% In jedem Zeitschritt j mit dem neu erfassten Wert y(j) den ZVF
% aktualisieren und mit rekursiver least squares Update für Parametervektor
% berechnen
% Achtung: Lösung der rekursiven LS ist nicht identisch mit Lösung direkte
% LS! Evtl. mit Unterschied in den Gütewerten nach fester Anzahl
% Rekursionen

for j=1:length(t)
    
    % ZVF für Eingang u:
    u_zvf = xu(1) + dd * u(j);
    xu = Ad * xu + bd * u(j);
    
    % ZVF für Ausgang y
    y_zvf = Cd2*xy + dd2 * y(j);                        % dd2 <> 0 wegen 'first order hold'
    xy = Ad2 * xy + bd2 * y(j);
    
    y_v = y_zvf(3);                                     % Messwert
    s = [-y_zvf(1); -y_zvf(2); u_zvf(1)];               % Datenvektor
    
    % Rekursive Least Squares OHNE Vergessen:
    k = P*s/(1 + s'*P*s);
    P = P - k*s'*P;
    theta = theta + k*(y_v - s'*theta);
    
    T2_est = 1 / theta(1);                          % Geschätzte Strecken-Zeitkonstante T2
    T1_est = theta(2) * T2_est;                     % Geschätzte Strecken-Zeitkonstante T1
    K_est = theta(3) * T2_est;                      % Geschätzte Verstärkung K
    
    
    % Rekursive Least Squares MIT exponentiellem Vergessen:
    k_exp = P_exp*s/(q + s'*P_exp*s);
    P_exp = 1/q*(P_exp - k_exp*s'*P_exp);
    %eig(P_exp);
    theta_exp = theta_exp + k_exp*(y_v - s'*theta_exp);
    
    T2_est_exp = 1 / theta_exp(1);                  % Geschätzte Strecken-Zeitkonstante T2
    T1_est_exp = theta_exp(2) * T2_est_exp;         % Geschätzte Strecken-Zeitkonstante T1
    K_est_exp = theta_exp(3) * T2_est_exp;          % Geschätzte Verstärkung K
    
    
    
    % Werte Merken für Plot
    y_zvf_plot(j,2) = y_zvf(1);
    % y_zvf_dot_plot(j) = y_zvf(2);
    u_zvf_plot(j,2) = u_zvf(1);
    K_est_plot(j,2) = K_est;
    T1_est_plot(j,2) = T1_est;
    T2_est_plot(j,2) = T2_est;
    T3_est_plot(j,2) = T3_est;
    K_est_exp_plot(j,2) = K_est_exp;
    T1_est_exp_plot(j,2) = T1_est_exp;
    T2_est_exp_plot(j,2) = T2_est_exp;
    T3_est_exp_plot(j,2) = T3_est_exp;
    
end

%% Parameteridentifikation rekursive MKQ-Gleichungsfehler DGL (zeit-kontinuierlich) für falschen Modellansatz 4. Ordnung

% Zustandsvariablenfilter (ZVF) initialisieren. Wird hier über eine Funktion "zvf" gemacht.
[ZVFdu, ZVFdy] = zvf(4, T_filter, T_A, Eingangssignal);
[Ad, bd, Cd, dd] = ssdata(ZVFdu);
[Ad2, bd2, Cd2, dd2] = ssdata(ZVFdy);

% Anfangszustände des ZVF für u und y
xy = [0; 0; 0; 0; 0];
xu = [0; 0; 0; 0; 0];

% Startwerte für rekursive LS
P = 100*eye(5);
theta = [1/T3_soll(1); T1_soll(1)/T3_soll(1); T2_soll(1)/T3_soll(1); 20; K_soll(1)/T3_soll(1)];
% Auch wenn mit den exakt richtigen Parametern theta gestartet wird,
% kann sich theta von den exakten Werten zwischenzeitlich entfernen!

% Für rekursive LS mit exponentiellem Vergessen
P_exp = 100*eye(5);
q = 0.98;                       % Gedächtnisfaktor 0.9 .. 0.995
theta_exp = [1/T3_soll(1); T1_soll(1)/T3_soll(1); T2_soll(1)/T3_soll(1); 20; K_soll(1)/T3_soll(1)];


% In jedem Zeitschritt j mit dem neu erfassten Wert y(j) den ZVF
% aktualisieren und mit rekursiver least squares Update für Parametervektor
% berechnen
% Achtung: Lösung der rekursiven LS ist nicht identisch mit Lösung direkte
% LS! Evtl. mit Unterschied in den Gütewerten nach fester Anzahl
% Rekursionen

for j=1:length(t)
    
    % ZVF für Eingang u:
    u_zvf = xu(1) + dd * u(j);
    xu = Ad * xu + bd * u(j);
    
    % ZVF für Ausgang y
    y_zvf = Cd2*xy + dd2 * y(j);                        % dd2 <> 0 wegen 'first order hold'
    xy = Ad2 * xy + bd2 * y(j);
    
    y_v = y_zvf(5);                                                 % Messwert
    s = [-y_zvf(1); -y_zvf(2); -y_zvf(3); -y_zvf(4); u_zvf(1)];     % Datenvektor
    
    % Rekursive Least Squares OHNE Vergessen:
    k = P*s/(1 + s'*P*s);
    P = P - k*s'*P;
    theta = theta + k*(y_v - s'*theta);
    
    T4_est = 1 / theta(1);                          % Geschätzte Strecken-Zeitkonstante T4
    T3_est = theta(4) * T4_est;                     % Geschätzte Strecken-Zeitkonstante T3
    T2_est = theta(3) * T4_est;                     % Geschätzte Strecken-Zeitkonstante T2
    T1_est = theta(2) * T4_est;                     % Geschätzte Strecken-Zeitkonstante T1
    K_est = theta(5) * T4_est;                      % Geschätzte Verstärkung K
    
    
    % Rekursive Least Squares MIT exponentiellem Vergessen:
    k_exp = P_exp*s/(q + s'*P_exp*s);
    P_exp = 1/q*(P_exp - k_exp*s'*P_exp);
    %eig(P_exp);
    theta_exp = theta_exp + k_exp*(y_v - s'*theta_exp);
    
    T4_est_exp = 1 / theta_exp(1);                  % Geschätzte Strecken-Zeitkonstante T4
    T3_est_exp = theta_exp(4) * T4_est_exp;         % Geschätzte Strecken-Zeitkonstante T3
    T2_est_exp = theta_exp(3) * T4_est_exp;         % Geschätzte Strecken-Zeitkonstante T2
    T1_est_exp = theta_exp(2) * T4_est_exp;         % Geschätzte Strecken-Zeitkonstante T1
    K_est_exp = theta_exp(5) * T4_est_exp;          % Geschätzte Verstärkung K
    
    
    % Werte Merken für Plot
    y_zvf_plot(j,3) = y_zvf(1);
    % y_zvf_dot_plot(j) = y_zvf(2);
    u_zvf_plot(j,3) = u_zvf(1);
    K_est_plot(j,3) = K_est;
    T1_est_plot(j,3) = T1_est;
    T2_est_plot(j,3) = T2_est;
    T3_est_plot(j,3) = T3_est;
    K_est_exp_plot(j,3) = K_est_exp;
    T1_est_exp_plot(j,3) = T1_est_exp;
    T2_est_exp_plot(j,3) = T2_est_exp;
    T3_est_exp_plot(j,3) = T3_est_exp;
    
    T4_est_plot(j,3) = T4_est;
    T4_est_exp_plot(j,3) = T4_est_exp;
    
end

%% Visualisierung

Visualisierung(t, [K_est_plot(:,1), T1_est_plot(:,1), T2_est_plot(:,1), T3_est_plot(:,1)],...
    [K_soll, T1_soll, T2_soll, T3_soll],'Rekursive LS ohne exp. Vergessen, Modell 3. Ordnung')

Visualisierung(t, [K_est_exp_plot(:,1), T1_est_exp_plot(:,1), T2_est_exp_plot(:,1), T3_est_exp_plot(:,1)],...
    [K_soll, T1_soll, T2_soll, T3_soll],'Rekursive LS mit exp. Vergessen, Modell 3. Ordnung')

Visualisierung(t, [K_est_plot(:,2), T1_est_plot(:,2), T2_est_plot(:,2)],...
    [K_soll, T1_soll, T2_soll],'Rekursive LS ohne exp. Vergessen, Modell 2. Ordnung')

Visualisierung(t, [K_est_exp_plot(:,2), T1_est_exp_plot(:,2), T2_est_exp_plot(:,2)],...
    [K_soll, T1_soll, T2_soll],'Rekursive LS mit exp. Vergessen, Modell 2. Ordnung')

Visualisierung(t, [K_est_plot(:,3), T1_est_plot(:,3), T2_est_plot(:,3), T3_est_plot(:,3), T4_est_plot(:,3)],...
    [K_soll, T1_soll, T2_soll, T3_soll, zeros(length(t),1)],'Rekursive LS ohne exp. Vergessen, Modell 4. Ordnung')

Visualisierung(t, [K_est_exp_plot(:,3), T1_est_exp_plot(:,3), T2_est_exp_plot(:,3), T3_est_exp_plot(:,3), T4_est_exp_plot(:,3)],...
    [K_soll, T1_soll, T2_soll, T3_soll, zeros(length(t),1)],'Rekursive LS mit exp. Vergessen, Modell 4. Ordnung')

figure
plot(t,y,'r','LineWidth',1);
hold on
plot(t, y_zvf_plot(:,1),'g','LineWidth',1);
plot(t, y_zvf_plot(:,2),'b','LineWidth',1);
plot(t, y_zvf_plot(:,3),'k','LineWidth',1);
legend('Wahres y','y_{zvf} Modell 3.Ordnung','y_{zvf} Modell 2.Ordnung','y_{zvf} Modell 4.Ordnung');

y_temp(:,1) = Ergebnis_Simulation([K_est_plot(end,1)], [T1_est_plot(end,1), T2_est_plot(end,1), T3_est_plot(end,1)], [0; 0; 0;], y_e, t, u);
y_temp(:,2) = Ergebnis_Simulation([K_est_plot(end,2)], [T1_est_plot(end,2), T2_est_plot(end,2)], [0; 0], y_e, t, u);
y_temp(:,3) = Ergebnis_Simulation([K_est_plot(end,3)], [T1_est_plot(end,3), T2_est_plot(end,3), T3_est_plot(end,3),...
    T4_est_plot(end,3)], [0; 0; 0; 0], y_e, t, u);

figure
plot(t,y,'r','LineWidth',1);
hold on
plot(t, y_zvf_plot(:,1),'g','LineWidth',1);
plot(t, y_zvf_plot(:,2),'b','LineWidth',1);
plot(t, y_zvf_plot(:,3),'k','LineWidth',1);
legend('Wahres y','y Modell 3.Ordnung','y Modell 2.Ordnung','y Modell 4.Ordnung');


%% Ergebnisdarstellung in Tabellen

% Modell 3. Ordnung
Ergebnis_Ordnung_3_Anteil_1 = table;
Ergebnis_Ordnung_3_Anteil_1.Parameter = {'K'; 'T1'; 'T2'; 'T3'};
Ergebnis_Ordnung_3_Anteil_1.Originale_Werte = [K(1); T1(1); T2(1); T3(1)];
Ergebnis_Ordnung_3_Anteil_1.Rekursives_Least_Squares = [K_est_plot(500/T_A,1); T1_est_plot(500/T_A,1); T2_est_plot(500/T_A,1);...
    T3_est_plot(500/T_A,1)];
Ergebnis_Ordnung_3_Anteil_1.Rekursives_Least_Squares_mit_exp_Vergessen = [K_est_exp_plot(500/T_A,1); T1_est_exp_plot(500/T_A,1);...
    T2_est_exp_plot(500/T_A,1); T3_est_exp_plot(500/T_A,1)];
Ergebnis_Ordnung_3_Anteil_1

Ergebnis_Ordnung_3_Anteil_2 = table;
Ergebnis_Ordnung_3_Anteil_2.Parameter = {'K'; 'T1'; 'T2'; 'T3'};
Ergebnis_Ordnung_3_Anteil_2.Originale_Werte = [K(2); T1(2); T2(2); T3(2)];
Ergebnis_Ordnung_3_Anteil_2.Rekursives_Least_Squares = [K_est_plot(end,1); T1_est_plot(end,1); T2_est_plot(end,1);...
    T3_est_plot(end,1)];
Ergebnis_Ordnung_3_Anteil_2.Rekursives_Least_Squares_mit_exp_Vergessen = [K_est_exp_plot(end,1); T1_est_exp_plot(end,1);...
    T2_est_exp_plot(end,1); T3_est_exp_plot(end,1)];
Ergebnis_Ordnung_3_Anteil_2

% Modell 2. Ordnung
Ergebnis_Ordnung_2_Anteil_1 = table;
Ergebnis_Ordnung_2_Anteil_1.Parameter = {'K'; 'T1'; 'T2'};
Ergebnis_Ordnung_2_Anteil_1.Originale_Werte = [K(1); T1(1); T2(1)];
Ergebnis_Ordnung_2_Anteil_1.Rekursives_Least_Squares = [K_est_plot(500/T_A,2); T1_est_plot(500/T_A,2); T2_est_plot(500/T_A,2)];
Ergebnis_Ordnung_2_Anteil_1.Rekursives_Least_Squares_mit_exp_Vergessen = [K_est_exp_plot(500/T_A,2); T1_est_exp_plot(500/T_A,2);...
    T2_est_exp_plot(500/T_A,2)];
Ergebnis_Ordnung_2_Anteil_1

Ergebnis_Ordnung_2_Anteil_2 = table;
Ergebnis_Ordnung_2_Anteil_2.Parameter = {'K'; 'T1'; 'T2'};
Ergebnis_Ordnung_2_Anteil_2.Originale_Werte = [K(2); T1(2); T2(2)];
Ergebnis_Ordnung_2_Anteil_2.Rekursives_Least_Squares = [K_est_plot(end,2); T1_est_plot(end,2); T2_est_plot(end,2)];
Ergebnis_Ordnung_2_Anteil_2.Rekursives_Least_Squares_mit_exp_Vergessen = [K_est_exp_plot(end,2); T1_est_exp_plot(end,2);...
    T2_est_exp_plot(end,2)];
Ergebnis_Ordnung_2_Anteil_2

% Modell 4. Ordnung
Ergebnis_Ordnung_4_Anteil_1 = table;
Ergebnis_Ordnung_4_Anteil_1.Parameter = {'K'; 'T1'; 'T2'; 'T3'; 'T4'};
Ergebnis_Ordnung_4_Anteil_1.Originale_Werte = [K(1); T1(1); T2(1); T3(1); NaN];
Ergebnis_Ordnung_4_Anteil_1.Rekursives_Least_Squares = [K_est_plot(500/T_A,3); T1_est_plot(500/T_A,3); T2_est_plot(500/T_A,3);...
    T3_est_plot(500/T_A,3); T4_est_plot(500/T_A,3)];
Ergebnis_Ordnung_4_Anteil_1.Rekursives_Least_Squares_mit_exp_Vergessen = [K_est_exp_plot(500/T_A,3); T1_est_exp_plot(500/T_A,3);...
    T2_est_exp_plot(500/T_A,3); T3_est_exp_plot(500/T_A,3); T4_est_exp_plot(500/T_A,3)];
Ergebnis_Ordnung_4_Anteil_1

Ergebnis_Ordnung_4_Anteil_2 = table;
Ergebnis_Ordnung_4_Anteil_2.Parameter = {'K'; 'T1'; 'T2'; 'T3'; 'T4'};
Ergebnis_Ordnung_4_Anteil_2.Originale_Werte = [K(2); T1(2); T2(2); T3(2); NaN];
Ergebnis_Ordnung_4_Anteil_2.Rekursives_Least_Squares = [K_est_plot(end,3); T1_est_plot(end,3); T2_est_plot(end,3);...
    T3_est_plot(end,3); T4_est_plot(end,3)];
Ergebnis_Ordnung_4_Anteil_2.Rekursives_Least_Squares_mit_exp_Vergessen = [K_est_exp_plot(end,3); T1_est_exp_plot(end,3);...
    T2_est_exp_plot(end,3); T3_est_exp_plot(end,3); T4_est_exp_plot(end,3)];
Ergebnis_Ordnung_4_Anteil_2


%% Hilfsfunktionen
function [] = Visualisierung(t, est_plot, soll, titel)
index = find(est_plot(1,:));
label = {'K_{est}'; 'T1_{est}'; 'T2_{est}'; 'T3_{est}'; 'T4_{est}'};
laenge = size(est_plot,2);

figure;
for i = 1:laenge
    subplot(1,laenge,i);
    plot(t,est_plot(:,i),'LineWidth',2);
    hold on;
    plot(t,soll(:,i),'r','LineWidth',1);
    xlim([0 2000]);
    ylim([min(min(est_plot(:,i))-2,min(soll(:,i))-2) max(max(est_plot(:,i))+2,max(soll(:,i))+2)]);
    xlabel('t');
    ylabel(char(label(i)));
    hold on;
end
sgtitle(titel);
end


function y = Ergebnis_Simulation(K, T, x_0_mess, y_e, t, u)
% Funktion zur Bestimmung des Ausgangssignals mit den bestimmten Parametern
% Eingangssignale: Verstärkung, Zeitkonstanten, Anfangswert, Arbeitspunkt, Zeitvektor und Eingang u
% Ausgangssignale: Ausganng y
if length(T) == 2 && length(K) == 1
    A = [0 1; -(1/T(2)) -(T(1)/T(2))];
    B = [0 K(1)/T(2)]';
    C = [1 0];
    D = 0;
elseif length(T) == 3 && length(K) == 1
    A = [0 1 0; 0 0 1; -(1/T(3)) -(T(1)/T(3)) -(T(2)/T(3))];
    B = [0 0 K(1)/T(3)]';
    C = [1 0 0];
    D = 0;
elseif length(T) ==3 && length(K) == 2
    A = [0 1 0; 0 0 1; -(1/T(3)) -(T(1)/T(3)) -(T(2)/T(3))];
    B = [0 0 1]';
    C = [K(1)/T(3) K(1)*K(2)/T(3) 0];
    D = 0;
elseif length(T) == 4 && length(K) == 1
    A = [0 1 0 0; 0 0 1 0; 0 0 0 1; -(1/T(4)) -(T(1)/T(4)) -(T(2)/T(4)) -(T(3)/T(4))];
    B = [0 0 0 K(1)/T(4)]';
    C = [1 0 0 0];
    D = 0;
elseif length(T) == 4 && length(K) == 2
    A = [0 1 0 0; 0 0 1 0; 0 0 0 1; -(1/T(4)) -(T(1)/T(4)) -(T(2)/T(4)) -(T(3)/T(4))];
    B = [0 0 0 1]';
    C = [K(1)/T(4) K(1)*K(2)/T(4) 0 0];
    D = 0;
end
system = ss(A,B,C,D);

x_0 = x_0_mess - y_e;
y = lsim(system, u, t, x_0);
end
