% Script for 2-D groundwater flow using FEM
close all
clear all
clc

disp([char(datetime('now')) ': read grid'])
% Reading in the grid
load mygreatgrid.mat
% vert (nnod x 2): coordinates of all nodes
% etri (nedge x 2): list of edges belonging to boundaries
% tria (nelem x 3): list of triangles
% tnum (nelem x 1): which element belongs to which part
% wellnode: node containing the well
% edge_inter: edges at the interface between part 1 and part 2

% transfer the triangulation to a triangualtion object
TR=triangulation(tria,vert(:,1),vert(:,2));
% plot the grid
triplot(TR,'color',[.9 .9 .9])
% determine the outer boundary
F = freeBoundary(TR);
% plot the outer boundary
hold on
plot(vert([F(:,1);F(end,2)],1),vert([F(:,1);F(end,2)],2),'k','linewidth',2)
hold off
daspect([1 1 1])
xlabel('x [m]')
ylabel('y [m]')
drawnow

% get numbers of vertices and elements
nnod = size(vert,1);
nelem = size(tria,1);

% Define coefficients
T1 = 1e-3;  % transmissivity of part 1 [m2/s]
T2 = 2e-3;  % transmissivity of part 2 [m2/s]
S1 = 1e-4;  % storage coefficient of part 1 [-]
S2 = 1e-4;  % storage coefficient of part 2 [-]
% Assign coefficients to elements
T = T1*ones(nelem,1);
T(tnum==2)=T2;
S = S1*ones(nelem,1);
S(tnum==2)=S2;

% Get in- and outflow nodes (Dirichlet B.C.)
innod = find(abs(vert(:,1))<0.01);
outnod = find(abs(vert(:,1)-1000)<0.01);

hin = 30;            % head at inflow boundary [m]
hout= 20;            % head at outflow boundary [m]

recharge = ones(nelem,1)*0.15/365/86400; % recharge for each element [m/s]
Qwell = -1000/86400; % pumping rate of the well [m3/s]

disp([char(datetime('now')) ': assemble matrices'])
% Set up matrices without boundary conditions
[Mstore,Mmob,Mrech]=globalmatrices(vert,tria,T,S);

% Combine matrices (if needed)
Mleft = Mmob;

% Consider recharge
r = Mrech*recharge; % initialize right-hand side vector with nodal loads 
                    % by recharge
% Consider the well
r(wellnode) = r(wellnode) + Qwell;

% Consider boundary conditions
disp([char(datetime('now')) ': consider boundary conditions'])
Mmod = Mleft;
rmod = r;
for ii=1:length(innod)
    row = zeros(1,nnod);
    row(innod(ii)) = 1;
    Mmod(innod(ii),:)= row;
    rmod(innod(ii)) = hin;
end
for ii=1:length(outnod)
    row = zeros(1,nnod);
    row(outnod(ii)) = 1;
    Mmod(outnod(ii),:)= row;
    rmod(outnod(ii)) = hout;
end

% Solve system of equations
disp([char(datetime('now')) ': solve system of equations'])
h = Mmod\rmod;

% compute nodal loads
load = Mleft*h;

% plot results
disp([char(datetime('now')) ': plot results'])
hold on
[CS,hand]=tricont(vert(:,1),vert(:,2),tria,h,50);
set(hand,'linewidth',1)
hold off
set(gca,'Layer','top')
colormap turbo
cb=colorbar;
ylabel(cb,'h [m]')
