clear; 
close all; 
clc;

% Nina Kunze
% Numerisches Modell

%% Daten einlesen

% Messstelle 1
opts_L1 = delimitedTextImportOptions('Delimiter', ',', 'DataLines', 2);      % durch Kommas getrennt, ab der 2.Zeile
opts_L1.VariableNames = {'t_L1_unix', 'volt', 'T_L1', 'c_L1', 'sat'};        % Spaltennamen definieren
opts_L1.VariableTypes = {'double', 'double', 'double', 'double','double'};   % Alle Spalten werden als numerisch eingelesen
data_L1 = readtable('Felddaten_Logger_1_kalibriert.txt', opts_L1);
data_L1.t_L1 = datetime(data_L1.t_L1_unix, 'ConvertFrom','posixtime','TimeZone','Europe/Berlin');   % Unix Zeit in datetime

% Messstelle 2
opts_L2 = opts_L1;
opts_L2.VariableNames = {'t_L2_unix', 'volt', 'T_L2', 'c_L2', 'sat'};
data_L2 = readtable('Felddaten_Logger_2_kalibriert.txt', opts_L2);
data_L2.t_L2 = datetime(data_L2.t_L2_unix, 'ConvertFrom','posixtime','TimeZone','Europe/Berlin');

% Messstelle 3
opts_L3 = opts_L1;
opts_L3.VariableNames = {'t_L3_unix', 'volt', 'T_L3', 'c_L3', 'sat'};
data_L3 = readtable('Felddaten_Logger_3_kalibriert.txt', opts_L3);
data_L3.t_L3 = datetime(data_L3.t_L3_unix, 'ConvertFrom','posixtime','TimeZone','Europe/Berlin');

% Messstelle 3 inkl. Goldersbach
opts_L3G = opts_L1;
opts_L3G.VariableNames = {'t_L3G_unix', 'volt', 'T_L3G', 'c_L3G', 'sat'};
data_L3G = readtable('M3_Verduennung_Goldersbach.txt', opts_L3G);
data_L3G.t_L3G = datetime(data_L3G.t_L3G_unix, 'ConvertFrom','posixtime','TimeZone','Europe/Berlin');

% Messstelle 4
opts_L4 = opts_L1;
opts_L4.VariableNames = {'t_L4_unix', 'volt', 'T_L4', 'c_L4', 'sat'};
data_L4 = readtable('Felddaten_Logger_4_kalibriert.txt', opts_L4);
data_L4.t_L4 = datetime(data_L4.t_L4_unix, 'ConvertFrom','posixtime','TimeZone','Europe/Berlin');

% Strahlungsdaten
Strahlung = readtable('strahlung.csv', 'Delimiter', ',');

timeStrings = Strahlung{:,1};     
t_R = datetime(string(timeStrings), 'InputFormat','yyyy-MM-dd HH:mm:ssXXX','TimeZone','Europe/Berlin');    % in datetime

R_1 = Strahlung{:,3};   % Strahlungswerte M1-M2
R_2 = Strahlung{:,4};   % Strahlungswerte M2-M3
R_3 = Strahlung{:,5};   % Strahlungswerte M3-M4

% Als Orientierung der Startwerte für R_0.5
R05_1 = mean(R_1); 
R05_2 = mean(R_2); 
R05_3 = mean(R_3); 

%%  Daten vorverarbeiten 

% Alle Zeilen mit NaN entfernen
data_L1 = rmmissing(data_L1);
data_L2 = rmmissing(data_L2);
data_L3 = rmmissing(data_L3);
data_L3G = rmmissing(data_L3G);
data_L4 = rmmissing(data_L4);

% Zeitraum zuschneiden in MESZ
StartDatum = datetime('2025-08-10 00:00:00','TimeZone','Europe/Berlin');
EndDatum   = datetime('2025-08-11 22:00:00','TimeZone','Europe/Berlin');

data_L1 = data_L1(data_L1.t_L1 >= StartDatum & data_L1.t_L1 <= EndDatum, :);
data_L2 = data_L2(data_L2.t_L2 >= StartDatum & data_L2.t_L2 <= EndDatum, :);
data_L3 = data_L3(data_L3.t_L3 >= StartDatum & data_L3.t_L3 <= EndDatum, :);
data_L3G = data_L3G(data_L3G.t_L3G >= StartDatum & data_L3G.t_L3G <= EndDatum, :);
data_L4 = data_L4(data_L4.t_L4 >= StartDatum & data_L4.t_L4 <= EndDatum, :);

%% Variablen extrahieren 

% L1
t_L1 = data_L1.t_L1;  
T_L1 = data_L1.T_L1;  
c_L1 = data_L1.c_L1;

% L2
t_L2 = data_L2.t_L2;  
T_L2 = data_L2.T_L2;  
c_L2 = data_L2.c_L2;

% L3
t_L3 = data_L3.t_L3;  
T_L3 = data_L3.T_L3;  
c_L3 = data_L3.c_L3;

% L3G
t_L3G = data_L3G.t_L3G; 
T_L3G = data_L3G.T_L3G; 
c_L3G = data_L3G.c_L3G;

% L4
t_L4 = data_L4.t_L4; 
T_L4 = data_L4.T_L4;  
c_L4 = data_L4.c_L4;    

dx = 20;      % Schrittweite [m] (Auflösung)

%% Modell 1 (Abschnitt M1-M2)
                
%% Modellparameter & Zeit

L1 = 1325.146+50;       % Flusslänge [m] (50m länger als Messabschnitt 1-2)
x1 = (0:dx:L1)';        % Ortsvektor von 0 bis L1 in 10 m Schritten
nx1 = length(x1);       % Anzahl der Gitterpunkte

v1 =  0.375;            % Fließgeschwindigkeit [m/s]
dt1 = dx/v1;            % Zeitschritt [s]
D1 = 1.64;              % Dispersionskoeffizient [m²/s]

t_end1 = seconds(t_L2(end) - t_L1(1)) + dt1;      % Modellzeitdauer in Sekunden (dt, damit das Zeitgitter auch den Endzeitpunkt enthält)
t_mod1 = (0:dt1:t_end1)';                         % Zeitvektor im Modell
nt1 = length(t_mod1) - 1;                         % Anzahl der Zeitschritte (-1, weil von einem Zeitpunkt zum nächsten)

x_obs1 = 1325.146;                        % Position des Messpunkts
idx_obs1 = find(x1 >= x_obs1, 1);         % Index im x-Vektor, der am nächsten dran ist am Messort

% Dispersionsmatrix M1 (implizit)
M1 = spdiags(ones(nx1,1)*[-dt1*D1/dx^2, 1+2*dt1*D1/dx^2, -dt1*D1/dx^2], -1:1, nx1, nx1);

% obere Randbedingung
M1(1,1) = 1; 
M1(1,2) = 0;     
% untere Randbedingung
M1(end,end) = 1;
M1(end,end-1) = 0; 

%% Interpolationen Strahlung

% Modellzeitachse relativ
t_rel1 = seconds(t_L1 - t_L1(1));          % Zeit in Sekunden relativ zum ersten Messpunkt

% Strahlungsdaten zeitlich relativ
t0 = t_R(1);
t_R_rel1 = seconds(t_R - t0);               % Strahlungszeitpunkte relativ zu t0

%  t_mod1 auf dieselbe Basis wie t_R_rel bringen
t_mod_rel3 = t_mod1 + seconds(t_L1(1) - t0);  % Modellzeiten relativ zu t0

% Interpolation
R_in1 = interp1(t_R_rel1, R_1, t_mod_rel3, 'linear', 'extrap');

%% Interpolationsfunktionen für c und T
c_in1 = @(t) interp1(t_rel1, c_L1, t, 'linear', 'extrap');
T_in1 = @(t) interp1(t_rel1, T_L1, t, 'linear', 'extrap');

%% Parameterfit

% [r_zehr, Smax_photo, k2, R05] MM
p0_MM1 = [2.27e-4, 1.05e-5, 3.23e-4, 173];          % Startwerte
lb_MM1 = [0, 0, 0, 0];                              % untere Grenzen (nicht negativ)
ub_MM1 = [3e-3, 1e-2, 0.1, 10000];                   % obere Grenzen

% [r_zehr, k_photo, k2] linear
p0_lin1 = [2.27e-4, 7.3e-6,  3.23e-4];              % Startwerte
lb_lin1 = [0, 0, 0];                                % untere Grenzen (nicht negativ)
ub_lin1 = [3e-3, 2e-5, 0.1];                        % obere Grenzen

t_fit1 = seconds(t_L2 - t_L1(1));     % relative Zeit für L3-Daten
c_fit1 = c_L2;                        % gemessene Konzentration an L3

% am Anfang Daten verwerfen
tau1 = L1/v1;                         % Fließzeit
mask1 = t_fit1 > tau1*1.5;            % Nehme nur Daten ab 1.5mal der Fließzeit, weil Daten am Anfang noch vom Anfangszustand beeinflusst sind
t_fit1 = t_fit1(mask1);
c_fit1 = c_fit1(mask1);

% Modellfunktionen zum Fitten
modelfun_MM1  = @(p, t_out) Modell_MM( p, t_out, nx1, dt1, t_mod1, nt1, idx_obs1, c_in1, T_in1, R_in1, M1);
modelfun_lin1 = @(p, t_out) Modell_lin(p, t_out, nx1, dt1, t_mod1, nt1, idx_obs1, c_in1, T_in1, R_in1, M1);

%% Fit Michaelis-Menten (4 Parameter)
[p_fit_MM1, resnorm_MM1, res_MM1, ~, ~, ~, J_MM1] = lsqcurvefit(modelfun_MM1, p0_MM1, t_fit1, c_fit1, lb_MM1, ub_MM1);

% Fehleranalyse
fprintf('Modell 1: Summe der Fehlerquadrate (SSE/resnorm) MM1 = %e\n', resnorm_MM1);

n_data_MM1   = length(c_fit1);                             % Anzahl Datenpunkte
n_params_MM1 = length(p_fit_MM1);                          % Anzahl Parameter
var_c_MM1    = resnorm_MM1 / (n_data_MM1 - n_params_MM1);  % Varianz der Residuen
Cpp_MM1      = full(inv(J_MM1' * J_MM1)) * var_c_MM1;      % Kovarianzmatrix der Parameter

% Standardabweichungen der Parameter
r_zehr_stabw_MM1      = sqrt(Cpp_MM1(1,1));
Smax_photo_stabw_MM1  = sqrt(Cpp_MM1(2,2));
k2_stabw_MM1          = sqrt(Cpp_MM1(3,3));
R05_stabw_MM1         = sqrt(Cpp_MM1(4,4));

RMSE_MM1 = sqrt(var_c_MM1);
fprintf('RMSE (Standardabweichung des Modells) MM1 = %8.3f mg/l\n', RMSE_MM1);

fprintf('\nGefundene Parameter MM1 und Unsicherheiten:\n');
fprintf('r_zehr     = %.3e +- %.3e [1/s]\n', p_fit_MM1(1), r_zehr_stabw_MM1);
fprintf('Smax_photo = %.3e +- %.3e [m^2/(W*s)]\n', p_fit_MM1(2), Smax_photo_stabw_MM1);
fprintf('k2         = %.3e +- %.3e [1/s]\n', p_fit_MM1(3), k2_stabw_MM1);
fprintf('R05        = %.3e +- %.3e []\n', p_fit_MM1(4), R05_stabw_MM1);

% Korrealtionskoeffizienten
cor_r_zehr_Smax_MM1 = Cpp_MM1(1,2) / (r_zehr_stabw_MM1 * Smax_photo_stabw_MM1);
cor_r_zehr_k2_MM1   = Cpp_MM1(1,3) / (r_zehr_stabw_MM1 * k2_stabw_MM1);
cor_r_zehr_R05_MM1  = Cpp_MM1(1,4) / (r_zehr_stabw_MM1 * R05_stabw_MM1);
cor_Smax_k2_MM1     = Cpp_MM1(2,3) / (Smax_photo_stabw_MM1 * k2_stabw_MM1);
cor_Smax_R05_MM1    = Cpp_MM1(2,4) / (Smax_photo_stabw_MM1 * R05_stabw_MM1);
cor_k2_R05_MM1      = Cpp_MM1(3,4) / (k2_stabw_MM1 * R05_stabw_MM1);

fprintf('\nKorrelationskoeffizienten MM1:\n');
fprintf('Corr(r_zehr, Smax_photo) = %.3f\n', cor_r_zehr_Smax_MM1);
fprintf('Corr(r_zehr, k2)         = %.3f\n', cor_r_zehr_k2_MM1);
fprintf('Corr(r_zehr, R05)        = %.3f\n', cor_r_zehr_R05_MM1);
fprintf('Corr(Smax_photo, k2)     = %.3f\n', cor_Smax_k2_MM1);
fprintf('Corr(Smax_photo, R05)    = %.3f\n', cor_Smax_R05_MM1);
fprintf('Corr(k2, R05)            = %.3f\n', cor_k2_R05_MM1);

%% Fit Lineares Modell (3 Parameter)
[p_fit_lin1, resnorm_lin1, res_lin1, ~, ~, ~, J_lin1] = lsqcurvefit(modelfun_lin1, p0_lin1, t_fit1, c_fit1, lb_lin1, ub_lin1);

fprintf('Summe der Fehlerquadrate (SSE/resnorm) linear1 = %e\n', resnorm_lin1);

% Fehleranalyse
n_data_lin1   = length(c_fit1);
n_params_lin1 = length(p_fit_lin1);
var_c_lin1    = resnorm_lin1 / (n_data_lin1 - n_params_lin1);
Cpp_lin1      = full(inv(J_lin1' * J_lin1)) * var_c_lin1;

% Standardabweichungen der Parameter
r_zehr_stabw_lin1     = sqrt(Cpp_lin1(1,1));
k_photo_stabw_lin1    = sqrt(Cpp_lin1(2,2));
k2_stabw_lin1         = sqrt(Cpp_lin1(3,3));

RMSE_lin1 = sqrt(var_c_lin1);
fprintf('RMSE (Standardabweichung des Modells) linear1 = %8.3f mg/l\n', RMSE_lin1);

fprintf('\nGefundene Parameter linear1 und Unsicherheiten:\n');
fprintf('r_zehr  = %.3e +- %.3e [1/s]\n', p_fit_lin1(1), r_zehr_stabw_lin1);
fprintf('k_photo = %.3e +- %.3e [m^2/(W*s)]\n', p_fit_lin1(2), k_photo_stabw_lin1);
fprintf('k2      = %.3e +- %.3e [1/s]\n', p_fit_lin1(3), k2_stabw_lin1);

% Korrealtionskoeffizienten
cor_r_zehr_k_photo_lin1 = Cpp_lin1(1,2) / (r_zehr_stabw_lin1 * k_photo_stabw_lin1);
cor_r_zehr_k2_lin1      = Cpp_lin1(1,3) / (r_zehr_stabw_lin1 * k2_stabw_lin1);
cor_k_photo_k2_lin1     = Cpp_lin1(2,3) / (k_photo_stabw_lin1 * k2_stabw_lin1);

fprintf('\nKorrelationskoeffizienten linear1:\n');
fprintf('Corr(r_zehr, k_photo) = %.3f\n', cor_r_zehr_k_photo_lin1);
fprintf('Corr(r_zehr, k2)      = %.3f\n', cor_r_zehr_k2_lin1);
fprintf('Corr(k_photo, k2)     = %.3f\n', cor_k_photo_k2_lin1);

%% Modellrechnung 
dt_mod1 = t_L1(1) + seconds(t_fit1);

% Modellkurven berechnen
BTC_MM1  = modelfun_MM1(p_fit_MM1, t_fit1);
BTC_lin1 = modelfun_lin1(p_fit_lin1, t_fit1);

%% Konfidenz- und Vorhersageintervall linear

% Varianz aus Parametern (Sensitivitäten * Cpp * Sensitivitäten^T)
var_paramlin1 = diag(J_lin1* Cpp_lin1 * J_lin1');  

% 95% Konfidenzintervall (nur Parameterunsicherheit)
conflin1 = 1.96 * sqrt(var_paramlin1);

% 95% Vorhersageintervall (Parameterunsicherheit + Messunsicherheit)
predlin1 = 1.96 * sqrt(var_paramlin1 + var_c_lin1);

% Intervallgrenzen
CI_lowerlin1 = BTC_lin1- conflin1;
CI_upperlin1 = BTC_lin1 + conflin1;
PI_lowerlin1 = BTC_lin1- predlin1;
PI_upperlin1 = BTC_lin1+ predlin1;

%% Konfidenz- und Vorhersageintervall MM1

% Varianz aus Parametern (Sensitivitäten * Cpp * Sensitivitäten^T)
var_paramMM1 = diag(J_MM1* Cpp_MM1 * J_MM1');  

% 95% Konfidenzintervall (nur Parameterunsicherheit)
confMM1 = 1.96 * sqrt(var_paramMM1);

% 95% Vorhersageintervall (Parameterunsicherheit + Messunsicherheit)
predMM1 = 1.96 * sqrt(var_paramMM1 + var_c_MM1);

% Intervallgrenzen
CI_lowerMM1 = BTC_MM1- confMM1;
CI_upperMM1 = BTC_MM1 + confMM1;
PI_lowerMM1 = BTC_MM1 - predMM1;
PI_upperMM1 = BTC_MM1 + predMM1;



%% Modell 2 (Abschnitt M2-M3)
                
%% Modellparameter & Zeit

L2 = 1713.874+50;       % Flusslänge [m] (50m länger als Messabschnitt 1-2)
x2 = (0:dx:L2)';        % Ortsvektor von 0 bis L1 in 10 m Schritten
nx2 = length(x2);       % Anzahl der Gitterpunkte

v2 = 0.3;             % Fließgeschwindigkeit [m/s]
dt2 = dx/v2;          % Zeitschritt [s]
D2 = 4.8;             % Dispersionskoeffizient [m²/s]

t_end2 = seconds(t_L3(end) - t_L2(1)) + dt2;      % Modellzeitdauer in Sekunden (dt, damit das Zeitgitter auch den Endzeitpunkt enthält)
t_mod2 = (0:dt2:t_end2)';                         % Zeitvektor im Modell
nt2 = length(t_mod2) - 1;                         % Anzahl der Zeitschritte (-1, weil von einem Zeitpunkt zum nächsten)

x_obs2 = 1713.874;                        % Position des Messpunkts
idx_obs2 = find(x2 >= x_obs2, 1);         % Index im x-Vektor, der am nächsten dran ist am Messort

% Dispersionsmatrix M2 (implizit)
M2 = spdiags(ones(nx2,1)*[-dt2*D2/dx^2, 1+2*dt2*D2/dx^2, -dt2*D2/dx^2], -1:1, nx2, nx2);

% obere Randbedingung
M2(1,1) = 1; 
M2(1,2) = 0;      
% untere Randbedingung
M2(end,end) = 1; 
M2(end,end-1) = 0; 


%% Interpolationen Strahlung

% Modellzeitachse relativ
t_rel2 = seconds(t_L2 - t_L2(1));          % Zeit in Sekunden relativ zum ersten Messpunkt
t0 = t_R(1);
t_R_rel2 = seconds(t_R - t0);

%  t_mod1 auf dieselbe Basis wie t_R_rel bringen
t_mod_rel3 = t_mod2 + seconds(t_L2(1) - t0);  % Modellzeiten relativ zu t0

% Interpolation
R_in2 = interp1(t_R_rel2, R_2, t_mod_rel3, 'linear', 'extrap');

%% Interpolationsfunktionen für c und T
c_in2 = @(t) interp1(t_rel2, c_L2, t, 'linear', 'extrap');
T_in2 = @(t) interp1(t_rel2, T_L2, t, 'linear', 'extrap');

%% 2. Parameterfit

% [r_zehr, Smax_photo, k2, R05] MM
p0_MM2 = [2.31e-4, 1.1e-5, 3.61e-4, 77];       % Startwerte
lb_MM2 = [0, 0, 0, 0];                         % untere Grenzen (nicht negativ)
ub_MM2 = [3e-3, 1e-2, 0.1, 10000];             % obere Grenzen

% [r_zehr, k_photo, k2] linear
p0_lin2 = [2.31e-4, 2.119e-6, 3.61e-4];          % Startwerte (geschätzt)
lb_lin2 = [0, 0, 0];                             % untere Grenzen (nicht negativ)
ub_lin2 = [1e-3, 1e-4, 1e-2];                    % obere Grenzen

t_fit2 = seconds(t_L3 - t_L2(1));    % relative Zeit für L3-Daten
c_fit2 = c_L3;                       % gemessene Konzentration unten

% am Anfang Daten verwerfen
tau2 = L2/v2;
mask2 = t_fit2 > tau2*1.5;            % Nehme nur Daten ab 1.5mal der Fließzeit
t_fit2 = t_fit2(mask2);
c_fit2 = c_fit2(mask2);

% Modellfunktionen zum Fitten
modelfun_MM2  = @(p, t_out) Modell_MM(p,  t_out, nx2, dt2, t_mod2, nt2, idx_obs2, c_in2, T_in2, R_in2, M2);
modelfun_lin2 = @(p, t_out) Modell_lin(p, t_out, nx2, dt2, t_mod2, nt2, idx_obs2, c_in2, T_in2, R_in2, M2);

%% 3. Fit Michaelis-Menten (4 Parameter)
[p_fit_MM2, resnorm_MM2, res_MM2, ~, ~, ~, J_MM2] = lsqcurvefit(modelfun_MM2, p0_MM2, t_fit2, c_fit2, lb_MM2, ub_MM2);

% Fehleranalyse
fprintf('Modell 2: Summe der Fehlerquadrate (SSE/resnorm) MM2 = %e\n', resnorm_MM2);

n_data_MM2 = length(c_fit2);                           
n_params_MM2 = length(p_fit_MM2);                      
var_c_MM2 = resnorm_MM2 / (n_data_MM2 - n_params_MM2);   
Cpp_MM2 = full(inv(J_MM2' * J_MM2)) * var_c_MM2;         

% Standardabweichungen der Parameter
r_zehr_stabw_MM2      = sqrt(Cpp_MM2(1,1));
Smax_photo_stabw_MM2  = sqrt(Cpp_MM2(2,2));
k2_stabw_MM2          = sqrt(Cpp_MM2(3,3));
R05_stabw_MM2         = sqrt(Cpp_MM2(4,4));

RMSE_MM2 = sqrt(var_c_MM2);
fprintf('RMSE (Standardabweichung des Modells) MM2 = %8.3f mg/l\n', RMSE_MM2);

fprintf('\nGefundene Parameter MM2 und Unsicherheiten:\n');
fprintf('r_zehr     = %.3e +- %.3e [1/s]\n', p_fit_MM2(1), r_zehr_stabw_MM2);
fprintf('Smax_photo = %.3e +- %.3e [m^2/(W*s)]\n', p_fit_MM2(2), Smax_photo_stabw_MM2);
fprintf('k2         = %.3e +- %.3e [1/s]\n', p_fit_MM2(3), k2_stabw_MM2);
fprintf('R05        = %.3e +- %.3e []\n', p_fit_MM2(4), R05_stabw_MM2);

% Korrelationen
cor_r_zehr_Smax_MM2 = Cpp_MM2(1,2) / (r_zehr_stabw_MM2 * Smax_photo_stabw_MM2);
cor_r_zehr_k2_MM2   = Cpp_MM2(1,3) / (r_zehr_stabw_MM2 * k2_stabw_MM2);
cor_r_zehr_R05_MM2  = Cpp_MM2(1,4) / (r_zehr_stabw_MM2 * R05_stabw_MM2);
cor_Smax_k2_MM2     = Cpp_MM2(2,3) / (Smax_photo_stabw_MM2 * k2_stabw_MM2);
cor_Smax_R05_MM2    = Cpp_MM2(2,4) / (Smax_photo_stabw_MM2 * R05_stabw_MM2);
cor_k2_R05_MM2      = Cpp_MM2(3,4) / (k2_stabw_MM2 * R05_stabw_MM2);

fprintf('\nKorrelationskoeffizienten MM2:\n');
fprintf('Corr(r_zehr, Smax_photo) = %.3f\n', cor_r_zehr_Smax_MM2);
fprintf('Corr(r_zehr, k2)         = %.3f\n', cor_r_zehr_k2_MM2);
fprintf('Corr(r_zehr, R05)        = %.3f\n', cor_r_zehr_R05_MM2);
fprintf('Corr(Smax_photo, k2)     = %.3f\n', cor_Smax_k2_MM2);
fprintf('Corr(Smax_photo, R05)    = %.3f\n', cor_Smax_R05_MM2);
fprintf('Corr(k2, R05)            = %.3f\n', cor_k2_R05_MM2);

%% 4. Fit Lineares Modell (3 Parameter)
[p_fit_lin2, resnorm_lin2, res_lin2, ~, ~, ~, J_lin2] = lsqcurvefit(modelfun_lin2, p0_lin2, t_fit2, c_fit2, lb_lin2, ub_lin2);

fprintf('Summe der Fehlerquadrate (SSE/resnorm) linear2 = %e\n', resnorm_lin2);

% Fehleranalyse
n_data_lin2 = length(c_fit2);
n_params_lin2 = length(p_fit_lin2);
var_c_lin2 = resnorm_lin2 / (n_data_lin2 - n_params_lin2);
Cpp_lin2 = full(inv(J_lin2' * J_lin2)) * var_c_lin2;

% Standardabweichungen der Parameter
r_zehr_stabw_lin2   = sqrt(Cpp_lin2(1,1));
k_photo_stabw_lin2  = sqrt(Cpp_lin2(2,2));
k2_stabw_lin2       = sqrt(Cpp_lin2(3,3));

RMSE_lin2 = sqrt(var_c_lin2);
fprintf('RMSE (Standardabweichung des Modells) linear2 = %8.3f mg/l\n', RMSE_lin2);

% Korrelationen
cor_r_zehr_k_photo_lin2 = Cpp_lin2(1,2) / (r_zehr_stabw_lin2 * k_photo_stabw_lin2);
cor_r_zehr_k2_lin2      = Cpp_lin2(1,3) / (r_zehr_stabw_lin2 * k2_stabw_lin2);
cor_k_photo_k2_lin2     = Cpp_lin2(2,3) / (k_photo_stabw_lin2 * k2_stabw_lin2);

fprintf('\nGefundene Parameter linear2 und Unsicherheiten:\n');
fprintf('r_zehr  = %.3e +- %.3e [1/s]\n', p_fit_lin2(1), r_zehr_stabw_lin2);
fprintf('k_photo = %.3e +- %.3e [m^2/(W*s)]\n', p_fit_lin2(2), k_photo_stabw_lin2);
fprintf('k2      = %.3e +- %.3e [1/s]\n', p_fit_lin2(3), k2_stabw_lin2);

fprintf('\nKorrelationskoeffizienten linear2:\n');
fprintf('Corr(r_zehr, k_photo) = %.3f\n', cor_r_zehr_k_photo_lin2);
fprintf('Corr(r_zehr, k2)      = %.3f\n', cor_r_zehr_k2_lin2);
fprintf('Corr(k_photo, k2)     = %.3f\n', cor_k_photo_k2_lin2);

%% Modellrechnung 
dt_mod2 = t_L2(1) + seconds(t_fit2);

% Modellkurven berechnen
BTC_MM2  = modelfun_MM2(p_fit_MM2, t_fit2);
BTC_lin2 = modelfun_lin2(p_fit_lin2, t_fit2);

%% Konfidenz- und Vorhersageintervall linear

% Varianz aus Parametern (Sensitivitäten * Cpp * Sensitivitäten^T)
var_paramlin2 = diag(J_lin2* Cpp_lin2 * J_lin2');  

% 95% Konfidenzintervall (nur Parameterunsicherheit)
conflin2 = 1.96 * sqrt(var_paramlin2);

% 95% Vorhersageintervall (Parameterunsicherheit + Messunsicherheit)
predlin2 = 1.96 * sqrt(var_paramlin2 + var_c_lin2);

% Intervallgrenzen
CI_lowerlin2 = BTC_lin2- conflin2;
CI_upperlin2 = BTC_lin2 + conflin2;
PI_lowerlin2 = BTC_lin2- predlin2;
PI_upperlin2 = BTC_lin2+ predlin2;

%% Konfidenz- und Vorhersageintervall MM

% Varianz aus Parametern (Sensitivitäten * Cpp * Sensitivitäten^T)
var_paramMM2 = diag(J_MM2* Cpp_MM2 * J_MM2');  

% 95% Konfidenzintervall (nur Parameterunsicherheit)
confMM2 = 1.96 * sqrt(var_paramMM2);

% 95% Vorhersageintervall (Parameterunsicherheit + Messunsicherheit)
predMM2 = 1.96 * sqrt(var_paramMM2 + var_c_MM2);

% Intervallgrenzen
CI_lowerMM2 = BTC_MM2- confMM2;
CI_upperMM2 = BTC_MM2 + confMM2;
PI_lowerMM2 = BTC_MM2 - predMM2;
PI_upperMM2 = BTC_MM2 + predMM2;



%% Modell 3 (Abschnitt M3-M4)               

%% Modellparameter & Zeit

L3 = 994.916+50;     % Flusslänge [m] (50m länger als Messabschnitt 3-4)
x3 = (0:dx:L3)';     % Ortsvektor
nx3 = length(x3);

v3 = 0.304;         % Fließgeschwindigkeit [m/s]
dt3 = dx/v3;        % Zeitschritt [s]
D3 = 1.86;          % Dispersionskoeffizient [m²/s]

t_end3 = seconds(t_L4(end) - t_L3G(1)) + dt3;     % Modellzeitdauer
t_mod3 = (0:dt3:t_end3)';                         % Zeitvektor im Modell
nt3 = length(t_mod3) - 1;                         % Anzahl der Zeitschritte

x_obs3 = 994.916;                         % Position des Messpunkts
idx_obs3 = find(x3 >= x_obs3, 1);         % Index im x-Vektor, der am nächsten dran ist

% Dispersionsmatrix M3 (implizit)
M3 = spdiags(ones(nx3,1)*[-dt3*D3/dx^2, 1+2*dt3*D3/dx^2, -dt3*D3/dx^2], -1:1, nx3, nx3);

% obere Randbedingung
M3(1,1) = 1; 
M3(1,2) = 0;      
% untere Randbedingung
M3(end,end) = 1; 
M3(end,end-1) = 0; 

%% Interpolation Strahlung

% Modellzeitachse relativ
t_rel3 = seconds(t_L3G - t_L3G(1));

% Zeitinterpolation 
t0 = t_R(1); 
t_R_rel3 = seconds(t_R - t0);

%  t_mod3 auf dieselbe Basis wie t_R_rel bringen
t_mod_rel3 = t_mod3 + seconds(t_L3G(1) - t0);  % Modellzeiten relativ zu t0

% Interpolation
R_in3 = interp1(t_R_rel3, R_3, t_mod_rel3, 'linear', 'extrap');

%% Interpolationsfunktionen c und T

c_in3 = @(t) interp1(t_rel3, c_L3G, t, 'linear', 'extrap');
T_in3 = @(t) interp1(t_rel3, T_L3G, t, 'linear', 'extrap');                         

%% Parameterfit

% [r_zehr, Smax_photo, k2, R05] MM
p0_MM3 = [2.27e-4, 1.42e-5, 3.12e-4, 175];       % Startwerte
lb_MM3 = [0, 0, 0, 0];                           % untere Grenzen (nicht negativ)
ub_MM3 = [3e-3, 1e-2, 0.1, 10000];               % obere Grenzen

% [r_zehr, k_photo, k2] linear
p0_lin3 = [2.27e-4, 7.3e-6, 3.12e-4];            % Startwerte
lb_lin3 = [0, 2e-9, 0];                           % untere Grenzen (nicht negativ)
ub_lin3 = [1e-3, 2e-5, 0.05];                     % obere Grenzen
                        
t_fit3 = seconds(t_L4 - t_L3G(1));    % relative Zeit für L4-Daten
c_fit3 = c_L4;                        % gemessene Konzentration unten

% am Anfang Daten verwerfen
tau3 = L3/v3;
mask3 = t_fit3 > tau3*1.5;            
t_fit3 = t_fit3(mask3);
c_fit3 = c_fit3(mask3);

% Modellfunktionen zum Fitten
modelfun_MM3  = @(p, t_out) Modell_MM(p,  t_out, nx3, dt3, t_mod3, nt3, idx_obs3, c_in3, T_in3, R_in3, M3);
modelfun_lin3 = @(p, t_out) Modell_lin(p, t_out, nx3, dt3, t_mod3, nt3, idx_obs3, c_in3, T_in3, R_in3, M3);

%% Fit Michaelis-Menten (4 Parameter)
[p_fit_MM3, resnorm_MM3, res_MM3, ~, ~, ~, J_MM3] = lsqcurvefit(modelfun_MM3, p0_MM3, t_fit3, c_fit3, lb_MM3, ub_MM3);

% Fehleranalyse
fprintf('Modell 3: Summe der Fehlerquadrate (SSE/resnorm) MM3 = %e\n', resnorm_MM3);

n_data_MM3   = length(c_fit3);
n_params_MM3 = length(p_fit_MM3);
var_c_MM3    = resnorm_MM3 / (n_data_MM3 - n_params_MM3);
Cpp_MM3      = full(inv(J_MM3' * J_MM3)) * var_c_MM3;

% Standardabweichungen der Parameter
r_zehr_stabw_MM3      = sqrt(Cpp_MM3(1,1));
Smax_photo_stabw_MM3  = sqrt(Cpp_MM3(2,2));
k2_stabw_MM3          = sqrt(Cpp_MM3(3,3));
R05_stabw_MM3         = sqrt(Cpp_MM3(4,4));

RMSE_MM3 = sqrt(var_c_MM3);
fprintf('RMSE (Standardabweichung des Modells) MM3 = %8.3f mg/l\n', RMSE_MM3);

fprintf('\nGefundene Parameter MM3 und Unsicherheiten:\n');
fprintf('r_zehr     = %.3e +- %.3e [1/s]\n', p_fit_MM3(1), r_zehr_stabw_MM3);
fprintf('Smax_photo = %.3e +- %.3e [m^2/(W*s)]\n', p_fit_MM3(2), Smax_photo_stabw_MM3);
fprintf('k2         = %.3e +- %.3e [1/s]\n', p_fit_MM3(3), k2_stabw_MM3);
fprintf('R05        = %.3e +- %.3e []\n', p_fit_MM3(4), R05_stabw_MM3);

% Korrelationen
cor_r_zehr_Smax_MM3 = Cpp_MM3(1,2) / (r_zehr_stabw_MM3 * Smax_photo_stabw_MM3);
cor_r_zehr_k2_MM3   = Cpp_MM3(1,3) / (r_zehr_stabw_MM3 * k2_stabw_MM3);
cor_r_zehr_R05_MM3  = Cpp_MM3(1,4) / (r_zehr_stabw_MM3 * R05_stabw_MM3);
cor_Smax_k2_MM3     = Cpp_MM3(2,3) / (Smax_photo_stabw_MM3 * k2_stabw_MM3);
cor_Smax_R05_MM3    = Cpp_MM3(2,4) / (Smax_photo_stabw_MM3 * R05_stabw_MM3);
cor_k2_R05_MM3      = Cpp_MM3(3,4) / (k2_stabw_MM3 * R05_stabw_MM3);

fprintf('\nKorrelationskoeffizienten MM3:\n');
fprintf('Corr(r_zehr, Smax_photo) = %.3f\n', cor_r_zehr_Smax_MM3);
fprintf('Corr(r_zehr, k2)         = %.3f\n', cor_r_zehr_k2_MM3);
fprintf('Corr(r_zehr, R05)        = %.3f\n', cor_r_zehr_R05_MM3);
fprintf('Corr(Smax_photo, k2)     = %.3f\n', cor_Smax_k2_MM3);
fprintf('Corr(Smax_photo, R05)    = %.3f\n', cor_Smax_R05_MM3);
fprintf('Corr(k2, R05)            = %.3f\n', cor_k2_R05_MM3);

%% Fit Lineares Modell (3 Parameter)
[p_fit_lin3, resnorm_lin3, res_lin3, ~, ~, ~, J_lin3] = lsqcurvefit(modelfun_lin3, p0_lin3, t_fit3, c_fit3, lb_lin3, ub_lin3);

fprintf('Summe der Fehlerquadrate (SSE/resnorm) linear3 = %e\n', resnorm_lin3);

% Fehleranalyse
n_data_lin3   = length(c_fit3);
n_params_lin3 = length(p_fit_lin3);
var_c_lin3    = resnorm_lin3 / (n_data_lin3 - n_params_lin3);
Cpp_lin3      = full(inv(J_lin3' * J_lin3)) * var_c_lin3;

% Standardabweichungen der Parameter
r_zehr_stabw_lin3   = sqrt(Cpp_lin3(1,1));
k_photo_stabw_lin3  = sqrt(Cpp_lin3(2,2));
k2_stabw_lin3       = sqrt(Cpp_lin3(3,3));

RMSE_lin3 = sqrt(var_c_lin3);
fprintf('RMSE (Standardabweichung des Modells) linear3 = %8.3f mg/l\n', RMSE_lin3);

fprintf('\nGefundene Parameter linear3 und Unsicherheiten:\n');
fprintf('r_zehr  = %.3e +- %.3e [1/s]\n', p_fit_lin3(1), r_zehr_stabw_lin3);
fprintf('k_photo = %.3e +- %.3e [m^2/(W*s)]\n', p_fit_lin3(2), k_photo_stabw_lin3);
fprintf('k2      = %.3e +- %.3e [1/s]\n', p_fit_lin3(3), k2_stabw_lin3);

% Korrelationen
cor_r_zehr_k_photo_lin3 = Cpp_lin3(1,2) / (r_zehr_stabw_lin3 * k_photo_stabw_lin3);
cor_r_zehr_k2_lin3      = Cpp_lin3(1,3) / (r_zehr_stabw_lin3 * k2_stabw_lin3);
cor_k_photo_k2_lin3     = Cpp_lin3(2,3) / (k_photo_stabw_lin3 * k2_stabw_lin3);

fprintf('\nKorrelationskoeffizienten linear3:\n');
fprintf('Corr(r_zehr, k_photo) = %.3f\n', cor_r_zehr_k_photo_lin3);
fprintf('Corr(r_zehr, k2)      = %.3f\n', cor_r_zehr_k2_lin3);
fprintf('Corr(k_photo, k2)     = %.3f\n', cor_k_photo_k2_lin3);

%% Modellrechnung 
dt_mod3 = t_L3G(1) + seconds(t_fit3);

% Modellkurven berechnen
BTC_MM3  = modelfun_MM3(p_fit_MM3, t_fit3);
BTC_lin3 = modelfun_lin3(p_fit_lin3, t_fit3);

%% Konfidenz- und Vorhersageintervall linear3

% Varianz aus Parametern (Sensitivitäten * Cpp * Sensitivitäten^T)
var_paramlin3 = diag(J_lin3* Cpp_lin3 * J_lin3');  

% 95% Konfidenzintervall (nur Parameterunsicherheit)
conflin3 = 1.96 * sqrt(var_paramlin3);

% 95% Vorhersageintervall (Parameterunsicherheit + Messunsicherheit)
predlin3 = 1.96 * sqrt(var_paramlin3 + var_c_lin3);

% Intervallgrenzen
CI_lowerlin3 = BTC_lin3 - conflin3;
CI_upperlin3 = BTC_lin3 + conflin3;
PI_lowerlin3 = BTC_lin3 - predlin3;
PI_upperlin3 = BTC_lin3 + predlin3;

%% Konfidenz- und Vorhersageintervall MM3

% Varianz aus Parametern (Sensitivitäten * Cpp * Sensitivitäten^T)
var_paramMM3 = diag(J_MM3* Cpp_MM3 * J_MM3');  

% 95% Konfidenzintervall (nur Parameterunsicherheit)
confMM3 = 1.96 * sqrt(var_paramMM3);

% 95% Vorhersageintervall (Parameterunsicherheit + Messunsicherheit)
predMM3 = 1.96 * sqrt(var_paramMM3 + var_c_MM3);

% Intervallgrenzen
CI_lowerMM3 = BTC_MM3 - confMM3;
CI_upperMM3 = BTC_MM3 + confMM3;
PI_lowerMM3 = BTC_MM3 - predMM3;
PI_upperMM3 = BTC_MM3 + predMM3;


%% Lineare Plots (einstellen ob zwei oder vier Tages Zeitraum)

figure;
tiledlayout(1,3); % 1 Zeilen, 3 Spalten
sgtitle('Lineare Modellberechnung über die einzelnen Abschnitte')

% Modell M1-M2
nexttile(1);
step = 5;  % jeden 5. Punkt anzeigen
h1 = plot(t_L2(1:step:end), c_L2(1:step:end), 'k.','DisplayName','Messwerte','MarkerSize',4);    % Messwerte
hold on;
h2 = plot(dt_mod1, BTC_lin1,'Color', [0 0.5 1] ,'DisplayName','Linear','LineWidth',1);           % Modellkurve
% Konfidenzintervall
h3 = fill([dt_mod1; flipud(dt_mod1)], [CI_lowerlin1; flipud(CI_upperlin1)], ...
         [0.3 0.7 1], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
h4 = fill([dt_mod1; flipud(dt_mod1)],[PI_lowerlin1; flipud(PI_upperlin1)], ...
          [0.3 0.7 1], 'FaceAlpha',0.2, 'EdgeColor','none','DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Abschnitt M1-M2');
grid on;

% Modell M2-M3
nexttile(2);
step =5;  % jeden 5. Punkt anzeigen
plot(t_L3(1:step:end), c_L3(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);      % Messwerte
hold on;
plot(dt_mod2, BTC_lin2,'Color', [0 0.5 1] , 'DisplayName','Linear','LineWidth',1);             % Modellkurve
% Konfidenzintervall
fill([dt_mod2; flipud(dt_mod2)],[CI_lowerlin2; flipud(CI_upperlin2)], ...
     [0.3 0.7 1], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
fill([dt_mod2; flipud(dt_mod2)], [PI_lowerlin2; flipud(PI_upperlin2)], ...
     [0.3 0.7 1], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Abschnitt M2-M3');
grid on;

% Modell M3-M4
nexttile(3);
step = 5; 
plot(t_L4(1:step:end), c_L4(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);     % Messwerte
hold on;
plot(dt_mod3, BTC_lin3,'Color', [0 0.5 1] , 'DisplayName','Linear','LineWidth',1);            % Modellkurve
% Konfidenzintervall
fill([dt_mod3; flipud(dt_mod3)], [CI_lowerlin3; flipud(CI_upperlin3)], ...
     [0.3 0.7 1], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
fill([dt_mod3; flipud(dt_mod3)], [PI_lowerlin3; flipud(PI_upperlin3)], ...
     [0.3 0.7 1], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Abschnitt M3-M4');
grid on;

% Legende
legend([h1 h2 h3 h4], ...
    {'Messwerte','Linear','95% Konfidenzintervall','95% Vorhersageintervall'}, ...
    'Location','northoutside','Orientation','horizontal');
lg1.Layout.Tile = 'north';

% Für Gesamtplot einmal mit zwei tage und einmal mit vier Tage laufen lassen und wie folgt abspeichern
% saveas(gcf, 'lin_zwei_tage.fig');   
% saveas(gcf, 'lin_vier_tage.fig');


%% MM Plots (einstellen ob zwei oder vier Tages Zeitraum)

figure;
tiledlayout(1,3); % 1 Zeilen, 3 Spalten
sgtitle('MM Modellberechnung über die einzelnen Abschnitte')

% Modell M1-M2
nexttile(1);
step = 5;  % jeden 5. Punkt anzeigen
h1 = plot(t_L2(1:step:end), c_L2(1:step:end), 'k.','DisplayName','Messwerte','MarkerSize',4);    % Messwerte
hold on;
h2 = plot(dt_mod1, BTC_MM1,'Color', [1 0.4 0.3] ,'DisplayName','Linear','LineWidth',1);           % Modellkurve
% Konfidenzintervall
h3 = fill([dt_mod1; flipud(dt_mod1)], [CI_lowerMM1; flipud(CI_upperMM1)], ...
         [1 0.6 0.6], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
h4 = fill([dt_mod1; flipud(dt_mod1)],[PI_lowerMM1; flipud(PI_upperMM1)], ...
          [1 0.6 0.6], 'FaceAlpha',0.2, 'EdgeColor','none','DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Abschnitt M1-M2');
grid on;

% Modell M2-M3
nexttile(2);
step =5;  % jeden 5. Punkt anzeigen
plot(t_L3(1:step:end), c_L3(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);      % Messwerte
hold on;
plot(dt_mod2, BTC_MM2,'Color', [1 0.4 0.3] , 'DisplayName','Linear','LineWidth',1);             % Modellkurve
% Konfidenzintervall
fill([dt_mod2; flipud(dt_mod2)],[CI_lowerMM2; flipud(CI_upperMM2)], ...
     [1 0.6 0.6], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
fill([dt_mod2; flipud(dt_mod2)], [PI_lowerMM2; flipud(PI_upperMM2)], ...
     [1 0.6 0.6], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Abschnitt M2-M3');
grid on;

% Modell M3-M4
nexttile(3);
step = 5; 
plot(t_L4(1:step:end), c_L4(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);     % Messwerte
hold on;
plot(dt_mod3, BTC_MM3,'Color', [1 0.4 0.3] , 'DisplayName','Linear','LineWidth',1);            % Modellkurve
% Konfidenzintervall
fill([dt_mod3; flipud(dt_mod3)], [CI_lowerMM3; flipud(CI_upperMM3)], ...
     [1 0.6 0.6], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
fill([dt_mod3; flipud(dt_mod3)], [PI_lowerMM3; flipud(PI_upperMM3)], ...
     [1 0.6 0.6], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Abschnitt M3-M4');
grid on;

% Legende
legend([h1 h2 h3 h4], ...
    {'Messwerte','Linear','95% Konfidenzintervall','95% Vorhersageintervall'}, ...
    'Location','northoutside','Orientation','horizontal');
lg1.Layout.Tile = 'north';

% Für Gesamtplot einmal mit zwei tage und einmal mit vier Tage laufen lassen und wie folgt abspeichern
% saveas(gcf, 'MM_zwei_tage.fig');   
% saveas(gcf, 'MM_vier_tage.fig');


%% Lineare und Michaelis-Menten Plots 

figure;
tiledlayout(2,3); % 2 Zeilen, 3 Spalten

nexttile(1);
step = 5;  % jeden 5. Punkt anzeigen
% Messwerte
h1 = plot(t_L2(1:step:end), c_L2(1:step:end), 'k.','DisplayName','Messwerte','MarkerSize',4); 
hold on;
% Modellkurve
h2 = plot(dt_mod1, BTC_lin1,'Color', [0 0.5 1] ,'DisplayName','Linear','LineWidth',1);
% Konfidenzintervall
h3 = fill([dt_mod1; flipud(dt_mod1)], [CI_lowerlin1; flipud(CI_upperlin1)], ...
         [0.3 0.7 1], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
h4 = fill([dt_mod1; flipud(dt_mod1)],[PI_lowerlin1; flipud(PI_upperlin1)], ...
          [0.3 0.7 1], 'FaceAlpha',0.2, 'EdgeColor','none','DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Modellberechnung linear M1-M2');
grid on;

nexttile(2);
step =5; 
plot(t_L3(1:step:end), c_L3(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);
hold on;
plot(dt_mod2, BTC_lin2,'Color', [0 0.5 1] , 'DisplayName','Linear','LineWidth',1);
% Konfidenzintervall
fill([dt_mod2; flipud(dt_mod2)],[CI_lowerlin2; flipud(CI_upperlin2)], ...
     [0.3 0.7 1], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
fill([dt_mod2; flipud(dt_mod2)], [PI_lowerlin2; flipud(PI_upperlin2)], ...
     [0.3 0.7 1], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Modellberechnung linear M2-M3');
grid on;

nexttile(3);
step = 5;  
plot(t_L4(1:step:end), c_L4(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);
hold on;
plot(dt_mod3, BTC_lin3,'Color', [0 0.5 1] , 'DisplayName','Linear','LineWidth',1);
% Konfidenzintervall
fill([dt_mod3; flipud(dt_mod3)], [CI_lowerlin3; flipud(CI_upperlin3)], ...
     [0.3 0.7 1], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
fill([dt_mod3; flipud(dt_mod3)], [PI_lowerlin3; flipud(PI_upperlin3)], ...
     [0.3 0.7 1], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Modellberechnung linear M3-M4');
grid on;

% Legende für die erste Zeile
lgd = legend([h1 h2 h3 h4], ...
    {'Messwerte','Linear','95% Konfidenzintervall','95% Vorhersageintervall'}, ...
    'Location','northoutside', 'Orientation','horizontal');
% Position 
pos = lgd.Position;         % aktuelle Position
pos(1) = pos(1) + 0.5;      % nach rechts verschieben
pos(2) = pos(2) + 0.05;     % etwas nach oben
lgd.Position = pos;


nexttile(4);
step = 5;  
h1 = plot(t_L2(1:step:end), c_L2(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);
hold on;
h2 = plot(dt_mod1, BTC_MM1, 'Color',[1 0.4 0.3],'DisplayName','Michaelis-Menten','LineWidth',1);
% Konfidenzintervall
h3 = fill([dt_mod1; flipud(dt_mod1)], [CI_lowerMM1; flipud(CI_upperMM1)], ...
          [1 0.6 0.6], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
h4 = fill([dt_mod1; flipud(dt_mod1)], [PI_lowerMM1; flipud(PI_upperMM1)], ...
          [1 0.6 0.6], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Modellberechnung Michaelis-Menten M1-M2');
grid on;

nexttile(5);
step =5; 
plot(t_L3(1:step:end), c_L3(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);
hold on;
plot(dt_mod2, BTC_MM2,'Color', [1 0.4 0.3] , 'DisplayName','Michaelis-Menten','LineWidth',1);
% Konfidenzintervall
fill([dt_mod2; flipud(dt_mod2)],[CI_lowerMM2; flipud(CI_upperMM2)], ...
     [1 0.6 0.6], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
fill([dt_mod2; flipud(dt_mod2)], [PI_lowerMM2; flipud(PI_upperMM2)], ...
     [1 0.6 0.6], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Modellberechnung Michaelis-Menten M2-M3');
grid on;

nexttile(6);
step = 5;  
plot(t_L4(1:step:end), c_L4(1:step:end), 'k.', 'DisplayName','Messwerte','MarkerSize',4);
hold on;
plot(dt_mod3, BTC_MM3,'Color', [1 0.4 0.3] , 'DisplayName','Michaelis-Menten','LineWidth',1);
% Konfidenzintervall
fill([dt_mod3; flipud(dt_mod3)], [CI_lowerMM3; flipud(CI_upperMM3)], ...
     [1 0.6 0.6], 'FaceAlpha',0.8, 'EdgeColor','none', 'DisplayName','95% Konfidenzintervall');
% Vorhersageintervall
fill([dt_mod3; flipud(dt_mod3)], [PI_lowerMM3; flipud(PI_upperMM3)], ...
     [1 0.6 0.6], 'FaceAlpha',0.2, 'EdgeColor','none', 'DisplayName','95% Vorhersageintervall');
xlabel('Datum'); 
ylabel('Konzentration [mg/L]');
title('Modellberechnung Michaelis-Menten M3-M4');
grid on;

% Legende für die zweite Zeile
lgd = legend([h1 h2 h3 h4], ...
    {'Messwerte','Linear','95% Konfidenzintervall','95% Vorhersageintervall'}, ...
    'Location','northoutside', 'Orientation','horizontal');
% Position
pos = lgd.Position;            % aktuelle Position
pos(1) = pos(1) + 0.5;         % nach rechts verschieben
pos(2) = pos(2) + 0.015;       % etwas nach oben
lgd.Position = pos;



%% Modell Michaelis-Menten

function c_out = Modell_MM(p,t_out,nx,dt,t_mod,nt,idx_obs,c_in,T_in,R_in,M)
   
    % Parameter entpacken
    r_zehr = p(1); 
    Smax_photo = p(2); 
    k2 = p(3);
    R05 = p(4);

    % Initialisierung
    c = zeros(nx, 1);
    c_sim = zeros(nt+1, 1);

    for it = 1:nt
        t = t_mod(it);

        % Advektion (explizit)
        c(2:end) = c(1:end-1);
        c(1) = c_in(t);

        % Dispersion (implizit)
        c = M \ c;

        T = T_in(t);
        R_obs = R_in(it);   

        c_sat = 468 / (31.6 + T);  

        % Lineare Zehrung
        zehr = r_zehr;

        % Michaelis-Menten Strahlung
        photo = Smax_photo * (R_obs / (R_obs + R05));
        
        % Halbschritt in der Reaktion
        % Reaktionsrate 
        r_tot = -zehr + photo + k2 * (c_sat - c);
        c = c + 0.5* r_tot*dt ;

        r_tot = -zehr + photo + k2 * (c_sat - c);
        c = c + 0.5* r_tot*dt ;

        % Speichern
        c_sim(it+1) = c(idx_obs);
    end
    
    % Ausgabe
    c_out = interp1(t_mod, c_sim, t_out, 'linear', NaN);
end

%% Modell linear

function c_out = Modell_lin(p,t_out,nx,dt,t_mod,nt,idx_obs,c_in,T_in,R_in,M)
     
    % Parameter entpacken
    r_zehr = p(1); 
    k_photo = p(2); 
    k2 = p(3);
    
    % Initialisierung
    c = zeros(nx, 1);
    c_sim = zeros(nt+1, 1);

    for it = 1:nt
        t = t_mod(it);

        % Advektion (explizit)
        c(2:end) = c(1:end-1);
        c(1) = c_in(t);

        % Dispersion (implizit)
        c = M \ c;

        T = T_in(t);
        R_obs = R_in(it);  
        
        c_sat = 468 / (31.6 + T);

        % Lineare Zehrung
        zehr = r_zehr;

        % Lineare Strahlung
        photo = k_photo * R_obs;

        % Halbschritt in der Reaktion
        % Reaktionsrate
        r_tot = -zehr + photo + k2 * (c_sat - c);
        c = c + 0.5 * r_tot * dt;

        r_tot = -zehr + photo + k2 * (c_sat - c);
        c = c + 0.5 * r_tot * dt;

        % speichern
        c_sim(it+1) = c(idx_obs);
    end
    % Ausgabe
    c_out = interp1(t_mod, c_sim, t_out, 'linear', NaN);
end



%% Figuren zusammenfügen Linear
% in der ZIP sind die figuren schon abgespeichert, dann müsste es laufen

fig1 = openfig('lin_zwei_tage.fig','invisible');
fig2 = openfig('lin_vier_tage.fig','invisible');

ax1 = findall(fig1,'Type','axes');
ax2 = findall(fig2,'Type','axes');
ax1 = flipud(ax1);   % Reihenfolge korrigieren
ax2 = flipud(ax2);

% Tiledlayout: 2x3
newFig = figure;
tl = tiledlayout(newFig,2,3);

sgtitle('Lineare Modellberechnung über die einzelnen Abschnitte');

% Erste Zeile Plots
for k = 1:numel(ax1)
    dstAx = nexttile(tl,k);
    newAx = copyobj(ax1(k), newFig);
    set(newAx,'Position',get(dstAx,'Position')); % Position merken
    delete(dstAx);
end

% Zweite Zeile Plots
for k = 1:numel(ax2)
    dstAx = nexttile(tl,3+k);
    newAx = copyobj(ax2(k), newFig);
    set(newAx,'Position',get(dstAx,'Position'));
    delete(dstAx);
end

% Gemeinsame Legende zwischen den Zeilen
lgdAx = axes('Position',[0.05 0.48 0.9 0.04],'Visible','off');  % Zwischenraum
h1 = findobj(ax1(1), 'DisplayName','Messwerte');
h2 = findobj(ax1(1), 'DisplayName','Linear');
h3 = findobj(ax1(1), 'DisplayName','95% Konfidenzintervall');
h4 = findobj(ax1(1), 'DisplayName','95% Vorhersageintervall');

lgd = legend(lgdAx,[h1 h2 h3 h4], ...
    {'Messwerte','Linear','95% Konfidenzintervall','95% Vorhersageintervall'},'Orientation','horizontal');
set(lgd,'Units','normalized'); 
set(lgd,'Position',[0 0 1 1]);


%% Figuren zusammenfügen MM
% in der ZIP sind die figuren schon abgespeichert, dann müsste es laufen

fig1 = openfig('MM_zwei_tage.fig','invisible');
fig2 = openfig('MM_vier_tage.fig','invisible');

ax1 = findall(fig1,'Type','axes');
ax2 = findall(fig2,'Type','axes');
ax1 = flipud(ax1);   % Reihenfolge korrigieren
ax2 = flipud(ax2);

% Tiledlayout: 2x3
newFig = figure;
tl = tiledlayout(newFig,2,3);

sgtitle('MM Modellberechnung über die einzelnen Abschnitte');

% Erste Zeile Plots
for k = 1:numel(ax1)
    dstAx = nexttile(tl,k);
    newAx = copyobj(ax1(k), newFig);
    set(newAx,'Position',get(dstAx,'Position')); % Position merken
    delete(dstAx);
end

% Zweite Zeile Plots
for k = 1:numel(ax2)
    dstAx = nexttile(tl,3+k);
    newAx = copyobj(ax2(k), newFig);
    set(newAx,'Position',get(dstAx,'Position'));
    delete(dstAx);
end

% Gemeinsame Legende zwischen den Zeilen
lgdAx = axes('Position',[0.05 0.48 0.9 0.04],'Visible','off');  % Zwischenraum
h1 = findobj(ax1(1), 'DisplayName','Messwerte');
h2 = findobj(ax1(1), 'DisplayName','Linear');
h3 = findobj(ax1(1), 'DisplayName','95% Konfidenzintervall');
h4 = findobj(ax1(1), 'DisplayName','95% Vorhersageintervall');

lgd = legend(lgdAx,[h1 h2 h3 h4], ...
    {'Messwerte','Linear','95% Konfidenzintervall','95% Vorhersageintervall'},'Orientation','horizontal');
set(lgd,'Units','normalized'); 
set(lgd,'Position',[0 0 1 1]);