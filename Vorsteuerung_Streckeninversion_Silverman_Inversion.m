%% Vorsteuerung per Streckeninversion (Übungsblatt Aufgabe 1) und Silverman-Inversion (Skript Folie 23)
close all
clear all

%% Signal yd(t) und dessen Ableitungen symbolisch berechnen

yd_0 = 0;       % Startwert
yd_T = 5;       % Endwert
T = 30;         % Transitionszeit

% Für C^3-Signal ist Polynom 7. Ordnung notwendig
p4 = 35;
p5 = -84;
p6 = 70;
p7 = -20;

% yd(t) als symbolische Größe definieren
syms yd(t)
yd(t) =  yd_0 + (yd_T - yd_0)*(p4*(t/T)^4 + p5*(t/T)^5 + p6*(t/T)^6 + p7*(t/T)^7);
figure
fplot(@(t) yd(t),[0 T],'b','Linewidth',1)
xlabel('time')
ylabel('y_{d}')
title('Sollsignal y_{d}');
grid on

% Da yd(t) ein eine symbolische Größe ist, wird hier durch den diff-Befehl symbolisch abgeleitet
% n = 3, n-m = 1
yd_d(t) = diff(yd(t));
yd_dd(t) = diff(yd_d(t));   % Brauchen wir hier nur für Streckeninversion nicht für Silverman-Inversion
yd_ddd(t) = diff(yd_dd(t)); % Brauchen wir hier nur für Streckeninversion nicht für Silverman-Inversion

time = (0:0.01:T)';

%% Silverman-Inversion

Zaehler = [1 5 6];
Nenner = [1 1 1 3];
G = tf(Zaehler, Nenner);

[q, r] = deconv(Nenner, Zaehler);

% Für Rest numerische Simulation
system_rest = tf(r,Zaehler);
ud_num = lsim(system_rest,double(yd(time)),time); % double(yd(time))-Berechnen echter Werte

ud_1 = q(1)*double(yd_d(time)) + q(2)*double(yd(time)) + ud_num;

figure
plot(time, ud_1,'b','Linewidth',1)
xlabel('time')
ylabel('u_{d1}')
title('Vorsteuersignal über Silverman-Inverse bei bekanntem y_{d}');
grid on

%% Streckeninversion

% 1. Ausführen der Inversion
G_inv = tf(Nenner, Zaehler);

% 2. Berechnung Hilfssignal vd(t)
syms vd(t)
vd(t) = yd_ddd(t) + Nenner(2)*yd_dd(t) + Nenner(3)*yd_d(t) + Nenner(4)*yd(t);

% 3. Filtern des Hilfssignals über das reduzierte System
system_rest = tf(1,Zaehler);
ud_2 = lsim(system_rest,double(vd(time)),time);

figure
plot(time, ud_2,'b','Linewidth',1)
xlabel('time')
ylabel('u_{d2}')
title('Vorsteuersignal über Streckeninversion bei bekanntem y_{d}');
grid on

