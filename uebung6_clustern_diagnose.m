% Auswahl Einzelmerkmal (EM)
% {'Messwert x1','Messwert x2'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'Messwert x1','Messwert x2'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

% Anzahl Cluster
set(gaitfindobj('CE_Cluster_AnzCluster'),'string','2');eval(gaitfindobj_callback('CE_Cluster_AnzCluster'));

% Abstandsmaß
% {'Euclidean distance'}
set_textauswahl_listbox(gaitfindobj('CE_Cluster_Abtandsmass'),{'Euclidean distance'});eval(gaitfindobj_callback('CE_Cluster_Abtandsmass'));

%% Cluster-Verfahren,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_Cluster_Ber'));

%% Cluster-Verfahren,  Ansicht,  Cluster-Zugehörigkeiten (sortiert nach Clustern) 
eval(gaitfindobj_callback('MI_Ansicht_ClusterZGH_sortiert'));

%% Cluster-Verfahren,  Ansicht,  Clustergramm 
eval(gaitfindobj_callback('MI_Ansicht_Clustergramm'));

