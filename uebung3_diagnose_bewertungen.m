% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

% Anzahl auszuwählender Merkmale
set(gaitfindobj('CE_Anzahl_Merkmale'),'string','2');eval(gaitfindobj_callback('CE_Anzahl_Merkmale'));

% TEX-Protokoll
set(gaitfindobj('CE_Tex_Protokoll'),'value',0);eval(gaitfindobj_callback('CE_Tex_Protokoll'));


% Auswahl Ausgangsgröße
% {'Diagnose (2 Klassen)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Diagnose (2 Klassen)'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  ANOVA, univariat 
eval(gaitfindobj_callback('MI_EMAusw_ANOVA'));

%% Einzelmerkmale,  Ansicht,  Merkmalsrelevanzen anzeigen (Tabelle,sortiert) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Relevanzen'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  MANOVA, multivariat 
eval(gaitfindobj_callback('MI_EMAusw_MANOVA'));

%% Einzelmerkmale,  Ansicht,  Merkmalsrelevanzen anzeigen (Tabelle,sortiert) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Relevanzen'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  Informationstheoretische Maße 
eval(gaitfindobj_callback('MI_EMAusw_Inform'));

%% Einzelmerkmale,  Ansicht,  Merkmalsrelevanzen anzeigen (Tabelle,sortiert) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Relevanzen'));

%% Einzelmerkmale,  Ansicht,  Entropiebilanz 
eval(gaitfindobj_callback('MI_Anzeige_Entropie'));

% Auswahl Ausgangsgröße
% {'Diagnose (3 Klassen)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Diagnose (3 Klassen)'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  ANOVA, univariat 
eval(gaitfindobj_callback('MI_EMAusw_ANOVA'));

%% Einzelmerkmale,  Ansicht,  Merkmalsrelevanzen anzeigen (Tabelle,sortiert) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Relevanzen'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  MANOVA, multivariat 
eval(gaitfindobj_callback('MI_EMAusw_MANOVA'));

%% Einzelmerkmale,  Ansicht,  Merkmalsrelevanzen anzeigen (Tabelle,sortiert) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Relevanzen'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  Informationstheoretische Maße 
eval(gaitfindobj_callback('MI_EMAusw_Inform'));

%% Einzelmerkmale,  Ansicht,  Merkmalsrelevanzen anzeigen (Tabelle,sortiert) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Relevanzen'));

%% Einzelmerkmale,  Ansicht,  Entropiebilanz 
eval(gaitfindobj_callback('MI_Anzeige_Entropie'));




