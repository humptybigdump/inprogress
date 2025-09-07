%% Ansicht,  Klassenzugehörigkeiten ausgewählter Datentupel anzeigen 
eval(gaitfindobj_callback('MI_Anzeige_Datentupel'));

%% Ansicht,  Anzahl Terme für ausgewählte Datentupel 
eval(gaitfindobj_callback('MI_Anzeige_Terms'));

% Auswahl Zeitreihe (ZR)
% {'Energy'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'Energy'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));

%% Zeitreihen,  Ansicht,  Originaldaten 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));

%% Zeitreihen,  Ansicht,  Mittelwertszeitreihen 
eval(gaitfindobj_callback('MI_Anzeige_ZR_MW'));

% ALLE 10
eval(gaitfindobj_callback('CE_Alle_ZR'));

%% FFT,  Ansicht,  FFT berechnen und anzeigen (ausgewählte Datentupel und Zeitreihen) 
eval(gaitfindobj_callback('MI_FFT'));



