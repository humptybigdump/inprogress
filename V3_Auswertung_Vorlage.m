%% V3 - Digitale Messdatenverarbeitung Studierende

% In diesem Versuch sollen die mit PULSE gemessenen Daten aus V2 (Stochastisch erregter Einmassenschwinger)  
% eingelesen werden und verarbeitet werden. Die Daten wurden bereits
% gesichtet.
%
% Die gemessenen Daten sind: 
% - Eingang ('in', Kraft ) und 
% - Antwort ('out', Beschleunigung)
% Die Aufgabe besteht darin, das vorliegende Matlab File zu verstehen und
% an den markierten Stellen zu ergaenzen. Die auszufuellenden Stellen sind
% mit '>>> .... <<<' markiert.
% 
% Um die Matlab-Hilfe aufzurufen, druecken Sie F1 oder klicken Sie rechts
% oben im Fenster auf das (?)-Symbol
% 
% Update 30.5.2016
% - Es wurden die festgesetzten y-Achsen im Amplitudengang und in der
%   spektralen Leistungsdichte variabel gemacht.
% - Die Umrechnung vom Bogenmaß in Grad war fehlerhaft.
% 
% Update 01.06.2016
% - Es wurde ein plot hinzugefügt, der das Verhalten des Filters aufzeigt
%   (Zeile 65: freqz(b,a);)
% - Es wurde die Dokumentation im Bereich des Filters erweitert
% - Der Aufruf der pwelch Funktion wurde in den Abschnitt PSD verschoben. 

%% Datenaufbereitung

clear all;
close all;

% PULSE-Daten laden
cd '>>>Pfad zum Messdatenordner hier eingeben<<<'
BKFiles
cd '..'                        % Hier passiert nichts Wichtiges - Es wird lediglich in den ursprünglichen Ordner zurückgegangen.

% Zeitpunkte und -abstand
T  = Group1{1,1}(:,2);         % Zeitvektor
Dt = T(2)-T(1);                % Zeitinkrement zwischen zwei Messpunkten

% Signale
Yout = Group1{1,1}(:,3)';      % Beschleunigungssignal
Yin  = Group1{1,2}(:,3)';      % Kraftsignal

%% Filterung und Integration

% Ausgangssignal (Beschleunigung)
% Hier ist der Befehl "cumsum" zu benutzen. Bei Unklarheit Matlab-Hilfe
% aufrufen
% Die gemessenen Beschleunigungsdaten werden hier in Geschwindigkeitsdaten 
% und Lagedaten umgerechnet. Stichwort: "Untere Treppenapproximation"
Aungefiltert = Yout;
Vungefiltert_treppe = '>>> Hier die untere Treppenapproximation eingeben <<<'; % Geschwindigkeit
Xungefiltert_treppe = '>>> Hier die untere Treppenapproximation eingeben <<<'; % Lage

% Filtergenerierung
fg=5;                                  % Grenzfrequenz des Filters
fs=1/Dt;                               % Abtastfrequenz
[b, a]=butter(5, fg/(fs/2), 'high');   % Grenzfrequenz wird als Bruchteil von fmax = fs/2 angegeben... 'high' -> highpass
                                       % Bemerkung: Der Filter will ein
                                       % eine dimensionslose Frequenz im
                                       % Bereich 0 und 1, wobei 1 der
                                       % maximal darstellbaren Frequenz
                                       % entspricht und 0 der Frequenz 0
                                       % Hz. Ueberpruefung: 
                                      
                                       
freqz(b,a);                            % Hier wird das Verhalten des Filters geplottet.

% Eigentliche Anwendung des Filters
% Hier ist ebenfalls der Befehl "cumsum" zu benutzen.

Agef = filter(b,a, Aungefiltert);   % Hier wird das Beschleunigungssignal gefiltert
Vgef_treppe = '>>> Hier die untere Treppenapproximation eingeben <<<';
Xgef_treppe = '>>> Hier die untere Treppenapproximation eingeben <<<';

%% Spektrale Leistungsdichten (PSD)
%
% Die PSD entspricht dem Betrag der Fourier Transformation. Zugunsten der
% Rauschunterdrueckung werden mehr (aber dafuer kuerzere) Segmente gemittelt
% (Matlab Standard: 8 Segmente, 50% Ueberlappung); die Einzelsegmente werden
% kuerzer, dadurch schlechtere spektrale Aufloesung (Abstand der
% Spektrallinie = Frequenzaufloesung)

% Die Benutzung mehrerer Fenster ermöglicht eine bessere Mittelung.
% Anstatt einer Mittelung über ein grosses Fenster wird hier über mehrere
% kleinere Fenster gemittelt.

Nwindow = floor(length(Aungefiltert)/300);  % floor() rundet ab
Ovrlp=round(0.64*Nwindow);                  % round() rundet

% Abschaetzung nach pwelch (siehe Dokumentation in Matlab)

% ungefiltert
[Paungef, faungef] = pwelch(Aungefiltert, Nwindow,Ovrlp,[], 1/Dt);
[Pvungef, fvungef] = pwelch(Vungefiltert_treppe, Nwindow,Ovrlp ,[], 1/Dt);

% gefiltert
[Pagef, fagef] = pwelch(Agef, Nwindow,Ovrlp,[], 1/Dt);
[Pvgef, fvgef] = pwelch(Vgef_treppe, Nwindow,Ovrlp,[], 1/Dt);


% Darstellung
figure(1);
close all;
plot(faungef, Paungef, '.-');
hold on;
grid on; 
plot(fagef, Pagef, 'r.-');
xlabel('Frequenz f'); ylabel('PSD ');
ymax1 = max(max(Paungef,Pagef));
fl=line([fg fg], [0 ymax1*1.2]);
set(fl, 'Color', 'r', 'LineStyle', '--');
legend('ungefiltert', 'gefiltert');
set(gca, 'YLim', [0 ymax1*1.25]); 
text(fg*1.1, ymax1*1.12, '\leftarrow Eckfrequenz Hochpassfilter', 'background', 'w')


figure(2)
plot(T, Vungefiltert_treppe); hold on;
plot(T, Vgef_treppe, 'r'); hold on;
title('Geschwindigkeit (1Fhg-Schwinger, Rauschanregung)')
legend('v_{ungef}', 'v_{gef}')

figure(3)
plot(T, Xungefiltert_treppe); hold on;
plot(T, Xgef_treppe, 'r'); hold on;
title('Lage (1Fhg-Schwinger, Rauschanregung)')
legend('x_{ungef}', 'x_{gef}')


%% Uebertragungsfunktionen


% Signalanalyse
% 
% Nwind bestimmt die Laenge der zu mittelnden Spektralen Leistungsdichten...
% wenn es gleich der Laenge der Messung ist, wird nur ueber 1 Messung
% gemittelt (also gar nicht!). Overlap ist die Ueberlappung der zu
% mittelnden Abschnitte

Nwind = length(T)/16;
ovrlap = round(0.64*Nwind);


% Bestimmung verschiedener Uebertragungsfunktionen
% unter Verwendung der Funktion cpsd = CrossPowerSpectralDensity

% Anregungsspektrum
[S_Yin_Yin, f1]  = cpsd(Yin, Yin, hann(Nwind),ovrlap,[],1/Dt);
% Ausgangsspektrum
[S_Yout_Yout, f1] = cpsd(Yout, Yout, hann(Nwind),ovrlap,[],1/Dt);

% Uebertragungsfunktion als Quotient der Fourier-Spektren

% Schaetzer G0
G0 = '>>> Hier den Schaetzer G0 eingeben <<<';

% Schaetzer G1
S_Yin_Yout = cpsd(Yin, Yout, hann(Nwind),ovrlap,[],1/Dt);
G1 = S_Yin_Yout./S_Yin_Yin;

% Schaetzer G2
S_Yout_Yin = '>>> Hier die cpsd Funktion eingeben <<<';
G2 = '>>> Hier den Schaetzer G2 eingeben <<<';

% Schaetzer G3
G3 = '>>> Hier den Schaetzer G3 eingeben <<<';


% Darstellung

% Uebertragungsfunktionen
figure(4);
subplot(1,3,1);
plot(f1, abs(S_Yin_Yin), '.-');
grid on;
set(gca, 'XLim', [10 100]);
title('spektr. Leistungsdichte Eingang')

subplot(1,3,2);
plot(f1, abs(G0), 'k--');
hold on;
plot(f1, abs(G1), 'b');  % G1  
plot(f1, abs(G2), 'r');  % G2
plot(f1, abs(G3), 'g');  % G3
title('Uebertragungsfunktionen')

legend('G0', 'G1', 'G2', 'G3', 'Location', 'northwest');
grid on;
set(gca, 'XLim', [10 100]);

subplot(1,3,3);
plot(f1, abs(S_Yout_Yout), '.-');
grid on;
set(gca, 'XLim', [10 100]);
title('spektr. Leistungsdichte Ausgang')


% "Bode"-Diagramm
figure(5);
subplot(2,1,1);
plot(f1, abs(G0), 'k--');
hold on;
plot(f1, abs(G1), 'b');  % G1  
plot(f1, abs(G2), 'r');  % G2
plot(f1, abs(G3), 'g');  % G3
title('Amplitudengang')
ylabel('Vergroesserung [-]');
legend('G0', 'G1', 'G2', 'G3', 'Location', 'southeast');
set(gca, 'XLim', [0 100], 'YLim',[0 300]);

subplot(2,1,2);
plot(f1, angle(G0)/pi*180, 'k--');
hold on;
plot(f1, angle(G1)/pi*180, 'b');  % G1  
plot(f1, angle(G2)/pi*180, 'r');  % G2
plot(f1, angle(G3)/pi*180, 'g');  % G3
title('Phasengang')
xlabel('Frequenz [Hz]'); ylabel('Phasenwinkel [Deg]');
set(gca, 'XLim', [0 100]);


% Nyquist-Digramm (der Bereich <10 Hz wird abgeschitten, da Gezappel)
figure(6);
plot(G1(find(f1>=10,1):end),'b');
hold on;
plot(G2(find(f1>=10,1):end),'r');
plot(G3(find(f1>=10,1):end),'g');
plot(G3(find(f1>=28,1)),'ko');
plot(G3(find(f1>=32.5,1)),'k*');
title('Nyquist-Diagramm')
legend('G1', 'G2', 'G3', '28 Hz', '32 Hz', 'Location', 'southeast');



