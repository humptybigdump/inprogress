% Auswahl Einzelmerkmal (EM)
% {'Concrete compressive strength(MPa, megapascals)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'Concrete compressive strength(MPa, megapascals)'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

% Alle Werte
set(gaitfindobj('CE_EM_Ausgangs_Alle'),'value',0);eval(gaitfindobj_callback('CE_EM_Ausgangs_Alle'));

%% Umwandeln,  Bearbeiten,  Ausgewählte Einzelmerkmale -> Ausgangsgrößen 
eval(gaitfindobj_callback('MI_EM_Klasse'));

% Auswahl Ausgangsgröße
% {'Concrete compressive strength(MPa, megapascals)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Concrete compressive strength(MPa, megapascals)'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  ANOVA, univariat 
eval(gaitfindobj_callback('MI_EMAusw_ANOVA'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  MANOVA, multivariat 
eval(gaitfindobj_callback('MI_EMAusw_MANOVA'));

