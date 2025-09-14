% Verfahren
% {'Fuzzy classifier'}
set_textauswahl_listbox(gaitfindobj('CE_Spezielle_Verfahren'),{'Fuzzy classifier'});eval(gaitfindobj_callback('CE_Spezielle_Verfahren'));

% Typ Zugehörigkeitsfunktion
% {'Equal distribution'}
set_textauswahl_listbox(gaitfindobj('CE_Fuzzy_TypeZGF'),{'Equal distribution'});eval(gaitfindobj_callback('CE_Fuzzy_TypeZGF'));

% Anzahl Linguistische Terme
set(gaitfindobj('CE_Fuzzy_AnzLingTerme'),'string','2');eval(gaitfindobj_callback('CE_Fuzzy_AnzLingTerme'));

%% Auswahl und Bewertung von Einzelmerkmalen,  Data-Mining,  Informationstheoretische Maße 
eval(gaitfindobj_callback('MI_EMAusw_Inform'));

%% Einzelmerkmale,  Ansicht,  Zugehörigkeitsfunktion und Gesamthistogramm 
eval(gaitfindobj_callback('MI_Anzeige_ZGF_Gesamthistogramm'));

