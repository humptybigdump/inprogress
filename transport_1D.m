% =========================================================================
% 1-D Simulation of Solute Transport - Simple Version 
% Olaf A. Cirpka
% University of Tübingen
% Department of Geosciences
% olaf.cirpka@uni-tuebingen.de
%
% June 19, 2024
% =========================================================================

close all
clear all
clc

% Transport Coefficients
L  = 1;           % length of column [m]
r  = 0.05;        % radius of column [m]
A = pi*r^2;       % cross-sectional area [m2]
Q = 1e-4/60;      % discharge 100 ml/min in m3/s
q  = Q/A;         % Darcy velocity [m/s]
poros = 0.4;      % porosity [-]
alpha = .005;     % dispersivity [m]
Dp = 1e-9;        % pore diffusion coefficient [m2/s]

tinj=3600*1;      % time of solute injection [s]
te = 3600*2;      % end time [s]
t_output=60;      % time increment for graphical output [s]

% Derived Coefficients
v    = q/poros;    % seepage velocity [m/s]
D    = alpha*v+Dp; % dispersion coefficient [m2/s]
t_PV = L/v;        % time for one pore volume [s]

% Spatial resolution
dx = 0.01;         % [m]
% Solve for dt to meet v*dt = dx
dt = dx/v;

% Spatial Discretization
x=[0.5*dx:dx:L];
nx = length(x);

% Dispersion Matrix
M = spdiags(ones(nx,1)*[-D*dt/dx^2, 1 + 2*D*dt/dx^2, -D*dt/dx^2],...
            -1:1,nx,nx);
M(1,1:2)=[1 0];
M(nx,nx-1:nx)=[-D*dt/dx^2,1+D*dt/dx^2];

% Number of Components
ncomp = 1;

% Matrix of Aqueous Concentrations
% Rows related to length coordinates
% Columns related to components
c = zeros(nx,ncomp);

% initialize breakthrough curve
BTC=zeros(0,ncomp);
% Open figure and delete its content
figure(1);clf
% =========================================================================
% Loop over all timepoints
% =========================================================================
for t=dt:dt:te

    % Inflow concentration [mmol/L]
    if t<tinj
        c_in = [1];
    else
        c_in = [0];
    end
    
    BTC=[BTC;c(end,:)];
    
    % =====================================================================
    % ADVECTION
    % =====================================================================
    % Advection at Courant-number 1 implies that the concentrations are
    % moved by exactly one box. The values in the last box are moved out.
    % The first box receives the inflow concentration.
    c(2:end,:)=c(1:end-1,:);
    c(1,:)=c_in;
    
    % =====================================================================
    % DISPERSION
    % =====================================================================
    % Implicit Euler
    c = M\c;
        
    % =====================================================================
    % REACTION
    % =====================================================================
    
    % =====================================================================
    % GRAPHICAL OUTPUT
    % =====================================================================
    % Graphical output
    if mod(t,t_output)<=dt
       figure(1)
       plot(x,c);
       xlabel('x [m]');
       ylabel('c [mmol/L]');
       ylim([0 1.1]);
       title(sprintf('Concentration, t=%6.1fh',t/3600));
       drawnow
    end
end
 
figure(2)
plot([dt:dt:te]/3600,BTC)
ylim([0 1.1]);
xlabel('t [h]')
ylabel('c [mmol/l]')
title('Breakthrough Curve')
