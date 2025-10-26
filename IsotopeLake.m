clear all
close all
clc
% Computes the concentration of phenol and its isotopes in a pond
% considering Monod-kinetics of microbial degradation and associated
% biomass growth, and dilution. Oxygen is available in excess.
% t: time [d]
% c: concentrations
%    1: conservative tracer [mol/m3]
%    2: isotopically light phenol [mol/m3]
%    3: isotopically heavy phenol [mol/m3]
%    4: biomass [g/m3]
% par: parameters
%    1: mean residence time in the pond [d]
%    2: maximum specific growth rate for turnover of light isotopologe [1/d]
%    3: maximum specific growth rate for turnover of heavy isotopologe [1/d]
%    4: Monod coefficient for light isotopologe [mol/m3]
%    5: Monod coefficient for heavy isotopologe [mol/m3]
%    6: yield coefficient [g/mol]
%    7: biomass decay coefficient [1/d]

% Assumption on fractionation:
% difference only in mumax
epsilon = -2e-3;     % fractionation coefficient [-]
alpha   = 1+epsilon; % fractionation factor [-]

% Standard isotope ratio
C13C12_ref  = 0.0111802;
% initial delta-value
delta0  = -23e-3;
% initial isotope ratio
C13C12_0=(delta0+1)*C13C12_ref;

% Parameters
T       = 432/1e-3/86400;% mean residence time in the pond [d]
mumax12 = 1;             % maximum specific growth rate for turnover of 
                         % light isotopologe [1/d]
mumax13 = alpha*mumax12; % maximum specific growth rate for turnover of
                         % heavy isotopologe [1/d]
K12     = 0.1;           % Monod coefficient for light isotopologe [mol/m3]
K13     = K12;           % Monod coefficient for heavy isotopologe [mol/m3]
Y       = 10;            % yield coefficient [g/mol]
kdec    = 0.1;           % biomass decay coefficient [1/d]
par=[T,mumax12,mumax13,K12,K13,Y,kdec];

% initial concentrationen
Cini  = 80000/94/432;    % total concentration C12+C13 [mol/m3]
C12_0 = Cini/(1+C13C12_0);
C13_0 = Cini*C13C12_0/(1+C13C12_0);
bio_0 = 1e-2;            % [g/m3]

c0 = [Cini;C12_0;C13_0;bio_0];

% time span
tspan = [0 10]; % [d]

% solution of ODE system
[t,c] = ode15s(@IsotopeLakeODE,tspan,c0,[],par);

% postprocessing
tracer = c(:,1);        % tracer concentration [mol/m3]
ctot = c(:,2)+c(:,3);   % total phenol [mol/m3]
relconc = ctot./tracer; % phenol normalyzed by tracer [-]

Delta = c(:,3)./c(:,2)/C13C12_ref-1;

figure(1)
tt=tiledlayout(3,1,'TileSpacing','compact');
nexttile(1);
plot(t,[tracer,ctot]);
xlabel('t [d]');
ylabel('c [mol/m^3]');
legend('tracer','phenol');
title('Concentrations of Solutes')

nexttile(2)
plot(t,Delta*1000);
xlabel('t [d]');
ylabel('\delta^{13}C [‰]');
title('\delta^{13}C of Phenol')

nexttile(3)
plot(t,c(:,4));
xlabel('t [d]');
ylabel('c_{bio} [g/m^3]');
title('Biomass Concentration')

sgtitle(tt,'Time Series')
set(gcf,'OuterPosition',get(0,'ScreenSize'))

figure(2)
tt=tiledlayout(1,2,'TileSpacing','compact');
nexttile(1);
semilogx(ctot/Cini,Delta*1000);
xlabel('c(t)/c(0) [-]')
ylabel('\delta^{13}C [‰]');
title('\delta^{13}C as Function of c')
axis tight
set(gca,'xgrid','on','ygrid','on')

nexttile(2)
semilogx(relconc,Delta*1000,'x',...
         relconc,(log(relconc)*epsilon+delta0)*1000,'-');
xlabel('c(t)/c_{cons} [-]');
ylabel('\delta^{13}C [‰]');
legend('Simulation','Rayleigh equation');
title('Rayleigh Plot')
axis tight
set(gca,'xgrid','on','ygrid','on')
title(tt,'Isotope Ratios')
set(gcf,'OuterPosition',get(0,'ScreenSize'))

function dcdt = IsotopeLakeODE(t,c,par)
% Computes the concentration of phenol and its isotopes in a pond
% considering Monod-kinetics of microbial degradation and associated
% biomass growth, and dilution. Oxygen is available in excess.
% t: time [d]
% c: concentrations
%    1: conservative tracer [mol/m3]
%    2: isotopically light phenol [mol/m3]
%    3: isotopically heavy phenol [mol/m3]
%    4: biomass [g/m3]
% par: parameters
%    1: mean residence time in the pond [d]
%    2: maximum specific growth rate for turnover of light isotopologe [1/d]
%    3: maximum specific growth rate for turnover of heavy isotopologe [1/d]
%    4: Monod coefficient for light isotopologe [mol/m3]
%    5: Monod coefficient for heavy isotopologe [mol/m3]
%    6: yield coefficient [g/mol]
%    7: biomass decay coefficient [1/d]

dcdt=zeros(size(c));
tracer  = c(1);
C12     = c(2);
C13     = c(3);
bio     = c(4);
T       = par(1);
mumax12 = par(2);
mumax13 = par(3);
K12     = par(4);
K13     = par(5);
Y       = par(6);
kdec    = par(7);

growth12 = mumax12*C12/K12/(1+C12/K12+C13/K13)*bio;
growth13 = mumax13*C13/K13/(1+C12/K12+C13/K13)*bio;

dcdt(1) = -tracer/T;            % tracer: only dilution
dcdt(2) = -C12/T - growth12/Y;  % C12-phenol: dilution and decay
dcdt(3) = -C13/T - growth13/Y;  % C13-phenol: dilution and decay
dcdt(4) = growth12+growth13-(kdec+1/T)*bio; % Biomass: dilution, growth and decay
end