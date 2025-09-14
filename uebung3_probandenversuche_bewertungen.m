% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

% TEX-Protokoll
set(gaitfindobj('CE_Tex_Protokoll'),'value',0);eval(gaitfindobj_callback('CE_Tex_Protokoll'));

% Anzahl auszuwählender Merkmale
set(gaitfindobj('CE_Anzahl_Merkmale'),'string','2');eval(gaitfindobj_callback('CE_Anzahl_Merkmale'));

% Auswahl Ausgangsgröße
% {'Griffart'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Griffart'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

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

%
