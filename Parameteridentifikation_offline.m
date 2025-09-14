clear all

%% Variablen zur Steuerung 
% Parameter zum veraendern:
Rauschen = 0;                           % 1 fuer Rauschen, 0 ohne Rauschen
Eingangssignal = 1;                     % 1 = Sprung
                                        % 2 = Sinus
                                        % 3 = PRBS
T_filter = 10;                          % Filterkonstante ZVF

% Generierung der Messdaten
PT3_Generiere_Messdaten_offline;       

                                       

%% Parameteridentifikation allgemein Arbeitspunkt/Ruhelage (Kleinsignalverhalten)!
% 1. Arbeitspunkt abziehen
y = y_mess - y_e;
u = u_mess - u_e;


%% Variante 1: 
%% 3. Ableitung ist auf der linken Seite und Schaetzen aller Parameter [K, T1, T2, T3]

Ergebnis_Ordnung_3_Ableitung_links = table;
Ergebnis_Ordnung_3_Ableitung_links.Parameter = {'K'; 'T1'; 'T2'; 'T3'};
Ergebnis_Ordnung_3_Ableitung_links.Originale_Werte = [K; T1; T2; T3];

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0])
% Problem: Anfangswert des Systems muss Null sein. Wenn Experiment nicht aus Ruhelage, dann Fehler 

% Zustandsvariablenfilter (ZVF) initialisieren. Wird hier ueber eine separate Funktion "zvf" gemacht.
[ZVFdu, ZVFdy] = zvf(3, T_filter, T_A, Eingangssignal);

% ZVF anwenden
y_f = lsim(ZVFdy,y,t,[0; 0; 0; 0]);
u_f = lsim(ZVFdu,u,t,[0; 0; 0; 0]);

% Gefilterte Signale fuer Least-Squares nutzen
y_N = y_f(:,4);                                             % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) -y_f(:,3) u_f(:,1)];             % Datenmatrix
theta = pinv(S_N)*y_N;                                      % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T3_est = 1 / theta(1);               % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(3) * T3_est;          % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T3_est;          % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(4) * T3_est;           % Geschaetzte Verstaerkung K

Ergebnis_Ordnung_3_Ableitung_links.GF_ohne_AW = [K_est; T1_est; T2_est; T3_est];

%Simulation Kleinsignalverhalten mit ermittelten Parametern
y1 = Ergebnis_Simulation([K_est], [T1_est, T2_est, T3_est], [0;0;0], t, u);


%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 MIT Anfangswertschaetzung x_0 = [y_0; dy_0; ddy_0]
% Fuer Schaetzung Anfangswerte
eins_f = lsim(ZVFdu,ones(size(y)),t,[0; 0; 0; 0]);

% Gefilterete Signale fuer Least-Squares nutzen
y_N = y_f(:,4);                                                                         % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) -y_f(:,3) u_f(:,1) eins_f(:,2) eins_f(:,3) eins_f(:,4)];     % Datenmatrix                
theta = pinv(S_N)*y_N;                                                                  % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T3_est = 1 / theta(1);                                                      % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(3) * T3_est;                                                 % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T3_est;                                                 % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(4) * T3_est;                                                  % Geschaetzte Verstaerkung K
y_0_est = theta(7);                                                         % Geschaetzter Anfangswert y
dy_0_est = theta(6) - y_0_est*T2_est/T3_est;                                % Geschaetzter Anfangswert dy
ddy_0_est = theta(5) - y_0_est*T1_est/T3_est - dy_0_est*T2_est/T3_est;      % Geschaetzter Anfangswert ddy

Ergebnis_Ordnung_3_Ableitung_links.GF_mit_AW = [K_est; T1_est; T2_est; T3_est];
y2 = Ergebnis_Simulation([K_est], [T1_est, T2_est, T3_est], [y_0_est; dy_0_est; ddy_0_est], t, u); 
y_0_est 
dy_0_est 
ddy_0_est

%% Parameteridentifikation ueber Ausgangsfehlerminimierung
% Zur Vereinfachung wird nachfolgend nur die Erregung aus einer Ruhelage [y_0, 0, 0] betrachtet.
% Damit muss nur der Anfangswert y_0 geschätzt werden.
% Separate Funktion implementieren, die zu einem gegebenen Parametersatz theta den
% Fehler zwischen Modell und Messung zurueckliefert:


%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0])
theta_0 = [15, 120, 55, 30]; % [K, T1 T2 T3] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT3_Model_Error, theta_0);
Ergebnis_Ordnung_3_Ableitung_links.AF_ohne_AW = [theta_opt(1); theta_opt(2); theta_opt(3); theta_opt(4)];
y3 = Ergebnis_Simulation([theta_opt(1)], theta_opt(2:4), [0;0;0], t, u); 


%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich MIT Anfangswertschaetzung Annahme x_0 = [y_0; 0; 0]
theta_0 = [15, 120, 55, 30, 0.15]; % [K, T1 T2 T3, y_0] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT3_Model_Error_x0, theta_0);
Ergebnis_Ordnung_3_Ableitung_links.AF_mit_AW = [theta_opt(1); theta_opt(2); theta_opt(3); theta_opt(4)];
y4 = Ergebnis_Simulation([theta_opt(1)], theta_opt(2:4), [theta_opt(5); 0; 0], t, u); 
  
Ergebnis_Ordnung_3_Ableitung_links
Visualisierung(t, [y_mess-y_e, y1, y2, y3, y4], 'Modell 3. Ordnung, hoechste Ableitung ist auf linker Seite');
theta_opt





%% Variante 2: 
%% 0. Ableitung (y) ist auf der linken Seite und Schaetzen aller Parameter [K, T1, T2, T3]

Ergebnis_Ordnung_3_y_links = table;
Ergebnis_Ordnung_3_y_links.Parameter = {'K'; 'T1'; 'T2'; 'T3'};
Ergebnis_Ordnung_3_y_links.Originale_Werte = [K; T1; T2; T3];

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0])

% Gefilterte Signale fuer Least-Squares nutzen
y_N = y_f(:,1);                                             % Messvektor 
S_N = [-y_f(:,2) -y_f(:,3) -y_f(:,4) u_f(:,1)];             % Datenmatrix
theta = pinv(S_N)*y_N;                                      % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T3_est = theta(3);                   % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(2);                   % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(1);                   % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(4);                    % Geschaetzte Verstaerkung K

Ergebnis_Ordnung_3_y_links.GF_ohne_AW = [K_est; T1_est; T2_est; T3_est];
y1 = Ergebnis_Simulation([K_est], [T1_est, T2_est, T3_est], [0;0;0], t, u);

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 MIT Anfangswertschaetzung
% Fuer Schaetzung Anfangswerte
eins_f = lsim(ZVFdu,ones(size(y)),t,[0; 0; 0; 0]);

% Gefilterete Signale fuer Least-Squares nutzen
y_N = y_f(:,1);                                                                         % Messvektor 
S_N = [-y_f(:,2) -y_f(:,3) -y_f(:,4) u_f(:,1) eins_f(:,2) eins_f(:,3) eins_f(:,4)];     % Datenmatrix                
theta = pinv(S_N)*y_N;                                                                  % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T3_est = theta(3);                                                          % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(2);                                                          % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(1);                                                          % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(4);                                                           % Geschaetzte Verstaerkung K
y_0_est = theta(7)/T3_est;                                                  % Geschaetzter Anfangswert y
dy_0_est = (theta(6) - y_0_est*T2_est) / T3_est;                            % Geschaetzter Anfangswert dy
ddy_0_est = (theta(5) - y_0_est*T1_est - dy_0_est*T2_est) / T3_est;         % Geschaetzter Anfangswert ddy

Ergebnis_Ordnung_3_y_links.GF_mit_AW = [K_est; T1_est; T2_est; T3_est];
y2 = Ergebnis_Simulation([K_est], [T1_est, T2_est, T3_est], [y_0_est; dy_0_est; ddy_0_est], t, u); 
  
Ergebnis_Ordnung_3_y_links
Visualisierung(t, [y_mess, y1, y2], 'Modell 3. Ordnung, y ist auf linker Seite');





%% Variante 3: 
%% 0. Ableitung (y) ist auf der linken Seite und der Parameter K ist bekannt; Schaetzen aller anderen Parameter Parameter [T1, T2, T3]

Ergebnis_Ordnung_3_K_bekannt = table;
Ergebnis_Ordnung_3_K_bekannt.Parameter = {'K'; 'T1'; 'T2'; 'T3'};
Ergebnis_Ordnung_3_K_bekannt.Originale_Werte = [K; T1; T2; T3];

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0])

% Gefilterte Signale fuer Least-Squares nutzen
y_N = y_f(:,1) - K*u_f(:,1);                                % Messvektor 
S_N = [-y_f(:,2) -y_f(:,3) -y_f(:,4)];                      % Datenmatrix
theta = pinv(S_N)*y_N;                                      % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T3_est = theta(3);                   % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(2);                   % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(1);                   % Geschaetzte Strecken-Zeitkonstante T1

Ergebnis_Ordnung_3_K_bekannt.GF_ohne_AW = [K; T1_est; T2_est; T3_est];
y1 = Ergebnis_Simulation([K], [T1_est, T2_est, T3_est], [0;0;0], t, u);

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 MIT Anfangswertschaetzung

% Fuer Schaetzung Anfangswert y_0
eins_f = lsim(ZVFdu,ones(size(y)),t,[0; 0; 0; 0]);

% Gefilterete Signale fuer Least-Squares nutzen
y_N = y_f(:,1) - K*u_f(:,1);                                                                         % Messvektor 
S_N = [-y_f(:,2) -y_f(:,3) -y_f(:,4) eins_f(:,2) eins_f(:,3) eins_f(:,4)];     % Datenmatrix                
theta = pinv(S_N)*y_N;                                                                  % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T3_est = theta(3);                                                          % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(2);                                                          % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(1);                                                          % Geschaetzte Strecken-Zeitkonstante T1
y_0_est = theta(6)/T3_est;                                                  % Geschaetzter Anfangswert y
dy_0_est = (theta(5) - y_0_est*T2_est) / T3_est;                            % Geschaetzter Anfangswert dy
ddy_0_est = (theta(4) - y_0_est*T1_est - dy_0_est*T2_est) / T3_est;         % Geschaetzter Anfangswert ddy

Ergebnis_Ordnung_3_K_bekannt.GF_mit_AW = [K; T1_est; T2_est; T3_est];
y2 = Ergebnis_Simulation([K], [T1_est, T2_est, T3_est], [y_0_est; dy_0_est; ddy_0_est], t, u); 


%% Parameteridentifikation ueber Ausgangsfehlerminimierung
% Separate Funktion implementieren, die zu einem gegebenen Parametersatz theta den
% Fehler zwischen Modell und Messung zurueckliefert:

%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0])
theta_0 = [120, 55, 30]; % [T1 T2 T3] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT3_Model_Error_K, theta_0);
Ergebnis_Ordnung_3_K_bekannt.AF_ohne_AW = [K; theta_opt(1); theta_opt(2); theta_opt(3)];
y3 = Ergebnis_Simulation(K, theta_opt(1:3), [0;0;0], t, u);

%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich MIT Anfangswertschaetzung (Annahme x_0 = [y_0;0;0])
theta_0 = [120, 55, 30, 0.15]; % [K, T1 T2 T3, y_0] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT3_Model_Error_K_x0, theta_0);
Ergebnis_Ordnung_3_K_bekannt.AF_mit_AW = [K; theta_opt(1); theta_opt(2); theta_opt(3)];
y4 = Ergebnis_Simulation(K, theta_opt(1:3), [theta_opt(4);0;0], t, u);
  
Ergebnis_Ordnung_3_K_bekannt
Visualisierung(t, [y, y1, y2, y3, y4], 'Modell 3. Ordnung, K ist bekannt');




%% Variante 4: Aufgabe 1 b
%% Falsches Modell (2. Ordnung)
% T2*d^2y/dt^2 + T1*dy/dt + y = K*u
Ergebnis_Ordnung_2 = table;
Ergebnis_Ordnung_2.Parameter = {'K'; 'T1'; 'T2'};
Ergebnis_Ordnung_2.Originale_Werte = [K; T1; T2];
%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT2 OHNE Anfangswertschaetzung (Annahme x_0 = [0;0])
% Problem: Anfangswert des Systems muss Null sein. Wenn Experiment nicht aus Ruhelage, dann Fehler 

% Zustandsvariablenfilter (ZVF) initialisieren. Wird hier ueber eine Funktion "zvf" gemacht.
[ZVFdu, ZVFdy] = zvf(2, T_filter, T_A, Eingangssignal);

% ZVF anwenden
y_f = lsim(ZVFdy,y,t,[0; 0; 0]);
u_f = lsim(ZVFdu,u,t,[0; 0; 0]);

% Gefilterte Signale fuer Least-Squares nutzen
y_N = y_f(:,3);                                             % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) u_f(:,1)];                       % Datenmatrix
theta = pinv(S_N)*y_N;                                      % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T2_est = 1 / theta(1);               % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T2_est;          % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(3) * T2_est;           % Geschaetzte Verstaerkung K

Ergebnis_Ordnung_2.GF_ohne_AW = [K_est; T1_est; T2_est];
y1 = Ergebnis_Simulation([K_est], [T1_est, T2_est], [0;0], t, u);

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT2 MIT Anfangswertschaetzung

% Fuer Schaetzung Anfangswert y_0
eins_f = lsim(ZVFdu,ones(size(y)),t,[0; 0; 0]);

% Gefilterete Signale fuer Least-Squares nutzen
y_N = y_f(:,3);                                                                         % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) u_f(:,1) eins_f(:,2) eins_f(:,3)];                           % Datenmatrix                
theta = pinv(S_N)*y_N;                                                                  % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T2_est = 1 / theta(1);                                                      % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T2_est;                                                 % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(3) * T2_est;                                                  % Geschaetzte Verstaerkung K
y_0_est = theta(5);                                                         % Geschaetzter Anfangswert y
dy_0_est = theta(4) - y_0_est*T1_est/T2_est;                                % Geschaetzter Anfangswert dy

Ergebnis_Ordnung_2.GF_mit_AW = [K_est; T1_est; T2_est];
y2 = Ergebnis_Simulation([K_est], [T1_est, T2_est], [y_0_est; dy_0_est], t, u); 

%% Parameteridentifikation ueber Ausgangsfehlerminimierung
% Separate Funktion implementieren, die zu einem gegebenen Parametersatz theta den
% Fehler zwischen Modell und Messung zurueckliefert:


%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich OHNE Anfansgwertschaetzung (Annahme x_0 = [0;0])
theta_0 = [15, 140, 55]; % [K, T1 T2] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT2_Model_Error, theta_0);
Ergebnis_Ordnung_2.AF_ohne_AW = [theta_opt(1); theta_opt(2); theta_opt(3)];
y3 = Ergebnis_Simulation([theta_opt(1)], theta_opt(2:3), [0;0], t, u);

%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich OHNE Anfansgwertschaetzung (Annahme x_0 = [y_0;0])
theta_0 = [15, 140, 55, 0.15]; % [K, T1 T2, y_0] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT2_Model_Error_x0, theta_0);
Ergebnis_Ordnung_2.AF_mit_AW = [theta_opt(1); theta_opt(2); theta_opt(3)];
y4 = Ergebnis_Simulation([theta_opt(1)], theta_opt(2:3), [theta_opt(4);0], t, u);  


Ergebnis_Ordnung_2
Visualisierung(t, [y_mess, y1, y2, y3, y4], 'Modell 2. Ordnung')







%% Variante 5: Aufgabe 1 c
%% Falsches Modell (4. Ordnung)
% T4*d^4/dty^4 + T3 d^3y/d4^3+ T2 d^2y/dt^2 + T1*dy/dt + y = K*u
Ergebnis_Ordnung_4 = table;
Ergebnis_Ordnung_4.Parameter = {'K'; 'T1'; 'T2'; 'T3'; 'T4'};
Ergebnis_Ordnung_4.Originale_Werte = [K; T1; T2; T3; NaN];

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT4 OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0;0])
% Problem: Anfangswert des Systems muss Null sein. Wenn Experiment nicht aus Ruhelage, dann Fehler

% Zustandsvariablenfilter (ZVF) initialisieren. Wird hier ueber eine Funktion "zvf" gemacht.
[ZVFdu, ZVFdy] = zvf(4, T_filter, T_A, Eingangssignal);

% ZVF anwenden
y_f = lsim(ZVFdy,y,t,[0; 0; 0; 0; 0]);
u_f = lsim(ZVFdu,u,t,[0; 0; 0; 0; 0]);

% Gefilterte Signale fuer Least-Squares nutzen
y_N = y_f(:,5);                                             % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) -y_f(:,3) -y_f(:,4) u_f(:,1)];   % Datenmatrix
theta = pinv(S_N)*y_N;                                      % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T4_est = 1 / theta(1);               % Geschaetzte Strecken-Zeitkonstante T4
T3_est = theta(4) * T4_est;          % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(3) * T4_est;          % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T4_est;          % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(5) * T4_est;           % Geschaetzte Verstaerkung K

Ergebnis_Ordnung_4.GF_ohne_AW = [K_est; T1_est; T2_est; T3_est; T4_est];
y1 = Ergebnis_Simulation([K_est], [T1_est, T2_est, T3_est, T4_est], [0; 0; 0; 0], t, u);

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT4 MIT Anfangswertschaetzung

% Fuer Schaetzung Anfangswert y_0
eins_f = lsim(ZVFdu,ones(size(y)),t,[0; 0; 0; 0; 0]);

% Gefilterete Signale fuer Least-Squares nutzen
y_N = y_f(:,5);                                                                                             % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) -y_f(:,3) -y_f(:,4) u_f(:,1) eins_f(:,2) eins_f(:,3) eins_f(:,4) eins_f(:,5)];   % Datenmatrix                
theta = pinv(S_N)*y_N;                                                                                      % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T4_est = 1 / theta(1);                                                      % Geschaetzte Strecken-Zeitkonstante T3
T3_est = theta(4) * T4_est;                                                 % Geschaetzte Strecken-Zeitkonstante T2
T2_est = theta(3) * T4_est;                                                 % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T4_est;                                                 % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(5) * T4_est;                                                  % Geschaetzte Verstaerkung K
y_0_est = theta(9);                                                         % Geschaetzter Anfangswert y
dy_0_est = theta(8) - y_0_est*T3_est/T4_est;                                % Geschaetzter Anfangswert dy
ddy_0_est = theta(7) - y_0_est*T2_est/T4_est - dy_0_est*T3_est/T4_est;      % Geschaetzter Anfangswert ddy
dddy_0_est = theta(6) - y_0_est*T1_est/T4_est - dy_0_est*T2_est/T4_est...   % Geschaetzter Anfangswert dddy
        - ddy_0_est*T3_est/T4_est;                                      
    
Ergebnis_Ordnung_4.GF_mit_AW = [K_est; T1_est; T2_est; T3_est; T4_est];
y2 = Ergebnis_Simulation([K_est], [T1_est, T2_est, T3_est, T4_est], [y_0_est; dy_0_est; ddy_0_est; dddy_0_est], t, u); 

%% Parameteridentifikation ueber Ausgangsfehlerminimierung
% Separate Funktion implementieren, die zu einem gegebenen Parametersatz theta den
% Fehler zwischen Modell und Messung zurueckliefert:



%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich OHNE Anfangswertschaetzung (Annahme x_0 = [0; 0; 0; 0])
theta_0 = [15, 140, 55, 30, 40]; % [K, T1 T2 T3 T4] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT4_Model_Error, theta_0);
Ergebnis_Ordnung_4.AF_ohne_AW = [theta_opt(1); theta_opt(2); theta_opt(3); theta_opt(4); theta_opt(5)];
y3 = Ergebnis_Simulation([theta_opt(1)], theta_opt(2:5), [0; 0; 0; 0], t, u);


%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich MIT Anfangswertschaetzung (Annahme x_0 = [y_0; 0; 0; 0])
theta_0 = [15, 140, 55, 30, 40, 0.15]; % [K, T1 T2 T3 T4, y_0] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT4_Model_Error_x0, theta_0);
Ergebnis_Ordnung_4.AF_mit_AW = [theta_opt(1); theta_opt(2); theta_opt(3); theta_opt(4); theta_opt(5)];
  
Ergebnis_Ordnung_4
Visualisierung(t, [y_mess, y1, y2, y3], 'Modell 4. Ordnung');



%% ************************************************************************************************
%% Ab hier nicht mehr alle Teile vollständig, da keine neue Information. Gleiches Prinzip wie oben!
%% ************************************************************************************************


%% Variante 6: 
%% Falsches Modell (3. Ordnung mit zusaetzlicher Ableitung des Eingangs auf rechter Seite)
% T3 d^3y/dt^3 + T2 d^2y/dt^2 + T1*dy/dt + y = K*(u + b1*du/dt) 

Ergebnis_Ordnung_3_mit_Ableitung_u = table;
Ergebnis_Ordnung_3_mit_Ableitung_u.Parameter = {'K'; 'b1'; 'T1'; 'T2'; 'T3'};
Ergebnis_Ordnung_3_mit_Ableitung_u.Originale_Werte = [K; NaN; T1; T2; T3];

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 OHNE Anfangswertschaetzung
% Problem: Anfangswert des Systems muss Null sein. Wenn Experiment nicht aus Ruhelage, dann Fehler

% Zustandsvariablenfilter (ZVF) initialisieren. Wird hier ueber eine Funktion "zvf" gemacht.
[ZVFdu, ZVFdy] = zvf(3, T_filter, T_A, Eingangssignal);

% ZVF anwenden
y_f = lsim(ZVFdy,y,t,[0; 0; 0; 0]);
u_f = lsim(ZVFdu,u,t,[0; 0; 0; 0]);

% Gefilterte Signale fuer Least-Squares nutzen
y_N = y_f(:,4);                                             % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) -y_f(:,3) u_f(:,1) u_f(:,2)];    % Datenmatrix
theta = pinv(S_N)*y_N;                                      % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T3_est = 1 / theta(1);               % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(3) * T3_est;          % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T3_est;          % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(4) * T3_est;           % Geschaetzte Verstaerkung K
b1_est = theta(5) * T3_est/K_est;    % Geschaetzte Verstaerlung b1

Ergebnis_Ordnung_3_mit_Ableitung_u.GF_ohne_AW = [K_est; b1_est; T1_est; T2_est; T3_est];
y1 = Ergebnis_Simulation([K_est, b1_est], [T1_est, T2_est, T3_est], [0;0;0], t, u);

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 MIT Anfangswertschaetzung

% Fuer Schaetzung Anfangswert y_0
eins_f = lsim(ZVFdu,ones(size(y)),t,[0; 0; 0; 0]);

% Gefilterete Signale fuer Least-Squares nutzen
y_N = y_f(:,4);                                                                                 % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) -y_f(:,3) u_f(:,1) u_f(:,2) eins_f(:,2) eins_f(:,3) eins_f(:,4)];    % Datenmatrix                
theta = pinv(S_N)*y_N;                                                                          % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T3_est = 1 / theta(1);                                                      % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(3) * T3_est;                                                 % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T3_est;                                                 % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(4) * T3_est;                                                  % Geschaetzte Verstaerkung K
b1_est = theta(5) * T3_est/K_est;                                           % Geschaetzte Verstaerkung b1
y_0_est = theta(8);                                                         % Geschaetzter Anfangswert y
dy_0_est = theta(7) - y_0_est*T2_est/T3_est;                                % Geschaetzter Anfangswert dy
ddy_0_est = theta(6) - y_0_est*T1_est/T3_est - dy_0_est*T2_est/T3_est;      % Geschaetzter Anfangswert ddy

Ergebnis_Ordnung_3_mit_Ableitung_u.GF_mit_AW = [K_est; b1_est; T1_est; T2_est; T3_est];
y2 = Ergebnis_Simulation([K_est, b1_est], [T1_est, T2_est, T3_est], [y_0_est; dy_0_est; ddy_0_est], t, u); 


%% Parameteridentifikation ueber Ausgangsfehlerminimierung
% Separate Funktion implementieren, die zu einem gegebenen Parametersatz theta den
% Fehler zwischen Modell und Messung zurueckliefert:

%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0])
theta_0 = [15, 10, 140, 55, 30]; % [K, b1, T1 T2 T3] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
theta_opt = fminsearch(@PT3u_Model_Error, theta_0);
Ergebnis_Ordnung_3_mit_Ableitung_u.AF_ohne_AW = [theta_opt(1); theta_opt(2); theta_opt(3); theta_opt(4); theta_opt(5)];
y3 = Ergebnis_Simulation([theta_opt(1:2)], theta_opt(3:5), [0;0;0], t, u);

%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich MIT Anfangswertschaetzung (Annahme x_0 = [y_0;0;0])
%theta_0 = [15, 10, 140, 55, 30, 0.15]; % [K, b1, T1 T2 T3, y_0] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
%theta_opt = fminsearch(@PT3_Model_Error_x0, [theta_0, 7]);
%Ergebnis_6.Ausgangsfehlerbasiert_mit_Anfangswert = [theta_opt(1); theta_opt(2); theta_opt(3); theta_opt(4)];
  
Ergebnis_Ordnung_3_mit_Ableitung_u
Visualisierung(t, [y_mess, y1, y2, y3], 'Modell 3. Ordnung mit Ableitung von u auf rechter Seite');






%% Variante 7: Falsches Modell (4. Ordnung mit zusaetzlicher Ableitung des Eingangs auf rechter Seite)
% T4 d^4/dty^4 + T3 d^3y/dt^3 + T2 d^2y/dt^2 + T1*dy/dt + y = K*(u + b1*du/dt)  
Ergebnis_Ordnung_4_mit_Ableitung_u = table;
Ergebnis_Ordnung_4_mit_Ableitung_u.Parameter = {'K'; 'b1'; 'T1'; 'T2'; 'T3'; 'T4'};
Ergebnis_Ordnung_4_mit_Ableitung_u.Originale_Werte = [K; NaN; T1; T2; T3; NaN];
%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT4 OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0;0])
% Problem: Anfangswert des Systems muss Null sein. Wenn Experiment nicht aus Ruhelage, dann Fehler

% Zustandsvariablenfilter (ZVF) initialisieren. Wird hier ueber eine Funktion "zvf" gemacht.
[ZVFdu, ZVFdy] = zvf(4, T_filter, T_A, Eingangssignal);

% ZVF anwenden
y_f = lsim(ZVFdy,y,t,[0; 0; 0; 0; 0]);
u_f = lsim(ZVFdu,u,t,[0; 0; 0; 0; 0]);

% Gefilterte Signale fuer Least-Squares nutzen
y_N = y_f(:,5);                                                         % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) -y_f(:,3) -y_f(:,4) u_f(:,1) u_f(:,2)];      % Datenmatrix
theta = pinv(S_N)*y_N;                                                  % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T4_est = 1 / theta(1);               % Geschaetzte Strecken-Zeitkonstante T4
T3_est = theta(4) * T4_est;          % Geschaetzte Strecken-Zeitkonstante T3
T2_est = theta(3) * T4_est;          % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T4_est;          % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(5) * T4_est;           % Geschaetzte Verstaerkung K
b1_est = theta(6) * T4_est/K_est;    % Geschaetzte Verstaerkung b1

Ergebnis_Ordnung_4_mit_Ableitung_u.GF_ohne_AW = [K_est; b1_est; T1_est; T2_est; T3_est; T4_est];
y1 = Ergebnis_Simulation([K_est, b1_est], [T1_est, T2_est, T3_est, T4_est], [0; 0; 0; 0], t, u);

%% Parameteridentifikation LS-Gleichungsfehler DGL (zeit-kontinuierlich) PT3 MIT Anfangswertschaetzung

% Fuer Schaetzung Anfangswert y_0
eins_f = lsim(ZVFdu,ones(size(y)),t,[0; 0; 0; 0; 0]);

% Gefilterete Signale fuer Least-Squares nutzen
y_N = y_f(:,5);                                                                                                         % Messvektor 
S_N = [-y_f(:,1) -y_f(:,2) -y_f(:,3) -y_f(:,4) u_f(:,1) u_f(:,2) eins_f(:,2) eins_f(:,3) eins_f(:,4) eins_f(:,5)];      % Datenmatrix                
theta = pinv(S_N)*y_N;                                                                                                  % Least-Squares-Loesung  

% Umrechnung der Parameter des Least-Squares zu den Parametern der Strecke
T4_est = 1 / theta(1);                                                      % Geschaetzte Strecken-Zeitkonstante T3
T3_est = theta(4) * T4_est;                                                 % Geschaetzte Strecken-Zeitkonstante T2
T2_est = theta(3) * T4_est;                                                 % Geschaetzte Strecken-Zeitkonstante T2
T1_est = theta(2) * T4_est;                                                 % Geschaetzte Strecken-Zeitkonstante T1
K_est = theta(5) * T4_est;                                                  % Geschaetzte Verstaerkung K
b1_est = theta(6) * T4_est/K_est;                                           % Geschaetzte Verstaerkung b1
y_0_est = theta(10);                                                         % Geschaetzter Anfangswert y
dy_0_est = theta(9) - y_0_est*T3_est/T4_est;                                % Geschaetzter Anfangswert dy
ddy_0_est = theta(8) - y_0_est*T2_est/T4_est - dy_0_est*T3_est/T4_est;      % Geschaetzter Anfangswert ddy
dddy_0_est = theta(7) - y_0_est*T1_est/T4_est - dy_0_est*T2_est/T4_est...   % Geschaetzter Anfangswert dddy
        - ddy_0_est*T3_est/T4_est;                                      
    
Ergebnis_Ordnung_4_mit_Ableitung_u.GF_mit_AW = [K_est; b1_est; T1_est; T2_est; T3_est; T4_est];
y2 = Ergebnis_Simulation([K_est, b1_est], [T1_est, T2_est, T3_est, T4_est], [y_0_est; dy_0_est; ddy_0_est; dddy_0_est], t, u); 

%% Parameteridentifikation ueber Ausgangsfehlerminimierung
% Separate Funktion implementieren, die zu einem gegebenen Parametersatz theta den
% Fehler zwischen Modell und Messung zurueckliefert:


theta_0 = [15, 10, 140, 55, 30, 40]; % [K b1 T1 T2 T3 T4] Startwert fuer Optimierung muss ungefaehr stimmen, sonst lokales Minimum
%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich OHNE Anfangswertschaetzung (Annahme x_0 = [0;0;0;0])
theta_opt = fminsearch(@PT4u_Model_Error, theta_0);
Ergebnis_Ordnung_4_mit_Ableitung_u.AF_ohne_AW = [theta_opt(1); theta_opt(2); theta_opt(3); theta_opt(4); theta_opt(5); theta_opt(6)];
y3 = Ergebnis_Simulation([theta_opt(1:2)], theta_opt(3:6), [0;0;0;0], t, u);

%% Ausgangsfehlerbasierte Least-Squares zeitkontinuierlich MIT Anfangswertschaetzung (Annahme x_0 = [y_0;0;0;0])
%theta_opt = fminsearch(@PT4u_Model_Error_x0, [theta_0, 7]);
%Ergebnis_Ordnung_4_mit_Ableitung_u.Ausgangsfehlerbasiert_mit_Anfangswert = [theta_opt(1); theta_opt(2); theta_opt(3); theta_opt(4)];
  
Ergebnis_Ordnung_4_mit_Ableitung_u
Visualisierung(t, [y_mess, y1, y2, y3], 'Modell 4. Ordnung mit Ableitung von u auf rechter Seite');





%% Funktion zur Berechnung des Ausgangssignals (Kleinsignalverhalten) mit den geschaetzten Parametern

function y = Ergebnis_Simulation(K, T, x_0, t, u)
    % Funktion zur Bestimmung des Ausgangssignals (Kleinsignalverhalten) mit den bestimmten Parametern
    % Eingangssignale: Verstaerkung, Zeitkonstanten, Anfangswert, Zeitvektor und Eingang u
    % Ausgangssignale: Ausgang y
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

    y = lsim(system, u, t, x_0);
end

%% Funktion zu Visualisierung

function [] = Visualisierung(t, y, title)

    anzahl = size(y,2);
    
    figure;
    subplot(anzahl,1,1);
    plot(t,y(:,1),'b','LineWidth',2);
    xlabel('t');
    ylabel('y original');

    subplot(anzahl,1,2);
    plot(t,y(:,2),'blue','LineWidth',2);
    xlabel('t');
    ylabel('y GF ohne AW');

    subplot(anzahl,1,3);
    plot(t,y(:,3),'blue','LineWidth',2);
    xlabel('t');
    ylabel('y GF mit AW');
    
    if anzahl >= 4
        subplot(anzahl,1,4);
        plot(t,y(:,4),'blue','LineWidth',2);
        xlabel('t');
        ylabel('y AF ohne AW');
    end
    
    if anzahl == 5
        subplot(anzahl,1,5);
        plot(t,y(:,5),'blue','LineWidth',2);
        xlabel('t');
        ylabel('y AF mit AW');
    end
    
    sgtitle(title)
end
