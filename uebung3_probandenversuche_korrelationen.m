% Typ für Korrelationsparameter
% {'Pearson'}
set_textauswahl_listbox(gaitfindobj('CE_Corr_Type'),{'Pearson'});eval(gaitfindobj_callback('CE_Corr_Type'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

%% Einzelmerkmale,  Ansicht,  Korrelationsvisualisierung 
eval(gaitfindobj_callback('MI_Korrelationsvisualisierung'));

% Typ für Korrelationsparameter
% {'Spearman'}
set_textauswahl_listbox(gaitfindobj('CE_Corr_Type'),{'Spearman'});eval(gaitfindobj_callback('CE_Corr_Type'));

%% Einzelmerkmale,  Ansicht,  Korrelationsvisualisierung 
eval(gaitfindobj_callback('MI_Korrelationsvisualisierung'));

% TEX-Protokoll
set(gaitfindobj('CE_Tex_Protokoll'),'value',0);eval(gaitfindobj_callback('CE_Tex_Protokoll'));

% Kritischer Korrelationskoeffizient
set(gaitfindobj('CE_Krit_Koeff'),'string','0.7');eval(gaitfindobj_callback('CE_Krit_Koeff'));

%% Einzelmerkmale,  Ansicht,  Korrelationskoeffizienten (Pearson) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Korr'));

%% Einzelmerkmale,  Ansicht,  Korrelationskoeffizienten (Spearman) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Spear'));

