close all;
%% Signale simulieren/messen
global t;
global u;
global y;

T_A = 1; %Abtastzeit sec
y_e = 5; %Ruhelage
u_e = 0;

% Systemparameter
k = 0.5; % Federsteifigkeit in N/m
m = 100; % Masse in kg
c = 1;   % D‰mpfung in N*s/m

%Anfangswert
x_0_mess = [5, 0]';

% Simulation Kleinsignalverhalten um Ruhelage
x_0 = x_0_mess - [y_e; 0];
t = (0:T_A:999)';
u = [ones(size(t,1)/4,1); -ones(size(t,1)/4,1); 
     ones(size(t,1)/4,1); -ones(size(t,1)/4,1)];
system = ss([0 1; -k/m -c/m], [0; 1/m], [1 0], 0);
y = lsim(system, u, t, x_0);
%y = y + 0.5*randn(size(t,1),1); %Messrauschen

% Groﬂsignalverhalten (Arbeitspunkt hinzu addieren)
u_mess = u + u_e;
y_mess = y + y_e;

% Plotten
figure;
subplot(1,2,1);
plot(t,u_mess,'LineWidth',2);
xlabel('t');
ylabel('u_{mess}');

subplot(1,2,2);
plot(t,y_mess,'LineWidth',2);
xlabel('t');
ylabel('y_{mess}');

