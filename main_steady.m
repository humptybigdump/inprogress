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
S0 = ones(nel,1)*1e-5; % specific storativity [1/m]
A = ones(nel,1)*10*100;% cross-sectional area [m^2]
hleft = 20;            % head at left boundary [m]
hright= 20;            % head at right boundary [m]
recharge = ones(nnod,1)*1e-5; % recharge*width [m^2/s]

% Set up matrices without boundary conditions
[Mstore,Mmob]=globalmatrices(xnod,incidence,K,S0,A);

% Combine matrices (if needed)
Mleft = Mmob;

% Consider recharge
r = recharge*dx;   % initialize right-hand side vector with nodal loads 
                   % by recharge
r(1)   = r(1)*0.5;
r(end) = r(end)*0.5;

% Consider boundary conditions
Mmod = Mleft;
Mmod(1,1:2) = [1, 0];
Mmod(end,end-1:end) = [0, 1];
r(1) = hleft;
r(end)=hright;

% Solve system of equations
h = Mmod\r;

% compute nodal loads
load = Mleft*h;

% plot results
plot(xnod,h)
xlabel('x [m]')
ylabel('h [m]')
