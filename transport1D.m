close all
clear all
clc

% Define the domain and grid
xnod = 0:1:200;       % coordinates of nodes [m]
nnod = length(xnod);  % number of nodes

% Define elements with properties
el= [(1:nnod-1)',(2:nnod)']; % incidence matrix nel x 2 (nel=nnod-1)
nel = nnod-1;

% coefficients
v = 1/86400;      % velocity [m/s]
D = 0.01*v;       % dispersion coefficient [m2/s]
c0=zeros(nnod,1); % initial concentration [kg/m3]
cin=1;            % inflow concentration [kg/m3]

% time discretization
dt = 43200;   % timestep size [s]
nt = 550;     % number of timesteps
Theta = 0.5;  % time-weighting (0: fully explicit; 1: fully implicit)

% Setting up matrices
[Mstor,Mmob]=globmattrans(xnod,el,v,D);

% Assemble system of equations
Mleft  = 1/dt*Mstor + Theta*Mmob;
Mright = 1/dt*Mstor + (Theta-1)*Mmob;

Mmod=Mleft;

% initialization
c = c0;
% time loop
for it=1:nt
    % right-had side vector due to transient transport
    rhs=Mright*c;
    % consider inflow boundary
    rhs(1) = rhs(1) + cin*v;
    rmod = rhs;
    % solve system of equations
    c = Mmod\rmod;
    % plot results
    plot(xnod,c);
    xlabel('x [m]')
    ylabel('c [kg/m^3]')
    drawnow
end

% Global matrices for transport
function [Mstor,Mmob]=globmattrans(x,el,v,D)
nel=size(el,1); % number of elements
nnod=length(x); % number of nodes

% initialization
ivec=zeros(nel*4,1);
jvec=zeros(nel*4,1);
a_stor=zeros(nel*4,1);
a_mob=zeros(nel*4,1);
for iel=1:nel
    % length of element
    L=abs(x(el(iel,1))-x(el(iel,2)));
    % get local matrics
    [Mstor_loc,Mmob_loc]=locmattrans(L,v,D);
    % put into global matrices
    ivec((iel-1)*4+(1:4))= [el(iel,1);el(iel,2);el(iel,1);el(iel,2)];
    jvec((iel-1)*4+(1:4))= [el(iel,1);el(iel,1);el(iel,2);el(iel,2)];
    a_stor((iel-1)*4+(1:4))=Mstor_loc(:);
    a_mob((iel-1)*4+(1:4)) =Mmob_loc(:);    
end
% convert into sparse matrices
Mstor=sparse(ivec,jvec,a_stor,nnod,nnod);
Mmob=sparse(ivec,jvec,a_mob,nnod,nnod);
% Consider inflow boundary for advection
Mmob(1,1)=Mmob(1,1)+v;
end

% Element-related matrices for transport
function [Mstor_loc,Mmob_loc]=locmattrans(L,v,D)
Mstor_loc=L*[1/3 1/6;1/6 1/3];
Mmob_loc =D/L*[1 -1;-1 1] + v/2*[-1 1;-1 1]; 
end