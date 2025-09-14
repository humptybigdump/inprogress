%% Vorlage für Parameteridentifikation im Online-Betrieb
close all;
clear all;

%% Generiere Messdaten 
% In folgendem Skript werden die Messdaten (y und u) für die Parameteridentifikation generiert. Versuchen Sie, 
% das Skript in dem die Messwerte generiert werden, zu verstehen. 
% Untersuchen Sie, wie sich Veränderungen der Parameter auf das Ausgangssignal auswirken.
PT3_Generiere_Messdaten_online;


%% Leere Vektoren für späteres Plotten definieren
y_zvf_plot = zeros(length(t), 1);
y_zvf_dot_plot = zeros(length(t), 1);
u_zvf_plot = zeros(length(t), 1);
K_est_plot = zeros(length(t), 1);
T1_est_plot = zeros(length(t), 1);
T2_est_plot = zeros(length(t), 1);
T3_est_plot = zeros(length(t), 1);
K_est_exp_plot = zeros(length(t), 1);
T1_est_exp_plot = zeros(length(t), 1);
T2_est_exp_plot = zeros(length(t), 1);
T3_est_exp_plot = zeros(length(t), 1);


%% Parameteridentifikation allgemein Arbeitspunkt
% 1. Arbeitspunkt abziehen
y = 
u =


%% Rekursive Parameteridentifikation (zeit-kontinuierlich)
% Bestimmung der gefilterten Größen und zeitlichen Ableitung über Zustandsvariablenfilter ZVF
% Zustandsvariablenfilter muss zuerst initialisiert werden: Achten Sie auf die Dimension des Zustandsvariablenfilters
% für eine PT3-Strecke.
% A,b,C und d müssen von Ihnen implementiert werden

ZVF = ss(A,b,C,d);

% Zeitdiskrete Realisierung des ZVF für Eingang und abspeichern der Matrizen für die spätere Verwendung
ZVFdu = 
[Ad, bd, Cd, dd] = 

% Zeitdiskrete Realisierung des ZVF für Ausgang und abspeichern der Matrizen für die spätere Verwendung
ZVFdy = 
[Ad2, bd2, Cd2, dd2] = 

% Anfangszustände des ZVF für u und y
xy = 
xu = 

% Für rekursive LS: Wichtungsmatrix und Anfangswerte (Startwissen) vorgeben
P = 
theta =   

% Für rekursive LS mit exponentiellem Vergessen: Wichtungsmatrix, Gedächtnisfaktor und Anfangswerte (Startwissen)
% vorgeben
P_exp = 
q =                       
theta_exp = 

% Achtung: Auch wenn mit den exakt richtigen Parametern theta gestartet wird, 
% kann sich theta von den exakten Werten zwischenzeitlich entfernen!

% In jedem Zeitschritt j wird mit dem neu erfassten Wert y(j) der ZVF
% aktualisiert und mit rekursivem Least Squares ein Update für den Parametervektor
% berechnt.
% Achtung: Lösung der rekursiven LS ist nicht identisch mit Lösung direkte
% LS! 


for j=1:length(t) 
   
    % ZVF für Eingang u: Bestimmen Sie zuerst den Eingang mithilfe der Matrizen der zeitdiskreten 
    % Realisierung des ZVF für den Eingang (ZVFdu) und dem neuen Eingang zum Zeitpunkt j. 
    % Aktualisieren Sie danach erst den Zustand mit den Matrizen und dem neuen Eingang.
    u_zvf = 
    xu = 
 
    % ZVF für Ausgang y: Bestimmen Sie zuerst den Ausgang mithilfe der Matrizen der zeitdiskreten 
    % Realisierung des ZVF für den Ausgang (ZVFdy) und dem neuen Ausgang zum Zeitpunkt j. 
    % Aktualisieren Sie danach erst den Zustand mit den Matrizen und dem neuen Ausgang.
    y_zvf =                        
    xy = 
    
    % Führen Sie jetzt mit den berechneten Messwerten u_zvf und y_zvf ein LS durch:
    % Zuerst Definition des Messwerts und des Datenvektors
    y_v =                                       % Messwert 
    S =                                         % Datenvektor
    
    
    % Ab hier: Berechnung der Parameter theta, dies kann auch nur alle n-Zyklen durchgeführt werden, 
    % was ein robusterer Verhalten gewährleistet. 
    
    % Rekursive Least Squares OHNE Vergessen:
    k =                         
    P = 
    theta = 
    T3_est =                    % Geschätzte Strecken-Zeitkonstante T3
    T2_est =                    % Geschätzte Strecken-Zeitkonstante T2
    T1_est =                    % Geschätzte Strecken-Zeitkonstante T1
    K_est =                     % Geschätzte Verstärkung K


    % Rekursive Least Squares MIT exponentiellem Vergessen:
    k_exp = 
    P_exp = 
    theta_exp = 
    T3_est_exp =                % Geschätzte Strecken-Zeitkonstante T3
    T2_est_exp =                % Geschätzte Strecken-Zeitkonstante T2
    T1_est_exp =                % Geschätzte Strecken-Zeitkonstante T1
    K_est_exp =                 % Geschätzte Verstärkung K


    % Werte Merken für Plot
    u_zvf_plot(j) = u_zvf(1);     
    K_est_plot(j) = K_est;
    T1_est_plot(j) = T1_est;
    T2_est_plot(j) = T2_est;
    T3_est_plot(j) = T3_est;
    K_est_exp_plot(j) = K_est_exp;
    T1_est_exp_plot(j) = T1_est_exp;
    T2_est_exp_plot(j) = T2_est_exp;
    T3_est_exp_plot(j) = T3_est_exp;

end

%% Plots für rekursives Least Squares OHNE exponentielles Vergessen
index = find(K_est_plot);

figure;
subplot(1,4,1);
title('Rekursive LS ohne exponentielles Vergessen');hold on;
plot(t(index),K_est_plot(index),'LineWidth',2);
hold on;
plot(t,K_soll,'r','LineWidth',1);
xlim([0 2000]);
ylim([0 20]);
xlabel('t');
ylabel('K_{est}');
hold on;

subplot(1,4,2);
plot(t(index),T1_est_plot(index),'LineWidth',2);
hold on;
plot(t,T1_soll,'r','LineWidth',1);
xlim([0 2000]);
ylim([0 800]);
xlabel('t');
ylabel('T1_{est}');
hold on;

subplot(1,4,3);
plot(t(index),T2_est_plot(index),'LineWidth',2);
hold on;
plot(t,T2_soll,'r','LineWidth',1);
xlim([0 2000]);
ylim([0 800]);
xlabel('t');
ylabel('T2_{est}');
hold on;

subplot(1,4,4);
plot(t(index),T3_est_plot(index),'LineWidth',2);
hold on;
plot(t,T3_soll,'r','LineWidth',1);

xlim([0 2000]);
ylim([0 800]);
xlabel('t');
ylabel('T3_{est}');
hold on;


%% Plots für rekursives Least Squares MIT exponentiellem Vergessen
index = find(K_est_exp_plot);

figure;
subplot(1,4,1);
title('Rekursive LS mit exponentiellem Vergessen');hold on;
plot(t(index),K_est_exp_plot(index),'LineWidth',2);
hold on;
plot(t,K_soll,'r','LineWidth',1);
xlim([0 2000]);
ylim([0 20]);
xlabel('t');
ylabel('K_{est}');
hold on;

subplot(1,4,2);
plot(t(index),T1_est_exp_plot(index),'LineWidth',2);
hold on;
plot(t,T1_soll,'r','LineWidth',1);
xlim([0 2000]);
ylim([0 800]);
xlabel('t');
ylabel('T1_{est}');
hold on;

subplot(1,4,3);
plot(t(index),T2_est_exp_plot(index),'LineWidth',2);
hold on;
plot(t,T2_soll,'r','LineWidth',1);
xlim([0 2000]);
ylim([0 800]);
xlabel('t');
ylabel('T2_{est}');
hold on;

subplot(1,4,4);
plot(t(index),T3_est_exp_plot(index),'LineWidth',2);
hold on;
plot(t,T3_soll,'r','LineWidth',1);
xlim([0 2000]);
ylim([0 800]);
xlabel('t');
ylabel('T3_{est}');
hold on;


  