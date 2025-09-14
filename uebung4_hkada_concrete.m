% Merkmalsaggregation
% {'Principal Component Analysis (PCA)'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Merkmalsaggregation'),{'Principal Component Analysis (PCA)'});eval(gaitfindobj_callback('CE_Klassifikation_Merkmalsaggregation'));

% Auswahl Einzelmerkmale
% {'Selected features'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Merkmalsauswahl'),{'Selected features'});eval(gaitfindobj_callback('CE_Klassifikation_Merkmalsauswahl'));

% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));

% Anzahl aggregierter Merkmale
set(gaitfindobj('CE_Anzahl_Aggregiert'),'string','3');eval(gaitfindobj_callback('CE_Anzahl_Aggregiert'));

% Normierung Einzelmerkmale
% {'Interval [0,1]'}
set_textauswahl_listbox(gaitfindobj('CE_Normierung_Merkmale'),{'Interval [0,1]'});eval(gaitfindobj_callback('CE_Normierung_Merkmale'));

%% Extrahieren,  Bearbeiten,  Einzelmerkmale -> Einzelmerkmale (mit gewählter Merkmalsaggregation aus Optionen-Data Mining: Klassifikation Einzelmerkmale) 
eval(gaitfindobj_callback('MI_Extraktion_EMEMA'));

phi_hk

% Merkmalsaggregation
% {'Discriminant analysis (DA)'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Merkmalsaggregation'),{'Discriminant analysis (DA)'});eval(gaitfindobj_callback('CE_Klassifikation_Merkmalsaggregation'));

%% Extrahieren,  Bearbeiten,  Einzelmerkmale -> Einzelmerkmale (mit gewählter Merkmalsaggregation aus Optionen-Data Mining: Klassifikation Einzelmerkmale) 
eval(gaitfindobj_callback('MI_Extraktion_EMEMA'));

phi_dis

