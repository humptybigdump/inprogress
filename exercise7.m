% Modeling of Reactions, Micobial Dynamics, and Bioreactive Transport
% Summer Semester 23
% Olaf A. Cirpka
% Solution to Problems 5 & 7
clear all
close all
clc

Vtot = 0.01;                     % total volume [m3]
frac_w = 0.75;                   % fraction of water
rho_res = 1500;                  % density of resin [kg/m3]
s_max = 10;                      % specific sorption capacity [mol/kg]
K_A = 500;                       % half-saturation conc. A [mol/m3]
K_B = 5000;                      % half-saturation conc. B [mol/m3]
c_A_ini = 1000;                  % initial concentration A [mol/m3]
c_B_inj = 1e4;                   % injected concentration B [mol/m3]


V_w = Vtot*frac_w;               % volume of water
m_res = Vtot*(1-frac_w)*rho_res; % mass of the resin [kg]

% Question 1: Initial sorbed concentration and masses
s_A_ini = c_A_ini*s_max/(K_A+c_A_ini);
m_A_ini = s_A_ini*m_res + c_A_ini*V_w;

disp('Exercise 5, Answers to Question 1')
fprintf('initial sorbed conc. A %0.3g mol/kg\n',s_A_ini);
fprintf('initial total mass   A %0.3g mol\n',m_A_ini);

% Question 2: Reequilibration after replacing the aqueous solution
m_A = s_A_ini*m_res;             % total mass of compound A 
m_B = V_w*c_B_inj;               % total mass of compound B

disp(' ')
disp('Go on to Question 2')
fprintf('total mass A %g mol\n',m_A);
fprintf('total mass B %g mol\n',m_B);

% initial guess
c_A = 0;
c_B = c_B_inj;

c_A_old = c_A_ini;
c_B_old = 0;

iter = 0; % iteration index (only for curiosity)

% Picard iteration
while ((c_A-c_A_old)^2+(c_B-c_B_old)^2 > 1e-5)
      iter = iter+1;
      sum_ci_over_Ki = c_A/K_A+c_B/K_B;
      c_A_old = c_A;
      c_B_old = c_B;
      c_A = m_A/(V_w + m_res*s_max/K_A/(1+sum_ci_over_Ki));
      c_B = m_B/(V_w + m_res*s_max/K_B/(1+sum_ci_over_Ki));
end
fprintf('%2.2i iterations needed to compute new equilibrium:\n',iter)
fprintf('c_A = %12.4g mol/m3, c_B = %12.4g mol/m3\n',[c_A,c_B]);

% Now compute the sorbed mass explicitly
sum_ci_over_Ki = c_A/K_A+c_B/K_B;
s_A_eq = c_A*s_max/K_A/(1+sum_ci_over_Ki);
s_B_eq = c_B*s_max/K_B/(1+sum_ci_over_Ki);
fprintf('s_A = %12.4g mol/kg, s_B = %12.4g mol/kg\n',[s_A_eq,s_B_eq]);

% Exercise 7: kinetic mass transfer
% ODE system
% vector of unknowns
% c(1): c_A
% c(2): s_A
% c(3): c_B
% c(4): s_B
disp(' ')
disp('Exercise 7, kinetic mass transfer')
% mass transfer coefficient as seen from the sorbing phase
kmt_s  = [1 2]; % [1/h]
% mass transfer coefficient as seen from the aqueous phase
kmt_a = kmt_s*m_res/V_w; % [kg/m3/h]
% time span
tspan=[0 4*max([1/kmt_a(1),1/kmt_s(1),1/kmt_a(2),1/kmt_s(2)])];
% initial condition
C0 = [0,s_A_ini,c_B_inj,0];
% solve ODE system
[T,C]=ode15s(@myode,tspan,C0,[],kmt_a,kmt_s,K_A,K_B,s_max);

% graphical output
tiledlayout('flow')
nexttile
yyaxis left
hl=plot(T,C(:,[1 3]));
ylabel('c [mol/m^3]')
xlabel('t [h]')
hold on
hm=plot(tspan(2)*[1 1],[c_A c_B],'xk');
hold off

yyaxis right
hr=plot(T,C(:,[2 4]));
ylabel('s [mol/kg]')
hold on
hm=plot(tspan(2)*[1 1],[s_A_eq s_B_eq],'xk');
hold off

% time to reach 99% of equilibrium
t_99_A=interp1((C(:,1)-C(end,1))/(C(1,1)-C(end,1)),T,0.01);
t_99_B=interp1((C(:,3)-C(end,3))/(C(1,3)-C(end,3)),T,0.01);
fprintf('99%% equilibration of compound A after %5.3fh\n',t_99_A)
fprintf('99%% equilibration of compound B after %5.3fh\n',t_99_B)
xline(t_99_A,':k')
xline(t_99_B,'.-k')
legend([hl;hr;hm],'c_A','c_B','s_A','s_B','equilibrium')
title('Kinetic Mass Transfer of Competing Sorbents on a Resin')

function dydt = myode(t,y,kmt_a,kmt_s,K_A,K_B,s_max)
% dydt: rate-of-change vector
% t    : time [h]
% y    : vector of dynamic state variables
%     1: aqueous-phase concentration of compound A, c_A [mol/m3]
%     2: sorbing-phase concentration of compound A, s_A [mol/kg]
%     3: aqueous-phase concentration of compound B, c_B [mol/m3]
%     4: sorbing-phase concentration of compound B, s_B [mol/kg]
% kmt_a: mass-transfer coefficients as seen from the aqueous phase [kg/m3/h]
% kmt_s: mass-transfer coefficients as seen from the sorbing phase [1/h]
% K_A  : half-saturation concentration of compound A [mol/m3]
% K_B  : half-saturation concentration of compound B [mol/m3]
% s_max: sorption capacity [mol/kg]
c_A=y(1);
s_A=y(2);
c_B=y(3);
s_B=y(4);
s_free=s_max-s_A-s_B;
dcA_dt = kmt_a(1)*(s_A-c_A/K_A*s_free);
dsA_dt = kmt_s(1)*(c_A/K_A*s_free-s_A);
dcB_dt = kmt_a(2)*(s_B-c_B/K_B*s_free);
dsB_dt = kmt_s(2)*(c_B/K_B*s_free-s_B);
dydt=[dcA_dt;dsA_dt;dcB_dt;dsB_dt];
end