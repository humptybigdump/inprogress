close all
%% a) System erstellen und Eigenbewegung ohne Regler simulieren
A=[0 1;-1 -0.1];
B=[0;1];
C=[1 0];
D=0;
x0=[0;1];
sys=ss(A,B,C,D);

%Simulation Strecke mit u=0
t=[0:0.1:100]';
u=zeros(1001,1);
[y,t,x]=lsim(sys,u,t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
legend('Weg x_1','Geschwindigkeit x_2');
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure; %Phasenporträt
plot(x(:,1),x(:,2));
xlabel('Weg in m');
ylabel('Geschwindigkeit in m/s');

%% b) LQ-Regler entwerfen
Q = eye(2);
%Q=C'*C; % wenn bzgl. Ausgangsfehler optimiert werden soll.
R = 1;
%R = 0.1 % es werden größere Reglerverstärkungen und damit größere Stellgrößen generiert
%R = 10  % es werden kleinere Reglerverstärkungen und damit kleinere Stellgrößen generiert
K = lqr(A,B,Q,R)
F = inv((C-D*K)*inv(-A+B*K)*B+D)

% Simulation des Zustandsregelkreises (Stabilisierung)
sys_RK=ss(A-B*K,B*F,C-D*K,D*F); % Siehe Folie 9 vd = F*y_d
t=[0:0.1:14]'; %kuerzere Zeit, da Regelkreis schneller
yd=zeros(141,1); %Einregeln nach Anfangsstörung (Anfangsgeschwindigkeit)
[y,t,x]=lsim(sys_RK,yd,t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure; %Phasenporträt
plot(x(:,1),x(:,2),'linewidth',2);
xlabel('Weg in m');
ylabel('Geschwindigkeit in m/s');
figure; %Stellverlauf
plot(t,-x*K'+F*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');

%% c) Simulation des Zustandsregelkreises (Führungsverhalten) ohne Modellfehler
x0 =[0;0];
yd=ones(141,1);
[y,t,x]=lsim(sys_RK,yd,t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure; %Stellverlauf
plot(t,-x*K'+F*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');
%Jetzt ist es an der Zeit, den Einfluss von R zu untersuchen.
%Hierzu ist oben R=0.1 und R=10 einzuklammern.
%Kleine R bedeuten geringe Bestrafung des Stellaufwands, also sportliche
%Regler
%Wer Lust hat, dreht jetzt am Q
%Q=C'*C bewertet den quadratische Ausgangsfehler, oben ausklammern
%Der fleißige Student vergleicht die Ausgangsfehlerquadratflächen
%Für Q=C'*C ist die Fläche kleiner.


%% d) Simulation des Zustandsregelkreises (Führungsverhalten) mit Modellfehlern
%Identifiziertes Modell, das leicht von tatsächlichem System abweicht:
A_dach=[0 1;-1.1 -0.11];
B_dach=[0;0.9]; 
C_dach=[1 0];
D_dach=0;

%Reglerentwurf auf Basis fehlerhaftem Modell --> fehlerhafter Regler:
K_dach=lqr(A_dach,B_dach,Q,R)
F_dach=inv((C_dach-D_dach*K_dach)*inv(-A_dach+B_dach*K_dach)*B_dach+D_dach)

%Simulation des geschlossenen Regelkreises mit fehlerhaftem Regler
sys_RKmitFehlern=ss(A-B*K_dach,B*F_dach,C-D*K_dach,D*F_dach);
% Hinweis: Für den Reglerentwurf (inkl. Vorfilter) liegt nur das
% fehlerbehaftete Modell vor. Der Regler wird aber dann auf das echte
% System angewendet bzw. hier mit echtem System simuliert. 
[y,t,x]=lsim(sys_RKmitFehlern,yd,t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure; %Stellverlauf
plot(t,-x*K_dach'+F_dach*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');
%deutlich zu erkennen ist, dass keine stationäre Genauigkeit mehr vorliegt

%% e) Zustandsregler mit Integrator (PI-Regler) mit Modellfehlern
% Strecke virtuell um Integrator erweitern (Folie 34)
K_pireg = lqr([A_dach zeros(2,1);C_dach 0],[B_dach; D_dach],blkdiag(Q,1),R) 
%(Zustandsgroessenwichtung auch fuer Integrator --> Q um 1 erweitern)
K_x = K_pireg(1:2); 
K_xi = K_pireg(3); %Plus, da Regelfehler bei uns definiert mit y-yd

%Alternative über lqi-Befehl:
%K_pireg = lqi(ss(A_dach,B_dach,C_dach,D_dach),[Q,[0;0];0,0,1],R);
%K_x = K_pireg(1:2); 
%K_xi = -K_pireg(3); %Minus, da Regelfehler in Matlab definiert mit yd-y

F_pireg=inv((C_dach-D_dach*K_x)*inv(-A_dach+B_dach*K_x)*B_dach+D_dach)
%F_pireg=inv((C-D*K_x)*inv(-A+B*K_x)*B+D)

% Simulation geschlossener Regelkreis mit Zustands-PI-Regler
sys_RKPI=ss([A-B*K_x -B*K_xi; C-D*K_x -D*K_xi],[B*F_pireg; D*F_pireg-eye(1)],[C-D*K_x -D*K_xi], D*F_pireg);
[y,t,x]=lsim(sys_RKPI,yd,t,[x0;0]); %Integratoranfangswert auf null

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure; %Stellverlauf
plot(t,-x*K_pireg'+F_pireg*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');
figure; %Integratoranteil
plot(t,-x(:,3)*K_xi,'c','linewidth',2);
xlabel('Zeit in s');
ylabel('Integratoranteil in N');
%deutlich zu erkennen ist, dass stationäre Genauigkeit vorliegt
%Wird F_pireg aus den wahren Streckenmatrizen berechnet, steht im Integrator tatsächlich stationär eine Null
%Dieser Fall kann durch Löschen des Kommentars vor F_pidreg überprüft
%werden

% Wegen PI-Zustandsregler ist bei Stellbergenzungen noch eine AW-Maßnahme zu entwerfen
% Das geht dann einfacher mit Simulink. 
% Siehe dazu Simulink-Modell: Zustandsregker_mit_Integratro_AWR


%% f) Zustandsregler mit Beobachter mit Eigenwertplatzierung auf [-2,-6]
% RK-Eigenwerte bei -0.68+-1i also Faktor 3 und 9 für Realteil 
L = acker(A',C',[-2 -6])'

% Zustandsraummodell für Regler mit Beobachter
% (Realisierung siehe Folie 24 "Beobachter-Entwurf")
sys_RegBeob = ss(A-L*C-(B-L*D)*K, [(B-L*D)*F,L], -K, [F,0]);      

% Zustandsraummodell für Regelkreis mit Regler mit Beobachter 
% (Realisierung siehe Folie 25 "Beobachter-Entwurf")
sys_Durchgriff = ss(0,0,0,1);
sys_Erweitert = append(sys_Durchgriff,sys);
feedin=2;
feedout=[1 2];
Cloop=feedback(sys_Erweitert,sys_RegBeob,feedin,feedout,+1);

% Simulation des Führungsverhaltens des Regelkreises mit Beobachter
yd=ones(141,1);
[y,t,x]=lsim(Cloop,[yd, zeros(141,1);],t, [0 0 0 1 1]);

figure; %Zeitverlaufsbild
plot(t,x(:,2),t,x(:,3),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure; %Stellverlauf
plot(t,-x(:,4:5)*K'+F*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');


%% g) Zurück auf Los (ideale Streckenkenntnis) - Folgeregler
%Simulation des Zustandsregelkreises (Führungsverhalten)
%So sieht der Zustandsregler für yd=sin(t) aus
sys_RK=ss(A-B*K,B*F,C-D*K,D*F);
yd=sin(t);
[y,t,x]=lsim(sys_RK,yd,t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
figure;
plot(t,-x*K'+F*yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft in N');
%ein wahrlich schlechtes Ergebnis
%aus dem Stellverlauf lesen wir eine Amplitude von 0.1 ab
%Das ist auch richtig, denn die Streckenvorsteuerung ist $ud=0.1*cos(t), da
%G(s)=1/(s^2+0.1s+1) ist, also [sin(t)]''+0.1[sin(t)]'+sin(t)=ud

%% h) Hilfloser Versuch das Ergebnis durch anderen Entwurf zu verbessern
K_acker=acker(A,B,[-15, -15]);
F_acker=inv((C-D*K_acker)*inv(-A+B*K_acker)*B+D);
sys_RK=ss(A-B*K_acker,B*F_acker,C-D*K_acker,D*F_acker);
yd=sin(t);
[y,t,x]=lsim(sys_RK,yd,t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
figure;
plot(t,-K_acker*x'+F_acker*yd','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft in N');
%optisch sieht das Ergebnis deutlich besser aus
%Der Stellwertverlaufist bei t=0.1 aber eine Katastrophe!!!!


%% i) Jetzt soll der Einfluss von Messfehlern bei der Erfassung der aktuellen Zustandsgrößen x1 und x2 bei diesen hohen Verstärkungen gezeigt werden. 
% Hierzu wird ein zusätzlicher Eingang für die Zustands-Messstörung z benötigt, der zwei dimensionen hat, da es zwei Zustandsgrößen gibt.
% Setzt man das um die Messstörung erweiterte Reglergesetz u = -K*(x+z)+F*yd in die Strecke ein, erhält man für den Regelkreis: 
sys_RK=ss(A-B*K_acker,[B*F_acker,-B*K_acker],[C-D*K_acker],[D*F_acker,-D*K_acker]);

% höhere Zeitauflösung für Simulation, um höherfrequente Rauschen nachbilden zu können
t=[0:0.01:14]';
yd=sin(t);
z=0.01*randn(length(t),2); %Die Störung ist etwa ein Hunderstel der Zustandsamplituden (entspricht 1 Prozent Fehler)
[y,t,x]=lsim(sys_RK,[yd,z],t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
figure;  %Stellverlaufsbild
plot(t,-K_acker*(x'+z')+F_acker*yd','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft in N');
%Der Stellverlauf ist eine Katastrophe (Stellglied nach 10 Sekunden kaputt)!!!!


%% j) 2DOF-Zustandsregler mit Regelkreisvorsteuerung
% Streckenvorsteuerung (Folie 5) nicht sinnvoll, da xd und ud separat berechnet werden müssten
% Regelkreisvorsteuerung (Folie 6): statisch (Festwertregelung) vd = F*yd*, 
% Für Folgeregelung: vd aus inverser des geschlossenen Regelkreises bestimmen
sys_RK_2DOF=ss(A-B*K,B,C-D*K,D);
tf(sys_RK_2DOF) %Die Vorsteuerung ist für den Regelkreis (nicht die Strecke) zu entwerfen
%zum Glück treten hier keine Zählernullstellen auf, die Regelkreisvorsteuerung vd kann 
%einfach durch Einsetzen des Sollsignals in die DGL berechnet werden
[num, den]=tfdata(sys_RK_2DOF);
% Damit direkt die Vorsteuerung berechnet werden kann, wird der Faktor vor u auf 1 normiert:
nenner=den{1}/num{1}(3);

%für Sollsignal yd = sin(t):
yd=sin(t);
vd=nenner(3)*sin(t)+nenner(2)*cos(t)-nenner(1)*sin(t);
x0=[0;0]; % Nullruhelage Anfangswert) nicht konsistent mit yd = sin(t)
%x0=[0;1]; % konsistenter Anfangswert für yd = sin(t)

%für Sollsignal yd = cos(t):
%yd=cos(t);
%vd=nenner(3)*cos(t)-nenner(2)*sin(t)-nenner(1)*cos(t);
%x0=[1;0]; %konsistenter Anfangswert für yd = cos(t)

[y,t,x]=lsim(sys_RK_2DOF,vd,t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
figure;  %Stellverlaufsbild
plot(t,-K*x'+vd','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft in N');
%hier hatten wir Glück, dass die Anfangswerte x0=[0;1] für den Sinus konsistent
%waren. 
% Wie sehen konsistente Anfangswerte und die Vorsteuerung für ein
% Sollsignal yd=cos(t) aus? --> x0=[1;0]


%% k) 2DOF-Zustandsregler, jetzt mit Modellfehler
% Vorsteuerung auf Basis des RK mit fehlerhaftem Modell 
sys_RK_2DOF_dach=ss(A_dach-B_dach*K_dach,B_dach,C_dach-D_dach*K_dach,D_dach);
tf(sys_RK_2DOF_dach) 
[num, den]=tfdata(sys_RK_2DOF_dach);
nenner=den{1}/num{1}(3);
yd=sin(t);
% Regelkreisvorsteuersignal auf Basis fehlerhaftem Modell
vd_dach=nenner(3)*sin(t)+nenner(2)*cos(t)-nenner(1)*sin(t);

% Simulation der echten Strecke mit Regler und Vorsteuerung auf Basis fehlerhaftem Modell
sys_RK_2DOF=ss(A-B*K_dach,B,C-D*K_dach,D);
x0=[0;1];
[y,t,x]=lsim(sys_RK_2DOF,vd_dach,t,x0);

figure; %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');


%% l) 2DOF-Zustandsregler, jetzt mit Modellfehler plus Störung am Ausgang nach 3 Sekunden

sys_RK_2DOF=ss(A-B*K_dach,[B zeros(2,1)],C-D*K_dach,[D 1]); %über die 1 im Durchgriff wirkt die Störung auf y
% Standard-Regelkreis gemäß Folie 9 mit zusätzlicher Ausgangsstörung za als zusätzlicher
% Eingang u2 = za. Die Ausgangsstörung muss nur additiv in der Ausgangsgleichung
% durch die zusätzliche 1 in [D 1] berücksichtigt werden. In der
% Systemgleichung muss nur die Dimension von B wegen des zusätzlichen Eingangs für die Ausgangsstörung erweitert werden. 
% Das aber durch eine Nullspalte, da die Ausgangsstörung ja nicht auf den Zustand wirkt. 

% Vorsteuerung wieder auf Basis des RK mit fehlerhaftem Modell 
sys_RK_2DOF_dach=ss(A_dach-B_dach*K_dach,B_dach,C_dach-D_dach*K_dach,D_dach);
tf(sys_RK_2DOF_dach) 
[num, den]=tfdata(sys_RK_2DOF_dach);
nenner=den{1}/num{1}(3);
yd=sin(t);
vd=nenner(3)*sin(t)+nenner(2)*cos(t)-nenner(1)*sin(t);

% Simulation wieder mit echter Strecke (fehlerfrei)
x0=[0;1];
% Ausgangsstörung geht nach 3 Sekunden von 0 auf den Wert 1
z=[zeros(301,1); ones(1100,1)];
[y,t,x]=lsim(sys_RK_2DOF,[vd,z],t,x0);

figure; %Zeitverlaufsbild
plot(t,y,t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
%der Zustandsregler sieht die Ausgangsstörung nicht und kann sie daher
%nicht bekämpfen, auch wenn er sie sehen würde, ist er nur ein P-Regler und
%würde i.Allg. keine stationäre Genauigkeit erreichen 


%% m) Um Ausgangsstörung und Modellfehler kompensieren zu können, wird eine Ausgangsrückführung mit PI-Regler benötigt
%PI-Reglerentwurf wieder mit fehlerbehaftetem Modell (exakt wir oben)
K_pireg = lqr([A_dach zeros(2,1);C_dach 0],[B_dach; D_dach],blkdiag(Q,1),R)
K_x = K_pireg(1:2); 
K_xi = K_pireg(3);

% Regelkreisvorsteuerung entwerfen (exakt wie oben)
sys_RK_vorst_dach=ss(A_dach-B_dach*K_x,B_dach,C_dach-D_dach*K_x,D_dach);
tf(sys_RK_vorst_dach) 
[num, den]=tfdata(sys_RK_vorst_dach);
nenner=den{1}/num{1}(3);
%für Sollsignal yd = sin(t):
yd=sin(t);
vd=nenner(3)*sin(t)+nenner(2)*cos(t)-nenner(1)*sin(t);

% System für Simulation aus Original-Strecke und eben entworfenem PI-Regler mit den Eingängen [vd; yd; z]
% (Herleitung siehe Musterlösung)
sys_RKPI=ss([A-B*K_x -B*K_xi; C-D*K_x -D*K_xi],[[B, zeros(2,1); D -1] [zeros(2,1);1]],[C-D*K_x -D*K_xi], [D 0 1]);

%Simulation System mit Vorsteuerung 
%(sowohl Regler als auch Vorsteuerung mit fehlerbehaftetem Modell entworfen)
x0=[0;1];
%Ohne Störung -> Modellfehler führen zu Abweichung, da I-Regler für Sinus nicht optimal
z = zeros(1401,1);
%Mit Störung wie oben -> Störung wird durch Ausgangsrückführung mit
%I-Anteil weggeregelt (hierfür nachfolgende Zeile aktivieren)
z=[zeros(301,1); ones(1100,1)];
[y,t,x]=lsim(sys_RKPI,[vd,yd,z],t,[x0;0]); %Integratoranfangswert auf null
figure; %Zeitverlaufsbild
plot(t,y,t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');


%% Das Ganze nun mit Störgrößenaufschaltung /-reduktion
% hier ist der fleißige Studierende gefragt


