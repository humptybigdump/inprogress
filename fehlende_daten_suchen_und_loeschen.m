%% Bearbeiten,  Fehlende Daten suchen 
eval(gaitfindobj_callback('MI_Anzeige_FehlDaten'));

% Löschschwellwert [Proz. fehlende Daten]
set(gaitfindobj('CE_Nullzr_Schwellwert'),'string','20');eval(gaitfindobj_callback('CE_Nullzr_Schwellwert'));

%% Löschen,  Bearbeiten,  Fehlende Daten 
eval(gaitfindobj_callback('MI_Nullzr_loeschen'));

%% Bearbeiten,  Fehlende Daten suchen 
eval(gaitfindobj_callback('MI_Anzeige_FehlDaten'));

