%% Alias-Effekt (Unterabtastung)
% ein Signal x mit zwei Frequenzanteilen, wird einmal sehr hoch (also quasi
% "kontinuierlich") abgetastet (_> x1), ein zweites mal niedriger (> x2).
% Ist die zweite Abtastfrequenz kleiner als 2mal die maximale im Signal x
% enthaltene Frequenz, so tritt der Aliasingeffekt ("Unterabtastung") auf 
%
% 
%   Veraendern Sie die Abtastrate, z.B. fs2 = 50, 40, 35, 30, 25, 22, 20, 18
%   > was faellt bei 35 Hz auf? 
%   > Wieso sieht man bei 30 Hz nur eine Frequenz, fuer 25 wieder 2?
%   > Was passiert beim Uebergang von 20 Hz auf 18 Hz?

clear;
close all;


%%  A B T A S T U N G    

% muss hier bereits angegeben werden, damit die Signale auf dem richtigen
% Raster erstellt werden.
% 1. Frequenz viel höher als Signalfrequenzen, 2. variabel

% Abtastfrequenzen
fs1 = 1000;
fs2 = 13;        % <- Durch Veraendern dieser Abtastfrequenz wird der Einfluss des Alias-Effekts deutlich


%% S I G N A L E

T = 20;          % Signallaenge (Zeit)
fI = 10;         % Frequenz 1. Anteil in den Signalen (Hertz !)
fII = 20;        % Frequenz 2. Anteil in den Signalen (Hertz !)

% Sinal 1 (Orignalsignal)
t1 = linspace(0, T, T*fs1 + 1);
x1 = sin(2*pi*fI*t1) + sin(2*pi*fII*t1);

% Signal 2 (niedriger abgetastet)
t2 = linspace(0, T, T*fs2 + 1);
x2 = sin(2*pi*fI*t2) + sin(2*pi*fII*t2);


%% Signalanalyse (Spektrale Leistungsdichten zur Frequenzinhaltsdarstellung)

[P1, f1] = pwelch(x1, [],[],[], fs1);
[P2, f2] = pwelch(x2, [],[],[], fs2);


%% Darstellung
figure(1)

subplot(2,1,1)
    plot(t1,x1); hold on
    plot(t2, x2, 'r.-'); 
    set(gca, 'XLim', [0 0.3]);
    title('Abtastung im Zeitbereich');
    xlabel('t [s]'); ylabel('x [-]');


subplot(2,1,2)
    plot(f1, P1, '.-'); hold on;
    plot(f2, P2, 'r.-'); 
    set(gca, 'XLim', [0 30]);
    
    h=line([1 1]*fs2/2, [0 1]*max(get(gca, 'YLim'))); set(h, 'Color', 'r', 'LineStyle', ':', 'Linewidth', 2)
    tt=text(1*fs2/2, 0.8*max(get(gca, 'YLim')), 'f_{max,unter} = f_{s2}/2  \rightarrow'); set(tt, 'HorizontalAlignment', 'right', 'Color', 'r');

    if fs2<2*fII, tt2='Unterabtastung'; else tt2='richtige Abtastung'; end;
    legend('richtig', tt2);
    title('Frequenzspektrum');
    xlabel('f [Hz]');
    ylabel('P [-]');