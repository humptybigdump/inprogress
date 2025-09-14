% Auswahl Einzelmerkmale
% {'All features'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Merkmalsauswahl'),{'All features'});eval(gaitfindobj_callback('CE_Klassifikation_Merkmalsauswahl'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Auswahl Einzelmerkmale
% {'ANOVA'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Merkmalsauswahl'),{'ANOVA'});eval(gaitfindobj_callback('CE_Klassifikation_Merkmalsauswahl'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Anzahl auszuwählender Merkmale
set(gaitfindobj('CE_Anzahl_Merkmale'),'string','2');eval(gaitfindobj_callback('CE_Anzahl_Merkmale'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Aktueller Klassifikator
% {'Bayes'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Klassifikator'),{'Bayes'});eval(gaitfindobj_callback('CE_Klassifikation_Klassifikator'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Normierung Einzelmerkmale
% {'Interval [0,1]'}
set_textauswahl_listbox(gaitfindobj('CE_Normierung_Merkmale'),{'Interval [0,1]'});eval(gaitfindobj_callback('CE_Normierung_Merkmale'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Merkmalsaggregation
% {'Principal Component Analysis (PCA)'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Merkmalsaggregation'),{'Principal Component Analysis (PCA)'});eval(gaitfindobj_callback('CE_Klassifikation_Merkmalsaggregation'));

% Anzahl aggregierter Merkmale
set(gaitfindobj('CE_Anzahl_Aggregiert'),'string','1');eval(gaitfindobj_callback('CE_Anzahl_Aggregiert'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Aktueller Klassifikator
% {'Artificial Neural Networks'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Klassifikator'),{'Artificial Neural Networks'});eval(gaitfindobj_callback('CE_Klassifikation_Klassifikator'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Aktueller Klassifikator
% {'Support Vector Machine'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Klassifikator'),{'Support Vector Machine'});eval(gaitfindobj_callback('CE_Klassifikation_Klassifikator'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Anzahl aggregierter Merkmale
set(gaitfindobj('CE_Anzahl_Aggregiert'),'string','2');eval(gaitfindobj_callback('CE_Anzahl_Aggregiert'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

%% Klassifikation,  Ansicht,  Ergebnis 
eval(gaitfindobj_callback('MI_Anzeige_Klassi_Erg'));

% Aktueller Klassifikator
% {'Bayes'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Klassifikator'),{'Bayes'});eval(gaitfindobj_callback('CE_Klassifikation_Klassifikator'));

%% Klassifikation,  Ansicht,  2D-Klassifikation mit SVMs 
eval(gaitfindobj_callback('MI_Anzeige_Klassi_SVM'));

% Verfahren
% {'Support Vector Machine'}
set_textauswahl_listbox(gaitfindobj('CE_Spezielle_Verfahren'),{'Support Vector Machine'});eval(gaitfindobj_callback('CE_Spezielle_Verfahren'));

% Auswahl Ausgangsgröße
% {'Diagnose (3 Klassen)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Griffart'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Aktueller Klassifikator
% {'Support Vector Machine'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Klassifikator'),{'Support Vector Machine'});eval(gaitfindobj_callback('CE_Klassifikation_Klassifikator'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

%% Klassifikation,  Ansicht,  2D-Klassifikation mit SVMs 
eval(gaitfindobj_callback('MI_Anzeige_Klassi_SVM'));

% Aktueller Klassifikator
% {'Bayes'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Klassifikator'),{'Bayes'});eval(gaitfindobj_callback('CE_Klassifikation_Klassifikator'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

% Mehrklassenprobleme
% {'Pure multiclass problem'}
set_textauswahl_listbox(gaitfindobj('CE_Klassifikation_Mehrklassen'),{'Pure multiclass problem'});eval(gaitfindobj_callback('CE_Klassifikation_Mehrklassen'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

%% Klassifikation,  Ansicht,  2D-Klassifikation mit Kovarianzmatrizen 
eval(gaitfindobj_callback('MI_Anzeige_Klassi_Kova'));

% Trennflächen anzeigen
set(gaitfindobj('CE_Anzeige_Trennflaechen'),'value',0);eval(gaitfindobj_callback('CE_Anzeige_Trennflaechen'));

%% Klassifikation,  Ansicht,  2D-Klassifikation mit Kovarianzmatrizen 
eval(gaitfindobj_callback('MI_Anzeige_Klassi_Kova'));

% Klassenanzeige Ausgangsgröße
% {'Only learning data'}
set_textauswahl_listbox(gaitfindobj('CE_Anzeige_Klassenanzeige'),{'Only learning data'});eval(gaitfindobj_callback('CE_Anzeige_Klassenanzeige'));

%% Klassifikation,  Ansicht,  Ergebnis 
eval(gaitfindobj_callback('MI_Anzeige_Klassi_Erg'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  Klassifikationsgüte (univariat) 
eval(gaitfindobj_callback('MI_Merkausklassuni'));

%% Einzelmerkmale,  Ansicht,  Merkmalsrelevanzen anzeigen (Tabelle,sortiert) 
eval(gaitfindobj_callback('MI_Anzeige_EM_Relevanzen'));

