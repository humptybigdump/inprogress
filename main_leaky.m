% Script for 1-D groundwater flow using FEM
close all
clear all
clc

% Define nodes by their coordinates
dx  = 1;      % grid spacing [m]
nel = 400;    % number of elements
nnod = nel+1; % numner of elements
xnod = 0:dx:dx*nel; % nodal coordinates

% Define elements by incidence matrix (nel x 2)
incidence = [(1:nel)',(2:nel+1)'];

% Define coefficients
K = ones(nel,1)*1e-4;  % hydraulic conductivity [m/s]
S0 = ones(nel,1)*1e-5; % specific storativity [1/m]
A = ones(nel,1)*10*100;% cross-sectional area [m^2]
L = 1e-6/0.2*100*ones(nel,1); % leakance = (conductivity of leaky layer)*(width of leaky
                              % layer)/(thickness of leaky layer) [m/s]
% no leakage in the middle
L(181:220) = 0;
hleft = 21;            % head at left boundary [m]
hright= 20;            % head at right boundary [m]
href = ones(nnod,1)*hright;
href(1:181)=hleft;

dt = 2;                % time step [s]
nt = 120;              % number of time steps

% Set up matrices without boundary conditions
[Mstore,Mmob,Mleak]=globalmatrices_leaky(xnod,incidence,K,S0,A,L);

% Combine matrices (if needed)
Mleft = Mmob + Mstore/dt + Mleak;
Mright = Mstore/dt;

% initial condition
h = ones(nnod,1)*hright;

% time loop
for it=1:nt
    % right-hand side vector
    r = Mright*h + Mleak*href;
    % Solve system of equations
    h = Mleft\r;
    % plot results
    plot(xnod,h)
    xlabel('x [m]')
    ylabel('h [m]')
    ylim([hright,hleft])
    title(sprintf('t = %i s',it*dt))
    drawnow
end