%% Vorsteuerentwurf über den flachen Ausgang: "Kochrezept" S.27 im Skript
close all;
clear all;

%% Strecke 
G = tf([1 5 -7],[1 1 1 3]);

% Ausgangspunkt: Regelungsnormalform
A = [0 1 0; 0 0 1; -3 -1 -1]
B = [0 0 1]'
C = [-7 5 1]
D = 0

% Der flache Ausgang ist der erste Zustand der Regelungsnormalform
% z = x1

%% Entwurf des Sollsignals zd(t) für z anhand der y-Sollwertforderung: z.B. Innerhalb von T = 5s von 0 auf 1 mit einer S Kurve. 

% Da es sich um eine Strecke 3. Grades handelt, wird eine S-Kurve 7. Grades benötigt.
% Es ist:   yd(0) = 0               yd(T) = 1
%           yd_d(0) = 0             yd_d(T) = 0 
%           yd_dd(0) = 0            yd_dd(T) = 0
%           yd_ddd(0) = 0           yd_ddd(T) = 0
%           zd(0) = 1/c1 * yd(0)    zd(T) = 1/c1 * yd(T)

%% Entwurf des Sollsignals zd(t) für den flachen Ausgang über S-Kurven-Formel
yd_0 = 0;   % Startwert (muss zu Anfangswert des Systems passen)
yd_T = 7;   % Endwert
T = 5;      % Transitionszeit

p4 = 35;
p5 = -84;
p6 = 70;
p7 = -20;

syms zd(t)
zd(t) =  yd_0/C(1) + (yd_T/C(1) - yd_0/C(1))*(p4*(t/T)^4 + p5*(t/T)^5 + p6*(t/T)^6 + p7*(t/T)^7);

% Ableitungen symbolisch berechnen
zd_d(t) = diff(zd(t))
zd_dd(t) = diff(zd_d(t))
zd_ddd(t) = diff(zd_dd(t))

%% Differenzielle Parametrierung
ud(t) = A(3,1)*zd(t) + A(3,2)*zd_d(t) + A(3,3)*zd_dd(t) + zd_ddd(t)
yd(t) = C(1)*zd(t) + C(2)*zd_d(t) + C(3)*zd_dd(t)
xd_1(t) = zd(t)
xd_2(t) = zd_d(t)
xd_3(t) = zd_dd(t)


%% Visualisierung
figure
subplot(5,1,1)
fplot(@(t) yd(t),[0 T],'b','Linewidth',1)
hold on
xlabel('time')
ylabel('y_{d}')
grid on

subplot(5,1,2)
fplot(@(t) ud(t),[0 T],'b','Linewidth',1)
xlabel('time')
ylabel('u_{d}')
grid on
sgtitle('Sollsignal, Vorsteuersignal und Zustandsverläufe')

subplot(5,1,3)
fplot(@(t) xd_1(t),[0 T],'b','Linewidth',1)
xlabel('time')
ylabel('x_{d1} = z_{d}')
grid on

subplot(5,1,4)
fplot(@(t) xd_2(t),[0 T],'b','Linewidth',1)
xlabel('time')
ylabel('x_{d2}')
grid on

subplot(5,1,5)
fplot(@(t) xd_3(t),[0 T],'b','Linewidth',1)
xlabel('time')
ylabel('x_{d3}')
grid on



