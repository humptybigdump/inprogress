
%% Matlab-Lösung zu Übungsaufgaben Beobachterentwurf
close all;

%% 1 Zustandsbeobachter 
%% 1 a) System simulieren
A = [-5 1 1; 1 -4 2; 2 3 -5];
B = [1; 2; 3];
C = [1 1 1];
D = 0;
sys = ss(A,B,C,D);
n = size(A,1);  %Systemordnung
x_0 = [2; 3; 4];

delta_T = 0.001;
% Sprungantworten des Systems mit Anfangswert verschieden von 0
t = [0:delta_T:10]';
u = zeros(length(t),1); u(1000:5000)=1; u(7500:end)=1;
[y, t, x] = lsim(sys,u,t,x_0);

plot(t,u); hold on;
xlabel('t');
title('Antwort der Strecke auf Sprünge');
plot(t,y,'linewidth',2);
plot(t,x);
legend('u','y', 'x1', 'x2', 'x3');


%% 1 b) Untersuchung der Beobachtbarkeit über Kalmansche Beobachtbarkeitsmatrix
Q_B = [C; C*A; C*A^2];
% voller Rang (=n) heißt vollständig beobachtbar
rank(Q_B)
% Nullraum von Q_B liefert den Unbeobachtbarkeitsunterraum (hier leer)
null(Q_B)

%% 1 c) Umformung in Beobachtungsnormalform
% Variante 1: Übertragungsfunktion berechnen und Polynomkoeffizienten gemäß
% Beobachtungsnormalform in Matrizen eintragen (ginge auch symbolisch)
 [Num, Den]=tfdata(sys);
 Num = Num{1};
 Den = Den{1};
 
 A_BNF = [0 0 -Den(n+1); 1 0 -Den(n); 0 1 -Den(n-1)];
 B_BNF = [Num(n+1)-Den(n+1)*Num(1); Num(n)-Den(n)*Num(1); Num(n-1)-Den(n-1)*Num(1)];
 C_BNF = [0 0 1];
 D_BNF = Num(1);
 sys_BNF = ss(A_BNF, B_BNF, C_BNF, D_BNF);
 
%% 1 d) Umformung in Beobachtungsnormalform  
 %Variante 2: durch Ähnlichkeitstransformation
 P = inv(obsv(A,C));
 T_BNF = inv(ctrb(A,P(:,n)));
 sys_BNF_2 = ss2ss(sys,T_BNF);
 
 %Zum Spaß auch noch Regelungsnormalform berechnen
 Q = inv(ctrb(A,B));
 T_RNF = obsv(A, Q(3,:));
 sys_RNF = ss2ss(sys,T_RNF);
  
 %% 1 e) Beobachterentwurf mit Polvorgabe
 % Wunscheigenwerte des Beobachters
 p = [-15, -16, -17]';
  
 % Annahme: Modell entspricht exakt dem realen System:

 % Variante 1: Nutzen der Beobachtungsnormalform 
 % - der Beobachter besitzt die Systemmatrix A_B = A_BNF-L_BNF*C_BNF
 % - in der BNF enthält die letzte Spalte von A_BNF die (mit -1 multiplizierten) Koeffizienten des charakteristischen Polynoms
 % - A_BNF-L_BNF*C_BNF subtrahiert L_BNF von der letzten Spalte (C_BNF = [0...0 1])
 % - die letzte Spalte von A_B besitzt dann die Elemente [(-a_0 - L_BNF_1); (-a_1-L_BNF_2); usw.]
 % - über poly können die Koeffizienten des Polynoms mit den Wunscheigenwerten berechnet werden
 % - daraus kann direkt L_BNF abgelesen werden
 
 
 % Den(n+1) = a_0
 % Den(n)   = a_1
 % Den(n-1) = a_2
 
 koeff = poly(p);
 L_BNF = [-Den(n+1)+koeff(n+1); -Den(n)+koeff(n); -Den(n-1)+koeff(n-1)];
 % Test:
 eig(A_BNF-L_BNF*C_BNF)
 

 %% 1 f) Rücktransformation des Beobachters in Originalkoordinaten:
  L = inv(T_BNF)*L_BNF
% Ergebnis muss gleich sein mit dem unten per place in (g) entworfenen L
  
 %% 1 g) Variante 2: direkt mit Matlab in Originalkoordinaten
 % Reglerentwurf mit Polplatzierung nutzte place(A,B,p) bzw. acker(A,B,p)
 % für Beobachterentwurf wird duales System (A',C') genutzt:
 L = place(A', C', p)'
 % Test:
 eig(A-L*C)
 
 %% 1 h) Beobachter aufbauen und testen:
 A_B = A-L*C;
 B_B = [B-L*D L];      % Beobachter besitzt 2 Eingänge: u und y
 C_B = C;
 D_B = [D 0];
 
 sys_B = ss(A_B, B_B, C_B, D_B);
 
 
 %x_0_B = x_0; %  Beobachteranfangswerte gleich mit Systemanfangswerten   
 x_0_B = [1; 2; 6]; % Beobachteranfangswerte verschieden von Systemanfangswerten
 % gewählte Beobachteranfangswerte sollten zumindest konsistent mit
 % Ausgangsgleichung sein (hier y(0) = x1+x2+x3 = 9)
 [y_B, t, x_B] = lsim(sys_B,[u,y],t, x_0_B);
 
 figure;
 plot(t,x,'--');
 title('System- und Beobachterzustände');
 hold on;xlabel('t');
 plot(t,x_B);
 legend('x1', 'x2', 'x3', 'x1_B', 'x2_B', 'x3_B');
 
  
 %% 2 Regler mit Zustandsrückführung mit -beobachter
 %% 2 a) LQ-Regler entwerfen
 Q=eye(3);
 R=1;
 K = lqr(A,B,Q,R)
 % Vorfilter
 F = inv((C-D*K)*inv(-A+B*K)*B+D)

% Simulation des Zustandsregelkreises ohne Beobachter 
 sys_RK=ss(A-B*K,B*F,C-D*K,D*F);
 % konstanter Sollwert 
 yd=ones(size(t,1),1)*5;
 [y_RK,t,x_RK]=lsim(sys_RK,yd,t,x_0);
  
 figure;
 plot(t,y_RK,'linewidth',2);
 title('Zustandsregelkreis OHNE Beobachter');
 hold on;xlabel('t');
 plot(t,x_RK)
 legend('y', 'x1', 'x2', 'x3');
 
 %% b) Variante 1: Simulation des gesamten Regelkreises mit Beobachter (Regler, Beobachter und Strecke in einem großen System)
 % Nur für Simulation geeignet (siehe Folie 17), da später Strecke nicht als Modell, sondern konkret vorliegt
  
 % Zustandsvektor x_RK = [x, x_B]
 A_RK = [A, -B*K;  L*C, A-L*C-B*K];
 B_RK = [B*F; B*F];
 C_RK = [C -D*K];
 D_RK = [D*F];
 
 sys_RK = ss(A_RK, B_RK, C_RK, D_RK);
 [y_RK,t,x_RK]=lsim(sys_RK,yd,t,[x_0; x_0_B]);
  
 figure;
 plot(t,y_RK,'linewidth',2);
 title('Zustandsregelkreis MIT Beobachter');
 hold on;xlabel('t');
 plot(t,x_RK)
 legend('y', 'x1', 'x2', 'x3');
 
 
 %% c) Variante 2: Zustandsregler mit Beobachter separat erstellen und erst anschließend für Simulation an die Strecke anbinden
 % siehe Folie 25
 % Zustandsregler mit Beobachter:
 % Eingang: [y_d, y]
 % Ausgang: u
 % Zustandsvektor: x_B
 A_RB = [A-L*C-(B-L*D)*K];
 B_RB = [(B-L*D)*F, L];
 C_RB = [-K];
 D_RB = [F, 0];
 sys_RegBeob = ss(A_RB, B_RB, C_RB, D_RB);

  % Geschlossenen Regelkreis aufbauen 
 % Regelstrecke um Durchgriff erweitern, so dass erweiterets System sowohl
 % y also auch y_d als Ausgang hat
 sys_Durchgriff = ss(0,0,0,1);
 sys_erweitert = append(sys_Durchgriff, sys);
 feedin = 2;
 feedout = [1 2];
 Cloop = feedback(sys_erweitert, sys_RegBeob, feedin, feedout, +1);
 
 % erster Anfangswert für Durchgriff=0
 [y_RK,t,x_RK]=lsim(Cloop,[yd, zeros(length(t),1)],t,[0; x_0; x_0_B]);
  
 figure;
 plot(t,y_RK(:,2),'linewidth',2);
 title('Zustandsregler mit Beobachter an Strecke');
 hold on;xlabel('t');
 plot(t,x_RK(:,2:7));
 legend('y', 'x1', 'x2', 'x3', 'x1_B', 'x2_B', 'x3_B');
 
 
 %% 3 Zustandsbeobachter bei Modellfehlern
 %% a) Streckenmodell mit Modellfehlern:
 mz = 0.5; %Parameter, um Stärke der Modellfehler anzugeben
 A_D = A + rand(size(A))*mz; 
 B_D = B + rand(size(B))*mz; 
 C_D = C; 
 D_D = D;
 
 %% b) Beobachterentwurf mit Polvorgabe anhand fehlerhaftem Modell
 L = place(A_D', C_D', p)';
  
 % Beobachter aufbauen:
 A_B_D = A_D-L*C_D;
 B_B_D = [B_D-L*D_D L];      % Beobachter besitzt 2 Eingänge: u und y
 C_B_D = C_D;
 D_B_D = [D_D 0];
 
 sys_B_D = ss(A_B_D, B_B_D, C_B_D, D_B_D);
  
 [y_B, t, x_B] = lsim(sys_B_D,[u,y],t, x_0_B);
 
 figure;
 plot(t,x,'--');
 title('System- und Beobachterzustände MIT Modellfehlern');
 hold on;xlabel('t');
 plot(t,x_B);
 legend('x1', 'x2', 'x3', 'x1_B', 'x2_B', 'x3_B');
  % deutliche Abweichungen zwischen tatsächlichen und beobachteten Zuständen
   
  

 
 %% c) PI-Beobachter bei Modell mit Fehlern (nach Söffker et al)
 L_3 = [1; 1; 1];
 A_D_PI = [A_D L_3; zeros(1,4)];
 B_D_PI = [B_D; 0];
 C_D_PI = [C_D 0];
 D_D_PI = D_D;
 L = place(A_D_PI', C_D_PI', [p; -10])';
 
 % Beobachter aufbauen:
 A_B_D = A_D_PI-L*C_D_PI;
 B_B_D = [B_D_PI-L*D_D_PI L];      % Beobachter besitzt 2 Eingänge: u und y
 C_B_D = C_D_PI;
 D_B_D = [D_D_PI 0];
 
 sys_B_D = ss(A_B_D, B_B_D, C_B_D, D_B_D);
 
 [y_B, t, x_B] = lsim(sys_B_D,[u,y],t, [x_0_B; 0]);
 
 figure;
 plot(t,x,'--');
 title('PI-Beobachter: System- und Beobachterzustände MIT Modellfehlern');
 hold on;xlabel('t');
 plot(t,x_B(:,1:4));
 legend('x1', 'x2', 'x3', 'x1_B', 'x2_B', 'x3_B', '\xi');
 % beobachtete Zustände passen trotz Modellfehler recht gut
 
  
 
  
 %% 4 Störgrößenbeobachter 
 B_z = [1;1;1]; % bekannte Wirkung der Störung auf Zustände
 D_z = 2;       % bekannte Wirkung der Störung auf Ausgang
 
 %% a) unbekannte konstante Störung z 
 z=ones(size(t,1),1)*0.5;
 
 % Simulation des gestörten Systems, um y(t) und x(t) zu ermitteln
 % System hat nun zwei Eingänge, u und z
 A_g = A;
 B_g = [B B_z];
 C_g = C;
 D_g = [D D_z];
 sys_g = ss(A_g, B_g, C_g, D_g);
 [y_z, t, x_z] = lsim(sys_g,[u';z'],t,x_0);

  
 %% b) erweiterter Beobachter für konstante Störung
 
 % Störmodell für konstante Störung (Folie 26)
 A_zeta = 0;
 B_zeta = 0;
 C_zeta = 1;
 D_zeta = 0;
  
 
 % erweitertes System mit zusätzlichem Zustand für Störung (Folie 27)
 A_SB = [A B_z*C_zeta; zeros(1,3), A_zeta];
 B_SB = [B; 0];
 C_SB = [C D_z*C_zeta];
 D_SB = D;
 
 % Beobachter für erweitertes System
 L = place(A_SB', C_SB', [p; -10])';
 
 % Beobachter aufbauen:
 A_B = A_SB-L*C_SB;
 B_B = [B_SB-L*D_SB L];      % Beobachter besitzt 2 Eingänge: u und y
 C_B = C_SB;
 D_B = [D_SB 0];
 
 sys_SB = ss(A_B, B_B, C_B, D_B);
 
 
 [y_SB, t, x_SB] = lsim(sys_SB,[u,y_z],t, [x_0_B; 0]);
 
 figure;
 plot(t,x_z,'--');
 title('Beobachter mit Störgrößenbeobachtung bei konstanter Störung');
 hold on;xlabel('t');
 plot(t,z,'--');
 plot(t,x_SB);
 legend('x1', 'x2', 'x3', 'z', 'x1_B', 'x2_B', 'x3_B', '\zeta');

  % sowohl den Zuständen x1, x2, x3 als auch der konstanten Störung z folgt
  % der erweiterte Beobachter nach kurzer Zeit perfekt  
 
 
  %% c) Signale für unbekannte sinusförmige Störung z
 w = 4;  % bekannte Kreisfrequenz
 Amp = 0.5;   % unbekannte Amplitude
 phi = 3; % unbekannte Phase 0..2pi
 z = Amp*sin(w*t+phi);
 B_z = [1;0;0]; % bekannte Wirkung der Störung auf Zustände
 D_z = 1;       % bekannte Wirkung der Störung auf Ausgang
 
 
 % Simulation des gestörten Systems
 A_g = A;
 B_g = [B B_z];
 C_g = C;
 D_g = [D D_z];
 sys_g = ss(A_g, B_g, C_g, D_g);
 [y_z, t, x_z] = lsim(sys_g,[u';z'],t,x_0);

 
 %% d) erweiterter Beobachter für sinusförmige Störung
 % Störmodell für sinusförmige Störung
 A_zeta = [0 1; -w^2 0];
 B_zeta = 0;
 C_zeta = [1 0];
 D_zeta = 0;
  
 
 % erweitertes System mit zwei zusätzlichen Zuständen xi für Störung
 A_SB = [A B_z*C_zeta; zeros(2,3), A_zeta];
 B_SB = [B; 0; 0];
 C_SB = [C D_z*C_xi];
 D_SB = D;
 
 % Beobachter für erweitertes System
 L = place(A_SB', C_SB', [p; -10; -11])';
 
 % Beobachter aufbauen:
 A_B = A_SB-L*C_SB;
 B_B = [B_SB-L*D_SB L];      % Beobachter besitzt 2 Eingänge: u und y
 C_B = C_SB;
 D_B = [D_SB 0];
 
 sys_SB = ss(A_B, B_B, C_B, D_B);
 
 
 [y_SB, t, x_SB] = lsim(sys_SB,[u,y_z],t, [x_0_B; 0; 0]);
 
 figure;
 plot(t,x_z,'--');
 title('Beobachter mit Störgrößenbeobachtung bei Sinusstörung');
 hold on;xlabel('t');
 plot(t,z,'--');
 plot(t,x_SB);
 legend('x1', 'x2', 'x3','z', 'x1_B', 'x2_B', 'x3_B', '\zeta_1', '\zeta_2');

 z_SB = x_SB(:,4); %Beobachtete Störung
 
 
 %% Zusatz: Rückrechnen auf Amplitude und Phase
 zeta = x_SB(:,4:5);

 %Amplitude Signale zeta_1 = Amp*sin(wt+phi) und zeta_2 = Amp*w*cos(wt+phi)
 %quadrieren und nach Amp auflösen
 Amp_SB = mean(sqrt(zeta(:,1).^2+1/w^2*zeta(:,2).^2))

 %Phase: Signale zeta_1 = Amp*sin(wt+phi) und xi_2 = Amp*w*cos(wt+phi)
 %dividieren und nach phi auflösen
 eps = 0.001;
 phi = mod(atan2( w.*zeta(:,1), xi(:,2) ) - w.*t(:),2*pi);
 phi(phi<(-2*pi+eps)) = phi(phi<(-2*pi+eps))+2*pi;
 phi(phi>(2*pi-eps)) = phi(phi>(2*pi-eps))-2*pi;
 phi_SB = mean(phi)
 
  
%% 5 Reduzierter Störgrößenbeobachter für sinusförmige Störung z (gestörte Systemzustände x_z sind alle bekannt/messbar)
%  
%% a) 
% erweitertes System mit zu beobachtenden Zuständen (hier nur die Störzustände zeta)
 A_RSB = [A_zeta];
 B_RSB = [zeros(2,1) zeros(2,3)];
 C_RSB = [D_z*C_zeta];
 D_RSB = [D C];
 
 % Beobachterentwurf
 L = place(A_RSB', C_RSB', [-10; -11])';
 
 % Beobachter aufbauen:
 A_B = A_RSB-L*C_RSB;
 B_B = [B_RSB-L*D_RSB L];      % Beobachter besitzt 2 Eingänge: u und y
 C_B = C_RSB;
 D_B = [D_RSB 0];
 
 sys_RSB = ss(A_B, B_B, C_B, D_B);
 
 [y_RSB, t, x_RSB] = lsim(sys_RSB,[u,x_z,y_z],t, [0; 0]);
 
 figure;
 plot(t,x,'--');
 title('Reduzierter Beobachter, nur Störgrößenbeobachtung bei Sinusstörung');
 hold on;xlabel('t');
 plot(t,x_RSB);
 legend('x1', 'x2', 'x3', '\zeta_1', '\zeta_2');
 
 z_RSB = x_RSB(:,1);

 
 % Rückrechnen auf Amplitude und Phase
 zeta = x_RSB;
 
 %Amplitude Signale zeta_1 = Amp*sin(wt+phi) und zeta_2 = Amp*w*cos(wt+phi)
 %quadrieren und nach Amp auflösen
 Amp_RSB = mean(sqrt(zeta(:,1).^2+1/w^2*zeta(:,2).^2))

 %Phase: Signale zeta_1 = Amp*sin(wt+phi) und zeta_2 = Amp*w*cos(wt+phi)
 %dividieren und nach phi auflösen
 eps = 0.001;
 phi = mod(atan2( w.*zeta(:,1), zeta(:,2) ) - w.*t(:),2*pi);
 phi(phi<(-2*pi+eps)) = phi(phi<(-2*pi+eps))+2*pi;
 phi(phi>(2*pi-eps)) = phi(phi>(2*pi-eps))-2*pi;
 phi_RSB = mean(phi)
 
 
 %% b) Vergleich Störgrößenbeobachter und reduzierter Beobachter
 figure;
 plot(t(1:2000),z(1:2000));
 title('Vergleich Beobachter und reduzierter Beobachter');
 hold on; xlabel('t');
 plot(t(1:2000),z_SB(1:2000));
 plot(t(1:2000),z_RSB(1:2000));
 legend('z', 'z_{SB}', 'z_{RSB}');
 
 
  
  