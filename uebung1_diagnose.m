%% Ansicht,  Klassenzugehörigkeiten ausgewählter Datentupel anzeigen 
eval(gaitfindobj_callback('MI_Anzeige_Datentupel'));

%% Ansicht,  Anzahl Terme für ausgewählte Datentupel 
eval(gaitfindobj_callback('MI_Anzeige_Terms'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

% Auswahl Ausgangsgröße
% {'Diagnose (3 Klassen)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Diagnose (3 Klassen)'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Einzelmerkmale,  Ansicht,  Einzelmerkmale gegen Einzelmerkmale 
eval(gaitfindobj_callback('MI_Anzeige_EM'));

% MAKRO AUSWAHLFENSTER Datentupel über Klassen ...
auswahl.dat=[];
auswahl.dat{1}={'All'};
auswahl.dat{2}={'B_1: Fehlerfrei','B_2: Fehler Typ A'};
eval(gaitfindobj_callback('MI_Datenauswahl_Klassen'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

%% Einzelmerkmale,  Ansicht,  Einzelmerkmale gegen Einzelmerkmale 
eval(gaitfindobj_callback('MI_Anzeige_EM'));

% Auswahl Einzelmerkmal (EM)
% {'Messwert x1','Messwert x2','Messwert x3','Messwert x4'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'Messwert x1','Messwert x2','Messwert x3','Messwert x4'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

%% Einzelmerkmale,  Ansicht,  Einzelmerkmale gegen Einzelmerkmale 
eval(gaitfindobj_callback('MI_Anzeige_EM'));




