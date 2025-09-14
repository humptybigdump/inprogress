% Auswahl Einzelmerkmal (EM)
% {'MAX ZR Energy','MIN ZR Energy'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'MAX ZR Energy','MIN ZR Energy'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

%% Einzelmerkmale,  Ansicht,  Manuelle Klassenzuweisung Datentupel über Einzelmerkmale 
eval(gaitfindobj_callback('MI_Anzeige_SpecialSelection'));
