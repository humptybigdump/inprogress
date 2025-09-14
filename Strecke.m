%% Schnittstellendefinition
% Eingang
% u;          % Stellwert Drehzahl Gebläse Stellbegrenzung 500...1500
% Ausgang
% y;          % Istwert  (Ist-Schlacke-Temperatur °C)
%% Initialisierung
if (first_run)
    first_run = false;
    % Strecken-Anfangswerte (Kleinsignal)
    u = Prozessluft_AP;
    u_hand = Prozessluft_AP;
    u_sim_old = 0;
    x_sim = [0;0;0];
    x_sim_allpass = 0;
    u_sim_vorfilter = 0;
    params = [  20    0.4   30   0.9  1  0.5]; %aus Identifikation
    T_FB3 = params(1);
    Gain_Fe_Oxid = params(2);
    T_2 = params(3);
    Gain_FB2 = params(4);
    T_G = params(5);
    Gain_G_to_FB2 = params(6);
    A = [-1/T_G, 0, 1/T_G; Gain_G_to_FB2*1/T_2, -1/T_2 0; 0, Gain_FB2*1/T_FB3, -1/T_FB3];
    b = [0; 0; Gain_Fe_Oxid/T_FB3];
    c = [0 0 1];
    d = 0;
    SYSC = ss(A,b,c,0);
    % Berechnen des zeitdiskreten Modells
    SYSD = c2d(SYSC,delta_t,'zoh');
    [A_d,b_d,c_d,d_d]=ssdata(SYSD);
    T_Allpass = 2;
    Gain_Allpass = 12 * 1.5;
    c_filter_allpass = exp(-delta_t/T_Allpass);
end


%% Simulation
%Streckeneingang u Arbeitspunkt abziehen
u_sim = u - Prozessluft_AP;

% Allpass nur in eine Richtung (Details siehe Paper)
delta_u_sim = (u_sim - u_sim_old)/delta_t;
u_sim_old = u_sim;
x_sim_allpass = c_filter_allpass * x_sim_allpass + (1 - c_filter_allpass) *  max(delta_u_sim,0);
u_sim_allpass = u_sim - Gain_Allpass * x_sim_allpass;

% Kleinsignalverhalten Strecke (Einschritt-Simulation auf Basis zeitdiskretem Modell)
x_sim =  A_d * x_sim + b_d * u_sim_allpass;
y_sim =  c_d * x_sim;

% zurück zum Großsignalverhalten und ggf. noch Messrauschen dazu addieren
Messrauschen = 30; % Übung: 0 oder 30
y = y_sim + Schlacketemp_AP + Messrauschen*randn;




