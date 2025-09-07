% Auswahl Zeitreihe (ZR)
% {'P_{mess}','P_{mess} NORMMEAN'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'P_{mess}','P_{mess} NORMMEAN'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));

% MAKRO AUSWAHLFENSTER Zeitreihe -> Zeitreihe, Zeitreihe -> Einzelmerkmal...
auswahl.gen=[];
auswahl.gen{1}={'P_{mess}','P_{mess} NORMMEAN'};
auswahl.gen{2}={'Whole time series (0...100%)'};
auswahl.gen{3}={'Maximum (MAX)','Minimum (MIN)','Mean value SF (MEAN)'};
eval(gaitfindobj_callback('MI_Extraktion_ZRZR'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

% Auswahl Einzelmerkmal (EM)
% {'MAX ZR P_{mess}','MIN ZR P_{mess}'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'MAX ZR P_{mess}','MIN ZR P_{mess}'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

%% Einzelmerkmale,  Ansicht,  Einzelmerkmale gegen Einzelmerkmale 
eval(gaitfindobj_callback('MI_Anzeige_EM'));

% Auswahl Ausgangsgröße
% {'MONAT'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'MONAT'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Einzelmerkmale,  Ansicht,  Einzelmerkmale gegen Einzelmerkmale 
eval(gaitfindobj_callback('MI_Anzeige_EM'));


