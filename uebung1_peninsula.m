%% Ansicht,  Klassenzugehörigkeiten ausgewählter Datentupel anzeigen 
eval(gaitfindobj_callback('MI_Anzeige_Datentupel'));

%% Ansicht,  Anzahl Terme für ausgewählte Datentupel 
eval(gaitfindobj_callback('MI_Anzeige_Terms'));

% Imageplot Zeitreihen (Farbkodierung)
set(gaitfindobj('CE_Anzeige_ZRImagePlot'),'value',0);eval(gaitfindobj_callback('CE_Anzeige_ZRImagePlot'));

% Klassensortierung für Imageplot
set(gaitfindobj('CE_Anzeige_ZRImagePlotClassSort'),'value',0);eval(gaitfindobj_callback('CE_Anzeige_ZRImagePlotClassSort'));

% Auswahl Ausgangsgröße
% {'Vertrag'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Vertrag'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

% Auswahl Zeitreihe (ZR)
% {'P_{mess}'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'P_{mess}'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));

%% Zeitreihen,  Ansicht,  Mittelwertszeitreihen 
eval(gaitfindobj_callback('MI_Anzeige_ZR_MW'));

% Auswahl Ausgangsgröße
% {'WOCHENTAG'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'WOCHENTAG'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Zeitreihen,  Ansicht,  Mittelwertszeitreihen 
eval(gaitfindobj_callback('MI_Anzeige_ZR_MW'));

% MAKRO AUSWAHLFENSTER Datentupel über Klassen ...
auswahl.dat=[];
auswahl.dat{1}={'All'};
auswahl.dat{2}={'All'};
auswahl.dat{3}={'All'};
auswahl.dat{4}={'All'};
auswahl.dat{5}={'All'};
auswahl.dat{6}={'MONTAG'};
auswahl.dat{7}={'All'};
auswahl.dat{8}={'All'};
auswahl.dat{9}={'All'};
auswahl.dat{10}={'All'};
eval(gaitfindobj_callback('MI_Datenauswahl_Klassen'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

% Auswahl Ausgangsgröße
% {'Vertrag'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'Vertrag'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Zeitreihen,  Ansicht,  Mittelwertszeitreihen 
eval(gaitfindobj_callback('MI_Anzeige_ZR_MW'));

% Imageplot Zeitreihen (Farbkodierung)
set(gaitfindobj('CE_Anzeige_ZRImagePlot'),'value',1);eval(gaitfindobj_callback('CE_Anzeige_ZRImagePlot'));

%% Zeitreihen,  Ansicht,  Originaldaten 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));

% MAKRO AUSWAHLFENSTER Datentupel über Klassen ...
auswahl.dat=[];
auswahl.dat{1}={'All'};
auswahl.dat{2}={'All'};
auswahl.dat{3}={'All'};
auswahl.dat{4}={'All'};
auswahl.dat{5}={'All'};
auswahl.dat{6}={'All'};
auswahl.dat{7}={'All'};
auswahl.dat{8}={'671'};
auswahl.dat{9}={'All'};
auswahl.dat{10}={'All'};
eval(gaitfindobj_callback('MI_Datenauswahl_Klassen'));
eval(get(figure_handle(size(figure_handle,1),1),'callback'));

% Auswahl Ausgangsgröße
% {'WOCHENTAG'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_Ausgangsgroesse'),{'WOCHENTAG'});eval(gaitfindobj_callback('CE_Auswahl_Ausgangsgroesse'));

%% Zeitreihen,  Ansicht,  Originaldaten 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));


