% FFT
clear;
close all;

%% F R A G E N

% 0. Orientierung
%    > Zoomen Sie in das Zeitsignal, erkennen Sie die Frequenzanteile und
%      das Rauschen?
%    > Vergleichen Sie die Transformierten des Signals einmal mit Rauschen
%      und einmal ohne Rauschen -> (das hier verwendete Breitband-)Rauschen
%      führt bei bei allen Frequenzen einen niedrigen Zusatzwert ein
%      ("Grundpegel")
%
% 1. Abtastung / FFT
%    Schauen Sie sich die Frequenzauflösung (Abstand zwischen den
%    Spektrallinien) an. 
%    > Wie lässt sich diese verbessern? 
%    > Wie groß ist die maximal sichtbare / darstellbare Frequenz im Spektrum?
%
% 2. Leakage
%    > Lässt sich das Leakage durch höhere Frequenzauflösung beheben? 
%    > Versuchen Sie mehrere Fenster (d.h. betrachten Sie die
%      F-Transformierten Xhan, Xham, ...
%
% 3. Warum sehen Sin / Cos im dargestellten Spektrum gleich aus?


%% S I G N A L

% geg.: eine Funktion, "Signal" genannt (s.u.)
% die Werte dieser (Zeit-)Funktion werden an diskreten Zeitpunkten bestimmt
% und im Messvektor x abgespeichert (=Abtastung)

fs = 3e2;        % Abtastfrequenz ("Sample-Frequenz") 
% fs = 50;
Dt = 1/fs;       % zeitlicher Abstand der Signalpunkte = Abtastperiode

tmax = 90;       % Signaldauer = Länge des betrachteten Signals = "Messdauer"
t = 0:Dt:tmax;   % Zeitvektor

% das Signal enthält 2 Frequenzen (f1, f2) sowie eine normalverteilte
% zufällige Störung (mit randn erstellt)
f1 = 10; 
f2 = 20; 
x = sin(2*pi*f1*t) + cos(2*pi*f2*t) + 0.05*randn(1,length(t));   %Signal, original
xideal = sin(2*pi*f1*t) + cos(2*pi*f2*t) ;   %Signal, idealisiert = ohne Rauschen

xidhan = hann(length(x))'.*xideal;
xhan   = hann(length(x))'.*x;       % Signal mit Hanning-Fenster gewichtet
xhamm  = hamming(length(x))'.*x;    % Signal mit Hamming-Fenster gewichtet 
xblack = blackman(length(x))'.*x;   % Signal mit Blackman-Fenster gewichtet


%% F F T

% FFT kann nur Signale verarbeiten, deren Länge eine Zweierpotenz ist ->
% erst muss die nächstgelegene, geeignete Signallänge ermittelt werden.
% Matlabs FFT hängt einfach entsprechend viele Nullen an, um die Länge des
% Signal auf 2^N zu bringen ("Zero-Padding"). 

% Diese Länge muss ermittelt werden, um die zugehörige Grundfrequenz zu
% ermitten, usw --> ein paar Vorarbeiten

NFFT = 2^(nextpow2(length(t))); % nächstgrößere Zweierpotenz
TFFT = (NFFT-1)*Dt;        % Matlab macht "zero-padding" -> Zeitreihe wird länger > TFFT ist die Länge dieser erweiterten Signalreiheder Zeitreihe

f0   = 1/TFFT;             % Grundfrequenz, d.h. Frequenzabstand der FFT - hängt von der Länge (Zweierpotenz!) ab
fmax = fs/2;               % maximale Frequenz im Frequenzbereich (Abtasttheorem!)
f    = -fmax:f0:fmax;      % Frequenzvektor

% hier nun die eigtl Transformation der Signale
X      = Dt*fft(x, NFFT);            % FFT - "unbehandelt", Signallänge ist NFFT
Xidhan = Dt*fft(xidhan, NFFT);       % FFT - ideales Signal ohne Rauschen
Xhan   = Dt*fft(xhan, NFFT);         % FFT - "Hanning-Fenster"
Xhamm  = Dt*fft(xhamm, NFFT);        % FFT - "Hamming-Fenster"
Xblack = Dt*fft(xblack, NFFT);       % FFT - "Blackman-Fenster"


%% D A R S T E L L U N G

% gewünschte/nicht gewünschte Zeitreihen ein-/auskommentieren

figure(2)
clf;

subplot(2,1,1);
plot(t, x,'b.-'); hold on;
plot(t, xhamm,'g.-'); 
plot(t, xhan,'r.-'); 
plot(t, xblack,'k.-'); 
set(gca, 'XLim', [0 TFFT]);
xlabel('Zeit t [s]'); ylabel('Signal x')

subplot(2,1,2)
stem(f, abs(fftshift(X)), 'b.-'); hold on;
stem(f, abs(fftshift(Xhan)), 'r.-'); hold on;
%stem(f, abs(fftshift(Xidhan)), 'y.-'); hold on;
% stem(f, abs(fftshift(Xhamm)), 'g.-'); hold on;
% stem(f, abs(fftshift(Xblack)), 'k.-'); hold on;
set(gca, 'XLim', [0 30]);
xlabel('Frequenz f [Hz]'); ylabel('Betrag F-Transformierte |X(\omega)|')
