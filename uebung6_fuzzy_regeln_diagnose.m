% ALLE 4
eval(gaitfindobj_callback('CE_Alle_EM'));



% Verfahren
% {'Fuzzy classifier'}
set_textauswahl_listbox(gaitfindobj('CE_Spezielle_Verfahren'),{'Fuzzy classifier'});eval(gaitfindobj_callback('CE_Spezielle_Verfahren'));

% Typ Zugehörigkeitsfunktion
% {'Clustering'}
set_textauswahl_listbox(gaitfindobj('CE_Fuzzy_TypeZGF'),{'Clustering'});eval(gaitfindobj_callback('CE_Fuzzy_TypeZGF'));

% Anzahl Linguistische Terme
set(gaitfindobj('CE_Fuzzy_AnzLingTerme'),'string','5');eval(gaitfindobj_callback('CE_Fuzzy_AnzLingTerme'));

%% Fuzzy-Systeme,  Data-Mining,  Entwurf (Einzelregeln) 
eval(gaitfindobj_callback('MI_Fuzzy_Einzelregel'));

% MAKRO AUSWAHLFENSTER Regeln anzeigen (mit Grafik)
auswahl.rule=[];
auswahl.rule(1)= 4;
eval(gaitfindobj_callback('MI_Fuzzy_Grafik'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

% Aktueller Klassifikator
% {'Fuzzy classifier'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Klassifikator'),{'Fuzzy classifier'});eval(gaitfindobj_callback('CE_Klassifikation_Klassifikator'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));


% n-fache Crossvalidierung
set(gaitfindobj('CE_CV_n'),'string','5');eval(gaitfindobj_callback('CE_CV_n'));

% Versuchsanzahl
set(gaitfindobj('CE_CV_Versuche'),'string','2');eval(gaitfindobj_callback('CE_CV_Versuche'));



%% Validierung,  Data-Mining,  Einzelmerkmale-Klassifikation 
eval(gaitfindobj_callback('MI_CV_EM_Standard'));

