close all;
clear all;

%% Erzeugen der Messwerte (durch Simulation)
%PT1 
% T*dy/dt + y = K*u
T = 300;
K = 10;

y_e = 0;                %Arbeitspunkt (Ruhelage)
u_e = 0;                 %Arbeitspunkt (Ruhelage)

global T_A;
global t;
global u;
global y;


%Signale erzeugen
T_A = 0.1; %Abtastzeit sec
t = (0:T_A:2000)';      %Vorgabe der Messzeitpunkte für Simulation
u = [zeros(100,1); ones(size(t,1)-100,1)];  %Eingangssprung (Achtung für Identifikation ist Sprungantwort nicht ideal, wegen persistent excitation!)

% Zustandsraumdarstellung PT1
system = ss(-1/T, K/T, 1, 0);
% Anfangswert Großsignalverhalten
x_0_mess = 0; %Wenn x_0_mess = y_e, dann Erregung aus der Ruhelage
%Anfangswert Kleinsignalverhalten (um die Ruhelage)
x_0 = x_0_mess - y_e;
y = lsim(system, u, t, x_0);


%Großsignalverhalten inkl. Messrauschen berechnen
y_mess = y + y_e; %Arbeitspunkt
y_mess = y_mess + 0.05*randn(size(t,1),1); %Messrauschen
u_mess = u + u_e;


%% Plotten
T_soll = [ones(size(t,1),1)*300];
K_soll = [ones(size(t,1),1)*10];


figure;
subplot(2,1,1);
plot(t,u_mess,'r','LineWidth',2);
xlabel('t');
ylabel('u_{mess}');

subplot(2,1,2);
plot(t,y_mess,'blue','LineWidth',2);
xlabel('t');
ylabel('y_{mess}');

