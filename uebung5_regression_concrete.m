% Auswahl Einzelmerkmal (EM)
% {'Cement (component 1)(kg in a m^3 mixture)','Blast Furnace Slag (component 2)(kg in a m^3 mixture)','Fly Ash (component 3)(kg in a m^3 mixture)','Water  (component 4)(kg in a m^3 mixture)','Superplasticizer (component 5)(kg in a m^3 mixture)','Coarse Aggregate  (component 6)(kg in a m^3 mixture)','Fine Aggregate (component 7)(kg in a m^3 mixture)','Age (day)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'Cement (component 1)(kg in a m^3 mixture)','Blast Furnace Slag (component 2)(kg in a m^3 mixture)','Fly Ash (component 3)(kg in a m^3 mixture)','Water  (component 4)(kg in a m^3 mixture)','Superplasticizer (component 5)(kg in a m^3 mixture)','Coarse Aggregate  (component 6)(kg in a m^3 mixture)','Fine Aggregate (component 7)(kg in a m^3 mixture)','Age (day)'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

% Ausgangsgröße Regression
% {'Concrete compressive strength(MPa, megapascals)'}
set_textauswahl_listbox(gaitfindobj('CE_Regression_Output'),{'Concrete compressive strength(MPa, megapascals)'});eval(gaitfindobj_callback('CE_Regression_Output'));

% Merkmalsauswahl
% {'Selected features'}
set_textauswahl_listbox(gaitfindobj('CE_Regression_Merkmalsauswahl'),{'Selected features'});eval(gaitfindobj_callback('CE_Regression_Merkmalsauswahl'));

% Verfahren
% {'Polynom'}
set_textauswahl_listbox(gaitfindobj('CE_Spezielle_Verfahren'),{'Polynom'});eval(gaitfindobj_callback('CE_Spezielle_Verfahren'));

% Maximale Anzahl interner Merkmale
set(gaitfindobj('CE_Regression_AnzahlPolyMerkmale'),'string','4');eval(gaitfindobj_callback('CE_Regression_AnzahlPolyMerkmale'));

%% Regression,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_Regression_EnAn'));

%% Regression,  Ansicht,  Koeffizienten Polynom-Modell 
eval(gaitfindobj_callback('MI_Anzeige_Koeff_Polynom'));

%% Regression,  Ansicht,  Ausgangsgröße und Schätzung 
eval(gaitfindobj_callback('MI_Anzeige_Regression_y_ydach'));

%% Regression,  Ansicht,  Ausgangsgröße und Fehler 
eval(gaitfindobj_callback('MI_Anzeige_Regression_y_Fehler'));

% Grad Polynom
set(gaitfindobj('CE_Regression_GradPolynom'),'string','3');eval(gaitfindobj_callback('CE_Regression_GradPolynom'));

%% Regression,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_Regression_EnAn'));

%% Regression,  Ansicht,  Ausgangsgröße und Schätzung 
eval(gaitfindobj_callback('MI_Anzeige_Regression_y_ydach'));

% Typ
% {'Artificial Neural Networks'}
set_textauswahl_listbox(gaitfindobj('CE_Regression_Typ'),{'Artificial Neural Networks'});eval(gaitfindobj_callback('CE_Regression_Typ'));

%% Regression,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_Regression_EnAn'));

%% Regression,  Ansicht,  Ausgangsgröße und Schätzung 
eval(gaitfindobj_callback('MI_Anzeige_Regression_y_ydach'));

%% Validierung,  Data-Mining,  Regression 
eval(gaitfindobj_callback('MI_CV_RegrEM_Standard'));



