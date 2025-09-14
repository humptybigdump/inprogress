ta = 0.01;
t  = [0:ta:20]';
yd.time = t;
yd.signals.values = sin(t);
ud.time = t;
ud.signals.values = 5*cos(t)-5*sin(t);


%% Ohne Berücksichtigung der Anfangswerte
% Simulink-Modell mit Übertragungsfunktion der Strecke
% Keine Vorgabe von Anfangswerten möglich
sim('ReglermitVorsteuerung.mdl', max(t),simset('AbsTol',1e-5))
figure(1); clf;
plot(yd.time,yd.signals.values,'r','Linewidth',3);
hold on;
plot(y.time,y.Data,'g','Linewidth',2);
xlabel('t'); ylabel('yd,y'); legend('yd','y')


%% Variante mit Sprung auf Anfangswerte mit Puls 
ud_puls = ud;
ud_puls.signals.values(1) = ud.signals.values(1)+6/ta; % Dirac-Impuls mit Fläche 6 hinzufügen

% Simulink-Modell mit Übertragungsfunktion der Strecke
% Keine Vorgabe von Anfangswerten möglich
sim('ReglermitVorsteuerungPuls.mdl', max(t),simset('AbsTol',1e-5))
figure(2); clf;
plot(yd.time,yd.signals.values,'r','Linewidth',3);
hold on;
plot(y.time,y.Data,'g','Linewidth',2);
xlabel('t'); ylabel('yd,y'); legend('yd','y')

%% Variante mit Setzen der Anfangswerte in Zustandsraummodell
% Simulink-Modell mit Zustandsraumdarstellung der Strecke können die
% Anfangswerte mit x_0=[0;1] konsistent zum Vorsteuersignal gewählt werden 
sim('ReglermitVorsteuerungStateSpace.mdl', max(t),simset('AbsTol',1e-5))
figure(3); clf;
plot(yd.time,yd.signals.values,'r','Linewidth',3);
hold on;
plot(y.time,y.signals.values,'g','Linewidth',2);
xlabel('t'); ylabel('yd,y'); legend('yd','y')