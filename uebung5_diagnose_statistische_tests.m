% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

% TEX-Protokoll
set(gaitfindobj('CE_Tex_Protokoll'),'value',0);eval(gaitfindobj_callback('CE_Tex_Protokoll'));

% Auswahl Ausgangsgröße
% {'Diagnose (3 Klassen)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Diagnose (2 Klassen)'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  T-Test berechnen (nur mit STAT-Toolbox!) 
eval(gaitfindobj_callback('MI_TTest'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  Test auf Normalverteilung 
eval(gaitfindobj_callback('MI_NormTest'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  Wilcoxon-Ranksum-Test berechnen (nur mit STAT-Toolbox!) 
eval(gaitfindobj_callback('MI_Wilcoxon'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

%% Einzelmerkmale,  Ansicht,  Mittelwert, Streuung, Minimum, Maximum 
eval(gaitfindobj_callback('MI_Anzeige_EM_Min_Max'));

% Auswahl Ausgangsgröße
% {'Diagnose (3 Klassen)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Diagnose (3 Klassen)'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  T-Test berechnen (nur mit STAT-Toolbox!) 
eval(gaitfindobj_callback('MI_TTest'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  Test auf Normalverteilung 
eval(gaitfindobj_callback('MI_NormTest'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  Wilcoxon-Ranksum-Test berechnen (nur mit STAT-Toolbox!) 
eval(gaitfindobj_callback('MI_Wilcoxon'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

%% Einzelmerkmale,  Ansicht,  Mittelwert, Streuung, Minimum, Maximum 
eval(gaitfindobj_callback('MI_Anzeige_EM_Min_Max'));




