clear zeitreihen

%Parameter setzen
laenge_zeitreihe = 9000;
projektinfos.abtastfrequenz = 100;
frequenz1 = 1;
frequenz2 = 0.1;
zeitreihen = [];
zeitreihen_name = {};
rauschanteil = 0.1;
trendanstieg = 0.1;
i=0;

%Trend erzeugen
i=i+1;
zeitreihen(1,1:laenge_zeitreihe,i) = trendanstieg*[1:laenge_zeitreihe]/projektinfos.abtastfrequenz;
zeitreihen_name{i} = 'Trend';

%Sinus mit 1. Grundfrequenz erzeugen
i=i+1;
zeitreihen(1,1:laenge_zeitreihe,i) = sin(2*pi/projektinfos.abtastfrequenz*frequenz1*[1:laenge_zeitreihe]);
zeitreihen_name{i} = sprintf('Sinus mit Grundfrequenz %g Hz',frequenz1);

%Sinus mit 1. Grundfrequenz und Rauschen erzeugen
i=i+1;
zeitreihen(1,1:laenge_zeitreihe,i) = sin(2*pi/projektinfos.abtastfrequenz*frequenz1*[1:laenge_zeitreihe])+rauschanteil*randn(1,laenge_zeitreihe);
zeitreihen_name{i} = sprintf('Sinus mit Grundfrequenz %g Hz mit Rauschen',frequenz1);

%Sinus mit 2. Grundfrequenz erzeugen
i=i+1;
zeitreihen(1,1:laenge_zeitreihe,i) = sin(2*pi/projektinfos.abtastfrequenz*frequenz2*[1:laenge_zeitreihe]);
zeitreihen_name{i} = sprintf('Sinus mit Grundfrequenz %g Hz',frequenz2);

%Sinus mit 2. Grundfrequenz und Rauschen erzeugen
i=i+1;
zeitreihen(1,1:laenge_zeitreihe,i) = sin(2*pi/projektinfos.abtastfrequenz*frequenz2*[1:laenge_zeitreihe])+rauschanteil*randn(1,laenge_zeitreihe);
zeitreihen_name{i} = sprintf('Sinus mit Grundfrequenz %g Hz mit Rauschen',frequenz2);

%Trend und beide Sinus mit Grundfrequenz überlagern
i=i+1;
zeitreihen(1,1:laenge_zeitreihe,i) = sum(zeitreihen(1,1:laenge_zeitreihe,[1 3 5]),3);
zeitreihen_name{i} = sprintf('Trend + 2*Sinus mit Grundfrequenz %g und %g Hz mit Rauschen',frequenz1,frequenz2);

%Gait-CAD-Projekt erzeugen
generate_new_scixminer_project('filter.prjz',[],[],[],[],[],zeitreihen,char(zeitreihen_name),[],[],projektinfos);
 

