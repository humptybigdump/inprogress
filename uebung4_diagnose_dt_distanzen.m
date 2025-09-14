% Auswahl Einzelmerkmal (EM)
% {'Messwert x1','Messwert x2','Messwert x3','Messwert x4'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'Messwert x1','Messwert x2','Messwert x3','Messwert x4'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

% Norm (Datentupeldistanzen)
% {'Frobenius norm'}
set_textauswahl_listbox(gaitfindobj('CE_DatDistNorm'),{'Frobenius norm'});eval(gaitfindobj_callback('CE_DatDistNorm'));

% Normierung Einzelmerkmale
% {'None'}
set_textauswahl_listbox(gaitfindobj('CE_Normierung_Merkmale'),{'None'});eval(gaitfindobj_callback('CE_Normierung_Merkmale'));

%% Datentupel-Distanzen ,  Ansicht,  Berechnen (ausgewählte Datentupel) 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatCompInd'));

%% Datentupel-Distanzen ,  Ansicht,  Matrix anzeigen 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatMat'));

% Auswahl Einzelmerkmal (EM)
% {'Messwert x1','Messwert x2','Messwert x3','Messwert x4'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'Messwert x1','Messwert x2'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

%% Datentupel-Distanzen ,  Ansicht,  Berechnen (ausgewählte Datentupel) 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatCompInd'));

%% Datentupel-Distanzen ,  Ansicht,  Matrix anzeigen 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatMat'));

% Normierung Einzelmerkmale
% {'MEAN = 0, STD = 1'}
set_textauswahl_listbox(gaitfindobj('CE_Normierung_Merkmale'),{'MEAN = 0, STD = 1'});eval(gaitfindobj_callback('CE_Normierung_Merkmale'));

%% Datentupel-Distanzen ,  Ansicht,  Berechnen (ausgewählte Datentupel) 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatCompInd'));

%% Datentupel-Distanzen ,  Ansicht,  Matrix anzeigen 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatMat'));

%% Datentupel-Distanzen ,  Ansicht,  Sortieren (VAT-Algorithmus) 
eval(gaitfindobj_callback('MI_Ansicht_PairDistSortVAT'));

%% Datentupel-Distanzen ,  Ansicht,  Matrix anzeigen 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatMat'));

%% Auswählen,  Bearbeiten,  Alle Datentupel 
eval(gaitfindobj_callback('MI_Datenauswahl_Alle'));

% Manuelle Auswahl von Datentupeln
set(gaitfindobj('CE_Select_DataPoints'),'string','15');eval(gaitfindobj_callback('CE_Select_DataPoints'));

%% Datentupel-Distanzen ,  Ansicht,  Berechnen (Nachbarn suchen für erstes Element manuelle Auswahl) 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatCompNeighb'));

% k
set(gaitfindobj('CE_kNN_k'),'string','10');eval(gaitfindobj_callback('CE_kNN_k'));

%% Datentupel-Distanzen ,  Ansicht,  Nachbarn anzeigen 
eval(gaitfindobj_callback('MI_Ansicht_PairDistDatNeighb'));



