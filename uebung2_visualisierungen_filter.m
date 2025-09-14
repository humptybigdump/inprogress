
% Auswahl Zeitreihe (ZR)
% {'Trend','Sinus mit Grundfrequenz 1 Hz','Sinus mit Grundfrequenz 1 Hz mit Rauschen','Sinus mit Grundfrequenz 0.1 Hz','Sinus mit Grundfrequenz 0.1 Hz mit Rauschen','Trend + 2*Sinus mit Grundfrequenz 1 und 0.1 Hz mit Rauschen'}
set_textauswahl_listbox(gaitfindobj('CE_Auswahl_ZR'),{'Trend','Sinus mit Grundfrequenz 1 Hz','Sinus mit Grundfrequenz 1 Hz mit Rauschen','Sinus mit Grundfrequenz 0.1 Hz','Sinus mit Grundfrequenz 0.1 Hz mit Rauschen','Trend + 2*Sinus mit Grundfrequenz 1 und 0.1 Hz mit Rauschen'});eval(gaitfindobj_callback('CE_Auswahl_ZR'));


%% FFT,  Ansicht,  FFT berechnen und anzeigen (ausgewählte Datentupel und Zeitreihen) 
eval(gaitfindobj_callback('MI_FFT'));

%% Zeitreihen,  Ansicht,  Originaldaten 
eval(gaitfindobj_callback('MI_Anzeige_ZR_Orig'));

