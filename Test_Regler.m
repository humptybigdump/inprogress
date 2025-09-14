%% Initialisierung
first_run = true;       % Um Logik der Initilaisierung in Strecke.m zu steuern

Schlacketemp_AP = 600;  % Arbeitspunkt für Regelgröße Schlacketempertur 
Prozessluft_AP = 800;   % Arbeitspunkt für Stellgröße Prozessluft

delta_t = 5/60;         % Abtastzeit in Minuten (5 sec)

% Beim ersten Start wird so getan, als ob wir vom Handbetrieb in den Automatikbetrieb wechseln
auto_old = 0;           % vorheriger Zyklus war noch Handbetrieb 
auto = 1;               % ab jetzt: Automatikbetrieb 

% Sollwert bei Start auf Arbeitspunkt setzen
r = Schlacketemp_AP;

% Vektoren für Datenaufzeichnung und späteres Plotten
t=[0:delta_t:1000]'; % Zeitvektor t in Minuten, Simulation in 5-sec-Schritten
U = zeros(size(t,1),1);
X = zeros(size(t,1),1);
P_vec = zeros(size(t,1),1);
I_vec = zeros(size(t,1),1);
D_vec = zeros(size(t,1),1);
R = zeros(size(t,1),1);
R_filtered = zeros(size(t,1),1);

%% Simulation des Regelkreises
for i=1:size(t,1) 
    
    %% Simulation des Regelkreises
    Strecke; % Einschritt-Simulation Strecke
    Regler;  % Einschritt-Simulation Regler
 
    %% Verschiedene Führungs- und Störszenarien erzeugen:
    % Führungsverhalten
    if (t(i) > 30); r = Schlacketemp_AP + 400; end      % Sollwert springt nach 30 min nach oben (Hochfahren des Ofens aus Stand-By)
    if (t(i) > 300); r = Schlacketemp_AP + 100 ; end    % Sollwert springt nach 300 min nach unten
    
    %Störverhalten
    %if (t(i)>500 && t(i)<500+60); x_sim(2) = x_sim(2)+0.1389*2;end  % Temperatur in Zone 2 FB sinkt um 100 K innerhalb einer Stunde
    %if (t(i)==500); x_sim(2) = x_sim(2)-50;end                      % Temperatur in Zone 2 FB sinkt plötzlich um 50 K 
       
    %Störung der Stellgröße (plötzliches Offset von 200) nach 2 Stunden
    %if t(i) > 120; u = u + 200; end
    
    % Datenprotokollierung für späteres Plotten
    R(i) = r;                        % Sollwertvorgabe durch Wartenpersonal
    R_filtered(i) = r_filtered_PT2;  % gefilterter Sollwert (Führungsgrößenfilterung)
    Y(i) = y;                        % Istwert
    U(i) = u;                        % Stellwert gesamt
    P_vec(i) = P;                    % P-Anteil Stellwert
    I_vec(i) = I;                    % I_Anteil Stellwert
    D_vec(i) = D;                    % D-Anteil Stellwert
    
end

%% Plotten der Ergebnisse
close all;
subplot(3,1,1);
h=plot(t, R,'blue');hold on;set(h,'linewidth',2);
h=plot(t, R_filtered,'black');set(h,'linewidth',2);
h=plot(t, Y, 'red');set(h,'linewidth',2);
ylim([400 1200]);
xlim([0 900]);
h=legend('Sollwert','gefilterter Sollwert', 'gemessene Temperatur');%, 'Temperatur aus Simulink');
set(h,'Location','NorthEast');
ylabel('Temperatur (°C)');

subplot(3,1,2);hold on;
h=plot(t, U, 'black');
set(h,'linewidth',2);
legend('Prozessluft');
xlim([0 900]);
ylim([400 2000]);
xlabel('Zeit (min)');
ylabel('Prozessluft (Umin^{-1})');

subplot(3,1,3);
hold on;
plot(t, P_vec, 'red');
plot(t, I_vec, 'green');
plot(t, D_vec, 'blue');
plot(t, U, 'black');
xlim([0 900]);
h=legend('P-Anteil des Stellwerts','I-Anteil des Stellwerts','D-Anteil des Stellwerts','Gesamtstellwert'); 
set(h,'Location','SouthEast');
