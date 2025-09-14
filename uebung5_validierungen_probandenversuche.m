% Validierungstyp
% {'Bootstrap'}
set_textauswahl_listbox(gaitfindobj('CE_CV_Typ'),{'Cross-validation'});eval(gaitfindobj_callback('CE_CV_Typ'));

% n-fache Crossvalidierung
set(gaitfindobj('CE_CV_n'),'string','2');eval(gaitfindobj_callback('CE_CV_n'));

% Versuchsanzahl
set(gaitfindobj('CE_CV_Versuche'),'string','2');eval(gaitfindobj_callback('CE_CV_Versuche'));

%% Klassifikation,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_EMKlassi_EnAn'));

%% Validierung,  Data-Mining,  Einzelmerkmale-Klassifikation 
eval(gaitfindobj_callback('MI_CV_EM_Standard'));

% Validierungstyp
% {'Bootstrap'}
set_textauswahl_listbox(gaitfindobj('CE_CV_Typ'),{'Bootstrap'});eval(gaitfindobj_callback('CE_CV_Typ'));

%% Validierung,  Data-Mining,  Einzelmerkmale-Klassifikation 
eval(gaitfindobj_callback('MI_CV_EM_Standard'));

