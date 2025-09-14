% Auswahl Zeitreihe (ZR)
% {'Energy'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'Energy'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));

%% Cluster-Verfahren,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_Cluster_Ber'));

%% Zeitreihen,  Ansicht,  Mittelwertszeitreihen 
eval(gaitfindobj_callback('MI_Anzeige_ZR_MW'));

%% Cluster-Verfahren,  Ansicht,  Cluster-Zugehörigkeiten (sortiert nach Clustern) 
eval(gaitfindobj_callback('MI_Ansicht_ClusterZGH_sortiert'));

