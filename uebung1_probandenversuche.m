%% Ansicht,  Klassenzugehörigkeiten ausgewählter Datentupel anzeigen 
eval(gaitfindobj_callback('MI_Anzeige_Datentupel'));

%% Ansicht,  Anzahl Terme für ausgewählte Datentupel 
eval(gaitfindobj_callback('MI_Anzeige_Terms'));

% Auswahl Einzelmerkmal (EM)
% {'S1 Dauer Bereich II','S1 Dauer Bereich III','S1 Dauer Bereich IV','S1 rel. Dauer Bereich II'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'S1 Dauer Bereich II','S1 Dauer Bereich III','S1 Dauer Bereich IV','S1 rel. Dauer Bereich II'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

%% Einzelmerkmale,  Ansicht,  Einzelmerkmale gegen Einzelmerkmale 
eval(gaitfindobj_callback('MI_Anzeige_EM'));



