
close all;
%% Konstanten definieren
m = 1; %t

%% Zustandsraummodell
% x(1) : Position
% x(2) : Geschwindigkeit

A = [0 1; 0 0];
b = [0; 1/m];
c = [1 0];
d = 0;
sys = ss(A,b,c,d);

%% Sollsignal für Folgeregelung definieren/berechnen
t = [0:0.01:10]';

Variante = 2;

if Variante == 1
    % Variante 1: Sollposition entspricht zeitlichem Sinus (hin- und herpendeln)
    y_d = sin(t);
    dy_d = cos(t);
    ddy_d = -sin(t);
    x_0 = [0; 1]; % Anfangswert hier kompatibel zu Sollsignal y_d = sin(t) gewählt
end

if Variante == 2
    % Variante 2: Zustandswechsel von x_0 = [0;0] auf [100;0] in 5 sec auf glatter Kurve (Polynom)
    % Polynom berechnen (wird in Vorlesung "Regelung mir Vorsteuerung" erklärt):
    y_0 = 0;    % Startposition
    y_T = 100;  % Endposition
    T = 5;      % Zeitvorgabe für Zustandswechsel
    y_d = y_0 + (y_T - y_0)*(10*t.^3/T^3 - 15*t.^4/T^4 + 6*t.^5/T^5);
    dy_d = (y_T - y_0)*(30*t.^2/T^3 - 60*t.^3/T^4 + 30*t.^4/T^5);
    ddy_d = (y_T - y_0)*(60*t/T^3 - 180*t.^2/T^4 + 120*t.^3/T^5);
    x_0 = [0; 0];
    % Polynome gelten nur bis t <= T, danach:
    idx = find(t>T);
    y_d(idx) = y_T;
    dy_d(idx) = 0;
    ddy_d(idx) = 0;
end


%% PD-Regler Folgeregelung ohne Vorsteuerung
% u = -k_p * (y - y_d) - k_d * (\dot y - \dot y_d)
% u = -[k_p, k_d] * [y; \dot y] + k_p * y_d + k_d * \dot y_d;
% u = -k * x + v_d
k_p = 1;
k_d = 1;
k = [k_p, k_d];

A_RK = A-b*k;
b_RK = b;
c_RK = c;
d_RK = d;

% neuer Eingang:
v_d = k_p*y_d + k_d*dy_d;

sys_RK = ss(A_RK, b_RK, c_RK, d_RK);

y_RK = lsim(sys_RK, v_d, t, x_0);

%% PD-Regler Folgeregelung ohne Vorsteuerung
% u = ddy_d - k_p * (y - y_d) - k_d * (\dot y - \dot y_d)
% u = -k * x + ddy_d + k_p * y_d + k_d * \dot y_d;
% u = -k * x + v_d

% neuer Eingang:
v_d = ddy_d + k_p*y_d + k_d*dy_d;
y_RK_VS = lsim(sys_RK, v_d, t, x_0);

%% Plotten
plot(t, y_RK,'linewidth',3);
hold on;
plot(t, y_RK_VS,'linewidth',3);
plot(t, y_d, 'linewidth',1);

legend( 'y PD-Regler', 'y PD-Regler mit Vorsteuerung','y_d','Location','southeast');


