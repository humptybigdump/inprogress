%% System erstellen
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
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure(2); %Pasenverlaufsbild
plot(x(:,1),x(:,2));
xlabel('Weg in m');
ylabel('Geschwindigkeit in m/s');

%% LQ-Regler entwerfen
Q=eye(2);
%Q=C'*C;
R=1;
%R=0.1
%R=10
K=lqr(A,B,Q,R)
F=inv((C-D*K)*inv(-A+B*K)*B+D)

% Simulation des Zustandsregelkreises (Stabilisierung)
sys_RK=ss(A-B*K,B*F,C-D*K,D*F);
t=[0:0.1:14]'; %kuerzere Zeit, da Regelkreis schnell
yd=zeros(141,1);
[y,t,x]=lsim(sys_RK,yd,t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure(2); %Pasenverlaufsbild
plot(x(:,1),x(:,2),'linewidth',2);
xlabel('Weg in m');
ylabel('Geschwindigkeit in m/s');


%% Simulation des Zustandsregelkreises (Führungsverhalten)
sys_RK=ss(A-B*K,B*F,C-D*K,D*F);
yd=ones(141,1);
[y,t,x]=lsim(sys_RK,yd,t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure(2); %Stellverlauf
plot(t,-x*K'+F*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');
%Jetzt ist es an der Zeit, den Einfluss von R zu untersuchen.
%Hierzu ist ober R=0.1 und R=10 einzuklammern.
%Kleine R bedeuten geringe Bestrafung des Stellaufwands, also sportliche
%Regler
%Wer Lust hat, dreht jetzt am Q
%Q=C^TC bewertet den quadratische Ausgangsfehler, oben ausklammern
%Der fleißige Student vergleicht die Ausgangsfehlerquadratflächen
%Für Q=C^TC ist die Fläche kleiner.


%% Simulation des Zustandsregelkreises (Führungsverhalten)
%mit Modellfehlern
A_dach=[0 1;-1.1 -0.11];;
B_dach=[0;0.9]; 
C_dach=[1 0];
D_dach=0;
K_dach=lqr(A_dach,B_dach,Q,R)
F_dach=inv((C_dach-D_dach*K_dach)*inv(-A_dach+B_dach*K_dach)*B_dach+D_dach)
sys_RKmitFehlern=ss(A-B*K_dach,B*F_dach,C-D*K_dach,D*F_dach);
[y,t,x]=lsim(sys_RKmitFehlern,yd,t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure(2); %Stellverlauf
plot(t,-x*K_dach'+F_dach*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');
%deutlich zu erkennen ist, dass keine stationäre Genauigkeit mehr vorliegt

%% Simulation des PI-Zustandsregelkreises (Führungsverhalten)
%mit Modellfehlern
K_pireg=lqr([A_dach zeros(2,1);C_dach 0],[B_dach; D_dach],blkdiag(Q,1),R)
K_x=K_pireg(1:2); K_xi=K_pireg(3);
F_pireg=inv((C_dach-D_dach*K_x)*inv(-A_dach+B_dach*K_x)*B_dach+D_dach)
%F_pireg=inv((C-D*K_x)*inv(-A+B*K_x)*B+D)
sys_RKPI=ss([A-B*K_x -B*K_xi; C-D*K_x -D*K_xi],[B*F_pireg; D*F_pireg-eye(1)],[C-D*K_x -D*K_xi], D*F_pireg);
[y,t,x]=lsim(sys_RKPI,yd,t,[x0;0]); %Integratoranfangswert auf null
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,x(:,2),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure(2); %Stellverlauf
plot(t,-x*K_pireg'+F_pireg*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');
figure(3); %Integratoranteil
plot(t,-x(:,3)*K_xi,'c','linewidth',2);
xlabel('Zeit in s');
ylabel('Integratoranteil in N');
%deutlich zu erkennen ist, dass stationäre Genauigkeit vorliegt
%Wird F_pireg aus den wahren Streckenmatrizen berechnet, steht im Integrator tatsächlich eine Null
%Dieser Fall kann durch Löschen des Kommentars vor F_pidreg überprüft
%werden

%% Hier sollte eigentlich ein PI-Zustandsregler mit AW-Maßnahme stehen
%Bisher keine Zeit, den zu programmieren



%% Jetzt ein Beobachterentwurf mit Eigenwertplatzierung auf [-2,-6]
%RK-Eigenwerte bei -0.68+-1i also Faktor 3 und 9 für Realteil 
sys_Durchgriff = ss(0,0,0,1);
sys_Erweitert = append(sys_Durchgriff,sys);
L=acker(A',C',[-2 -6])'
sys_RegBeob=ss(A-L*C-B*K+L*D*K,[B*F-L*D*F,L],-K,[F,0]);
feedin=2;
feedout=[1 2];
Cloop=feedback(sys_Erweitert,sys_RegBeob,feedin,feedout,+1);
yd=ones(141,1);
u_aufschaltung = zeros(141,1);
[y,t,x]=lsim(Cloop,[yd, u_aufschaltung],t, [0 0 0 1 1]);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,2),t,x(:,3),'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');
figure(2); %Stellverlauf
plot(t,-x(:,4:5)*K'+F*yd,'r','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft (u) in N');

%% Zurück auf Los (ideale Streckenkenntnis) - Folgeregler
%Simulation des Zustandsregelkreises (Führungsverhalten)
%So sieht der Zustandsregler für yd=sin(t) aus
sys_RK=ss(A-B*K,B*F,C-D*K,D*F);
yd=sin(t);
[y,t,x]=lsim(sys_RK,yd,t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
figure(2);
plot(t,-x*K'+F*yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft in N');
%ein wahrlich schlechtes Ergebnis
%aus dem Stellverlauf lesen wir eine Amplitude von 0.1 ab
%Das ist auch richtig, denn die Streckenvorsteuerung ist $ud=0.1*cos(t), da
%G(s)=1/(s^2+0.1s+1) ist, also [sin(t)]''+0.1[sin(t)]'+sin(t)=ud

%% Hilfloser Versuch das Ergebnis durch anderen Entwurf zu verbessern
K_acker=acker(A,B,[-15, -15]);
F_acker=inv((C-D*K_acker)*inv(-A+B*K_acker)*B+D);
sys_RK=ss(A-B*K_acker,B*F_acker,C-D*K_acker,D*F_acker);
t=[0:0.01:10]';
yd=sin(t);
[y,t,x]=lsim(sys_RK,yd,t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
figure(2);
plot(t,-K_acker*x'+F_acker*yd','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft in N');
%optisch sieht das Ergebnis deutlich besser aus
%Hier schwingt die Stellgröße aber mit einer Amplitude von 0.2, obwohl der
%Regler doch die ideale Streckenvorsteuerung erzeugen müsste
%Wir sind in eine böse Falle getappt: Numerische Probleme
%Aktivieren Sie den Zeitvektor mit höherer Genauigkeit und die Probleme
%sind weg, also Amplitude des stationären Stellsignals wie erwartet 0.1
%Der erste Stellwert von -29.9 ist dagegen eine Katastrophe!!!!

%% Jetzt soll der Einfluss der Messfehler bei diesen hohen
%Verstärkungen gezeigt werden. Hierzu wird ein zweiter Eingang benötigt
sys_RK=ss(A-B*K_acker,[B*F_acker,-B*K_acker],[C-D*K_acker],[D*F_acker,-D*K_acker]);
t=[0:0.01:10]';
yd=sin(t);
z=0.01*randn(1001,2); %Die Störung ist etwa ein Hunderstel der Zustandsamplituden (entspricht 1 Prozent Fehler)
[y,t,x]=lsim(sys_RK,[yd,z],t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
figure(2);  %Stellverlaufsbild
plot(t,-K_acker*(x'+z')+F_acker*yd','linewidth',2);
xlabel('Zeit in s');
ylabel('Kraft in N');
%Der Stellverlauf ist eine Katastrophe (Gerät nach 10 Sekunden kaputt)!!!!


%% Der fleißige Student entwirft hier einen 2DOF-Zustandsregler
%Eingang ist nicht mehr F*yd, sondern direkt ud, deshalb fällt F im System
%weg und neuer Eingang v ist Vorsteuerung ud
sys_RK_2DOF=ss(A-B*K,B,C-D*K,D);
tf(sys_RK_2DOF) %Die Vorsteuerung ist für den Regelkreis (nicht die Strecke) zu entwerfen
%zum Glück treten hier keine Zählernullstellen auf, die Vorsteuerung ud kann 
%einfach durch Einsetzen des Sollsignals in die DGL berechnet werden
[num, den]=tfdata(sys_RK_2DOF);
nenner=den{1}/num{1}(3);
%für Sollsignal yd = sin(t):
yd=sin(t);
ud=nenner(3)*sin(t)+nenner(2)*cos(t)-nenner(1)*sin(t);
x0=[0;1];
%für Sollsignal yd = cos(t):
%yd=cos(t);
%ud=nenner(3)*cos(t)-nenner(2)*sin(t)-nenner(1)*cos(t);
%x0=[1;0];
[y,t,x]=lsim(sys_RK_2DOF,ud,t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
%hier hatten wir Glück, dass die Anfangswerte x0=[0,1] für den Sinus konsistent
%waren, wie sehen konsistente Anfangswerte und die Vorsteuerung für ein Sollsignal yd=cos(t) aus

%% 2DOF-Zustandsregler, jetzt mit Modellfehler
sys_RK_2DOF=ss(A-B*K_dach,B,C-D*K_dach,D);
sys_RK_2DOF_dach=ss(A_dach-B_dach*K_dach,B_dach,C_dach-D_dach*K_dach,D_dach);
tf(sys_RK_2DOF_dach) 
[num, den]=tfdata(sys_RK_2DOF_dach);
nenner=den{1}/num{1}(3);
yd=sin(t);
ud=nenner(3)*sin(t)+nenner(2)*cos(t)-nenner(1)*sin(t);
x0=[0;1];
[y,t,x]=lsim(sys_RK_2DOF,ud,t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,x(:,1),t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');


%% 2DOF-Zustandsregler, jetzt mit Modellfehler plus Störung am Ausgang nach 3
%Sekunden
sys_RK_2DOF=ss(A-B*K_dach,[B zeros(2,1)],C-D*K_dach,[D 1]);
sys_RK_2DOF_dach=ss(A_dach-B_dach*K_dach,B_dach,C_dach-D_dach*K_dach,D_dach);
tf(sys_RK_2DOF_dach) 
[num, den]=tfdata(sys_RK_2DOF_dach);
nenner=den{1}/num{1}(3);
yd=sin(t);
ud=nenner(3)*sin(t)+nenner(2)*cos(t)-nenner(1)*sin(t);
x0=[0;1];
z=[zeros(301,1); ones(700,1)];
[y,t,x]=lsim(sys_RK_2DOF,[ud,z],t,x0);
close all;
figure(1); %Zeitverlaufsbild
plot(t,y,t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Soll- und Istverlauf in m');
%der Zustandsregler sieht die Ausgangsstörung nicht und kann sie daher
%nicht bekämpfen, auch wenn er sie sehen würde, ist er nur ein P-Regler und
%würde i.Allg. keine stationäre Genauigkeit erreichen 


%% Um Ausgangsstörung und Modellfehler kompensieren zu können, wird eine
%Ausgangsrückführung mit PI-Regler benötigt
%Reglerentwurf wieder mit fehlerbehaftetem Modell
K_pireg=lqr([A_dach zeros(2,1);C_dach 0],[B_dach; D_dach],blkdiag(Q,1),R)
K_x=K_pireg(1:2); K_xi=K_pireg(3);
%System für Simulation aus Original-Strecke und eben entworfenem Regler
%mit den Eingängen ud,yd,z 
sys_RKPI=ss([A-B*K_x -B*K_xi; C-D*K_x -D*K_xi],[[B, zeros(2,1); D -1] [zeros(2,1);1]],[C-D*K_x -D*K_xi], [D 0 1]);
%Vorsteuerung berechnen anhand fehlerbehaftetem Modell 
sys_RK_vorst_dach=ss(A_dach-B_dach*K_x,B_dach,C_dach-D_dach*K_x,D_dach);
tf(sys_RK_vorst_dach) 
[num, den]=tfdata(sys_RK_vorst_dach);
nenner=den{1}/num{1}(3);
%für Sollsignal yd = sin(t):
yd=sin(t);
ud=nenner(3)*sin(t)+nenner(2)*cos(t)-nenner(1)*sin(t);
%Simulation System mit Vorsteuerung 
%(sowohl Regler als auch Vorsteuerung mit fehlerbehaftetem Modell entworfen)
x0=[0;1];
%Ohne Störung -> Modellfehler führen zu Abweichung, da I-Regler für sinus
%nicht optimal
z = zeros(1001,1);
%Mit Störung wie oben -> Störung wird durch Ausgangsrückführung mit
%I-Anteil weggeregelt (hierfür nachfolgende Zeile aktivieren)
%z=[zeros(31,1); ones(110,1)];

[y,t,x]=lsim(sys_RKPI,[ud,yd,z],t,[x0;0]); %Integratoranfangswert auf null
close all;
figure(1); %Zeitverlaufsbild
plot(t,y,t,yd,'linewidth',2);
xlabel('Zeit in s');
ylabel('Weg in m und Geschwindigkeit in m/s');


%% Das Ganze nun mit Störgrößenaufschaltung /-reduktion
% hier ist der fleißige Studierende gefragt

