% Selection of time series (TS)
% {'Energy'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'Energy'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));

%% Time series (TS),  View,  Original time series 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));

% MACRO CONFIGURATION WINDOW Time series -> Time series, Time series -> Single features...
auswahl.gen=[];
auswahl.gen{1}={'Energy'};
auswahl.gen{2}={'Whole time series (0...100%)'};
auswahl.gen{3}={'Maximum (MAX)','Minimum (MIN)'};
eval(gaitfindobj_callback('MI_Extraktion_ZRZR'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

% Selection of single feature(s) (SF)
% {'MAX TS Energy','MIN TS Energy'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'MAX TS Energy','MIN TS Energy'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

%% Time series (TS),  View,  Original time series 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));


% Selection of single feature(s) (SF)
% {'MAX TS Energy','MIN TS Energy'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_EM'),{'MAX TS Energy','MIN TS Energy'});eval(gaitfindobj_callback('CE_Auswahl_EM'));

%% Single features,  View,  Single features vs. single features 
eval(gaitfindobj_callback('MI_Anzeige_EM'));



