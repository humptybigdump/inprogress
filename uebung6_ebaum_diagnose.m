

% Aktueller Klassifikator
% {'Decision tree'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Klassifikator'),{'Decision tree'});eval(gaitfindobj_callback('CE_Klassifikation_Klassifikator'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

% Auswahl Einzelmerkmale
% {'Selected features'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Merkmalsauswahl'),{'Selected features'});eval(gaitfindobj_callback('CE_Klassifikation_Merkmalsauswahl'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

%% Ansicht,  Entscheidungsbaum (LaTeX) 
eval(gaitfindobj_callback('MI_Ansicht_Ebaum'));

