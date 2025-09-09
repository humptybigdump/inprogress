% Script for 1-D groundwater flow using FEM
close all
clear all
clc

% Define nodes by their coordinates
dx  = 10;     % grid spacing [m]
nel = 100;    % number of elements
nnod = nel+1; % numner of elements
xnod = 0:dx:dx*nel; % nodal coordinates

% Define elements by incidence matrix (nel x 2)
incidence = [(1:nel)',(2:nel+1)'];

% Define coefficients
K = ones(nel,1)*1e-4 + sin((0.5:nel)'/nel*2*pi)*8e-5;  % hydraulic conductivity [m/s]
% K = ones(nel,1)*1e-4;  % hydraulic conductivity [m/s]
S0 = ones(nel,1)*1e-5; % specific storativity [1/m]
A = ones(nel,1)*10*100;% cross-sectional area [m^2]
hleft = 21;            % head at left boundary [m]
hright= 20;            % head at right boundary [m]
recharge = zeros(nnod,1)*1e-5; % recharge*width [m^2/s]

dt = 60;               % time step [s]
nt = 720;              % number of time steps

% Set up matrices without boundary conditions
[Mstore,Mmob]=globalmatrices(xnod,incidence,K,S0,A);

% Combine matrices (if needed)
Mleft = Mmob + Mstore/dt;
Mright = Mstore/dt;

% Consider recharge
rec = recharge*dx;   % initialize right-hand side vector with nodal loads 
                   % by recharge
rec(1)   = rec(1)*0.5;
rec(end) = rec(end)*0.5;

% Consider boundary conditions
Mmod = Mleft;
Mmod(1,1:2) = [1, 0];
Mmod(end,end-1:end) = [0, 1];

% initial condition
h = ones(nnod,1)*hright;

% time loop
for it=1:nt
    % right-hand side vector
    r = Mright*h + rec;
    % consider Dirichlet boundary
    r(1) = hleft;
    r(end) = hright;
    % Solve system of equations
    h = Mmod\r;
    % plot results
    plot(xnod,h)
    xlabel('x [m]')
    ylabel('h [m]')
    title(sprintf('t = %i s',it*dt))
    drawnow
end