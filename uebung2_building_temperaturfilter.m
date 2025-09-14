%% Zeitreihen,  Ansicht,  Originaldaten 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));

% Plugins aktualisieren
eval(gaitfindobj_callback('CE_PlugListUpdate'));

% Auswahl Plugins
% {'Filtering (FIL)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Plugins'),{'Filtering (FIL)'});eval(gaitfindobj_callback('CE_Auswahl_Plugins'));

% Plugin-Parameter
% {'Lowpass'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_PluginsCommandLine'),{'Lowpass'});eval(gaitfindobj_callback('CE_Auswahl_PluginsCommandLine'));

% Nr.
% {'P2/3'}
set_textauswahl_listbox(gaitfindobj('CE_Plugins_ParameterNumber'),{'P2/4'});eval(gaitfindobj_callback('CE_Plugins_ParameterNumber'));

% Plugin-Parameter
set(gaitfindobj('CE_Auswahl_PluginsCommandLine'),'string','3');eval(gaitfindobj_callback('CE_Auswahl_PluginsCommandLine'));

% Nr.
% {'P3/3'}
set_textauswahl_listbox(gaitfindobj('CE_Plugins_ParameterNumber'),{'P3/4'});eval(gaitfindobj_callback('CE_Plugins_ParameterNumber'));

% Plugin-Parameter
set(gaitfindobj('CE_Auswahl_PluginsCommandLine'),'string','2');eval(gaitfindobj_callback('CE_Auswahl_PluginsCommandLine'));

% MAKRO AUSWAHLFENSTER Zeitreihe -> Zeitreihe, Zeitreihe -> Einzelmerkmal...
auswahl.gen=[];
auswahl.gen{1}={'TEMP'};
auswahl.gen{2}={'Whole time series (0...100%)'};
auswahl.gen{3}={'Filtering (FIL)'};
eval(gaitfindobj_callback('MI_Extraktion_ZRZR'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

% Zeitreihen in Subplots zeichnen
set(gaitfindobj('CE_Zeitreihen_Subplots'),'value',0);eval(gaitfindobj_callback('CE_Zeitreihen_Subplots'));

% Auswahl Zeitreihe (ZR)
% {'TEMP','TEMP LPass 3.0'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'TEMP','TEMP LPass 3.0'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));

%% Zeitreihen,  Ansicht,  Originaldaten 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Auswahl Plugins
% {'Filtering (FIL)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Plugins'),{'Filtering (FIL)'});eval(gaitfindobj_callback('CE_Auswahl_Plugins'));

% Nr.
% {'P2/3'}
set_textauswahl_listbox(gaitfindobj('CE_Plugins_ParameterNumber'),{'P2/4'});eval(gaitfindobj_callback('CE_Plugins_ParameterNumber'));

% Plugin-Parameter
set(gaitfindobj('CE_Auswahl_PluginsCommandLine'),'string','0.01 ');eval(gaitfindobj_callback('CE_Auswahl_PluginsCommandLine'));

% MAKRO AUSWAHLFENSTER Zeitreihe -> Zeitreihe, Zeitreihe -> Einzelmerkmal...
auswahl.gen=[];
auswahl.gen{1}={'TEMP'};
auswahl.gen{2}={'Whole time series (0...100%)'};
auswahl.gen{3}={'Filtering (FIL)'};
eval(gaitfindobj_callback('MI_Extraktion_ZRZR'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

% Zeitreihen in Subplots zeichnen
set(gaitfindobj('CE_Zeitreihen_Subplots'),'value',0);eval(gaitfindobj_callback('CE_Zeitreihen_Subplots'));

% Auswahl Zeitreihe (ZR)
% {'TEMP','TEMP LPass 3.0'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'TEMP','TEMP LPass 0.0'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));

%% Zeitreihen,  Ansicht,  Originaldaten 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Auswahl Plugins
% {'Filtering (FIL)'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Plugins'),{'Filtering (FIL)'});eval(gaitfindobj_callback('CE_Auswahl_Plugins'));

% Nr.
% {'P2/3'}
set_textauswahl_listbox(gaitfindobj('CE_Plugins_ParameterNumber'),{'P2/4'});eval(gaitfindobj_callback('CE_Plugins_ParameterNumber'));

% Plugin-Parameter
set(gaitfindobj('CE_Auswahl_PluginsCommandLine'),'string','0.1 ');eval(gaitfindobj_callback('CE_Auswahl_PluginsCommandLine'));

% MAKRO AUSWAHLFENSTER Zeitreihe -> Zeitreihe, Zeitreihe -> Einzelmerkmal...
auswahl.gen=[];
auswahl.gen{1}={'TEMP'};
auswahl.gen{2}={'Whole time series (0...100%)'};
auswahl.gen{3}={'Filtering (FIL)'};
eval(gaitfindobj_callback('MI_Extraktion_ZRZR'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

% Zeitreihen in Subplots zeichnen
set(gaitfindobj('CE_Zeitreihen_Subplots'),'value',0);eval(gaitfindobj_callback('CE_Zeitreihen_Subplots'));

% Auswahl Zeitreihe (ZR)
% {'TEMP','TEMP LPass 3.0'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'TEMP','TEMP LPass 0.1'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));

%% Zeitreihen,  Ansicht,  Originaldaten 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));
