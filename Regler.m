%% Schnittstellendefinition
% Eingänge
% r;          % Sollwert (Soll-Temperatur °C)
% y;          % Istwert  (Ist-Temperatur °C)
% auto;       % aktuelle Auswahl ob Hand- oder Automatikbetrieb (1 = Automatikbetrieb, 0 = Handbetrieb)
% u_hand;     % manueller Stellwert aus Handbetrieb
 
% Ausgang
% u;          % Stellwert Drehzahl Gebläse Stellbegrenzung 500...1500

%% Initialisierung einmalig beim Start (im realen Einsatz außerhalb des zyklischen Betriebs)
u_max = 1500;      % maximal möglicher Stellwert (Drehzahl Prozessluft-Gebläße)
u_min = 500;       % minimal möglicher Stellwert (Drehzahl Prozessluft-Gebläße)

%% Festlegen der Reglerparameter
K_P = 4;           % Regler-Verstaerkung P-Anteil
T_N = 13;          % Nachstellzeit I-Anteil (Minuten)
T_V = 16;          % Vorhaltezeit D-Anteil (Minuten)
T_Sollwert = 0;    % Zeitkonstante für Führungsgrößenfilterung (Minuten),       Übung: 0 oder 30
T_Messwert = 30;   % Zeitkonstante für Messgrößen-/Regelfehlergrößen (Minuten)  Übung: 10 oder 30

%% Berechnung der zeitdiskreten Filterkonstanten 
c_filter = exp(-delta_t/T_Messwert);            % Regelgrößenfilter (Tiefpassfilter zur Glättung der Regelgröße)
c_filter_sollwert = exp(-delta_t/(T_Sollwert)); % Sollwertfilter (PT2 durch Reihenschaltung 2xPT1), um Sollwersprünge zu glätten
T_paras = 0.2 * T_V;                            % Realsierungs-(Glättungs-)tiefpass
c_filter_e_dot = exp(-delta_t/T_paras);         % Realisierungsfilter (D-Anteil)
T_AWR = sqrt(T_N);                              % Anti-Windup-Filter

%% Zyklisches Einlesen der Eingänge (wird in Simulation durch Strecke.m geliefert, in Realität über Messgrößen)
% r;          % Sollwert (Soll-Temperatur °C)
% y;          % Istwert  (Ist-Temperatur °C)
% auto;       % aktuelle Auswahl ob Hand- oder Automatikbetrieb (1 = Automatikbetrieb, 0 = Handbetrieb)
% u_hand;     % manueller Stellwert aus Handbetrieb


%% Regeln

if (auto == 1)
%% Automatikbetrieb des Reglers
    
    % Hand->Automatik-Umschaltung (bzw. erstmaliger Start)
    if (auto_old == 0) 
        auto_old = 1;
        %Sprungfreie Umschaltung H->A
        %Anfangswerte der Sollwertfilter auf aktuellen Soll-Wert setzen
        r_filtered_PT1 = r;  
        r_filtered_PT2 = r; 
        
        %Anfangswerte des Regelgrößenfilters auf aktuellen Ist-Wert setzen
        e_filtered = 0;
        
        %Anfangswerte für D-Anteil-Realsierungs-(Glättungs-)tiefpass auf 0 setzen
        e_filtered_old = 0;
        e_dot_filtered = 0; 
        
        %Setzen des Integratoranteils 
        I = u_hand;
        
        %Anfangswert des Stellwertfilters auf aktuellen Stellwert
        v_filtered = u_hand; 
    end
    
    % Für Sollgrößensprünge (Arbeitspunktwechsel) anstelle S-Kurven-Berechnung über Polynom:
    % Sollgroessenfilterung (PT2 durch Reihenschaltung zweier PT1), bei
    r_filtered_PT1 = c_filter_sollwert*r_filtered_PT1 + (1-c_filter_sollwert)*r;
    r_filtered_PT2 = c_filter_sollwert*r_filtered_PT2 + (1-c_filter_sollwert)*r_filtered_PT1;
    
    % Berechnung und Filterung des Regelfehlers
    e = (r_filtered_PT2 - y); %ungefiltert
    e_filtered = c_filter * e_filtered + (1-c_filter)*e; %gefiltert
        
    % Berechnung der Ableitung des gefilterten Regelfehlers für D-Anteil per DT1
    e_dot = (e_filtered - e_filtered_old)/delta_t; % Ableitung durch Rückwärtsdifferenz
    e_filtered_old = e_filtered;
    e_dot_filtered = c_filter_e_dot * e_dot_filtered + (1-c_filter_e_dot) * e_dot; %Tiefpassfilterung der Ableitung
    
    
    % Berechnung theoretischer Stellwert 
    P = K_P * e_filtered; 
    I = I + delta_t*1/T_N * e_filtered;
    D = T_V * e_dot_filtered;
    v = P + I + D;% 
    
    % Berechnung tatsächlicher Stellwert u mit Sättigung (Stellbegrenzung)
    if (v > u_max)
        u = u_max;
    elseif (v < u_min)
        u = u_min;
    else
        u = v;
    end
        
    % Anti-windup-Maßnahme 
    
    % Anti-windup-hold: Integrator-Stop (conditional integration oder auch integrator clamping)
    % wenn Sättigung erreicht, dann wird Integrator gestoppt 
    %(also Änderung von oben rückgängig gemacht)
    if (u ~= v)
       I = I - delta_t*1/T_N * e_filtered;
    end
    
    % Alternative: 
    % Anti-wind-up-reset (back-calculation --> gleitendes Rücksetzen)
    % I = I + (delta_t/T_AWR) * (u - v);
    
else
%% Handbetrieb (Stellwert u_hand wird durch Benutzer über GUI im Prozessleitsystem eingegeben)    
    auto_old = 0;
    u = u_hand;
end






