% MATLAB script transverse_mix_plume_instant.m
%
% This script computes 2-D fields of heads and
% stream function values, constructs streamline-oriented grids,
% computes steady-state concentrations, and concentrations of
% reactive compounds undergoing an instantaneous reaction
%
% written by 
%
% Olaf A. Cirpka
%
% University of Tuebingen
% Center for Applied Geoscience
% Hoelderlinstr. 12
% 72074 Tuebingen
% Germany
% Olaf.Cirpka@uni-tuebingen.de
%
% September 19, 2013
%
%

clear all,close all,clc
% ============== BEGIN INPUT BLOCK ================================================
% number of elements per direction
nx = [200,100];
% grid spacing
dx = [.05,.0125];
% number of stream tubes
ntube = 100;
% number of sections per stream tube
nsec =  200;
% hydraulic conductivity of the matrix
K1 = 1e-4;
% hydraulic conductivity of the inclusion
K2 = 1e-3;
% variance of log-conductivity
varY=2;
% head difference
phiin = nx(1)*dx(1)*0.01;
% transport parameter
poros = 0.3;
al    = 0.01;
at    = 0.001;
Dp    = 1e-9;

% ============== END INPUT BLOCK ==================================================

% Generate the field
% Spatial coordinates
[X,Y]=meshgrid([0:nx(1)]*dx(1),[0:nx(2)]*dx(2));
% conductivity of the matrix
K=ones(nx(2),nx(1))*K1;
% conductivity of the inclusion
K(floor(nx(2)*.4+1):floor(nx(2)*.6+1),floor(nx(1)*.3+1):floor(nx(1)*.7+1))=K2;

% Output
figure(1)
colormap('jet')
set(gcf,'outerposition',get(0,'screensize'))
subplot(3,1,1)
pcolor(X,Y,log10([K K(:,1);K(1,:) K(1,1)]));
shading flat;
xlim([0,nx(1)*dx(1)]);
ylim([0,nx(2)*dx(2)]);
box on;
daspect([1 1 1]);
xlabel('x_1');ylabel('x_2');
cb=colorbar;
ylabel(cb,'log_{10} K (K in m/s)')
title('log-conductivity field')
set(gca,'outerposition',[0 2/3+0.025 1 1/3-0.025])
drawnow;
% ============== END FIELD GENERATION BLOCK =======================================

% ============== BEGIN HEAD CALCULATION ===========================================
% stiffness matrix of a single element
disp([datestr(clock) ': Set up System of Equations for Head']);
M_h_el = calc_h_stiff_el(dx(2),dx(1));
% stiffness matrix of entire system
M      = sparprep(K,M_h_el);
% number of nodes
nnod = prod(nx+1);
% righthand side vector
r = zeros(nnod,1);
% in- and outflow nodes
innod  = [1:nx(2)+1];
outnod = innod + nx(1)*(nx(2)+1);
% set Dirichlet boundary condition
[Mmod,rmod]=gwdiri(M,r,[innod outnod],[phiin*ones(1,nx(2)+1) zeros(1,nx(2)+1)]);

% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mmod);
disp([datestr(clock) ': Solve for Head']);
% h     = bicgstab(Mmod,rmod,1e-12,10*nnod,L,U);
h     = Mmod\rmod;
% remove roundoff errors of inflow and outflow nodes
h(innod)=phiin;
h(outnod)=0;

Qin = sum(M(innod,:)*h);
disp([datestr(clock) sprintf(': Qin = %g m2/s',Qin)]);
% ============== END HEAD CALCULATION =============================================

% ============== BEGIN STREAM FUNCTION CALCULATION ================================
% stiffness matrix of entire system
disp([datestr(clock) ': Set up System of Equations for Stream Function']);
M    = sparprep(K.^-1,M_h_el);

% righthand side vector
r = zeros(nnod,1);
% in- and outflow nodes
botnod = [1:nx(2)+1:nnod];
topnod = botnod + nx(2);
% boundary condition
[Mmod,rmod]=gwdiri(M,r,[botnod topnod],[zeros(1,nx(1)+1) Qin*ones(1,nx(1)+1)]);

% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mmod);
disp([datestr(clock) ': Solve for Stream Function']);
%psi   = bicgstab(Mmod,rmod,1e-12,10*nnod,L,U);
psi   = Mmod\rmod;
% remove roundoff errors of bottom and top nodes
psi(topnod)=Qin;
psi(botnod)=0;

% ============== END STREAM FUNCTION CALCULATION ==================================
subplot(3,1,2)
h=reshape(h,nx(2)+1,nx(1)+1);
psi=reshape(psi,nx(2)+1,nx(1)+1);
contour(X,Y,psi,[1:49]/50*Qin,'k');
hold on
contour(X,Y,h,100);
hold off
box on;
daspect([1 1 1]);
xlabel('x_1');ylabel('x_2');
caxis([0 phiin]);
colorbar;
title('flow net')
set(gca,'outerposition',[0 1/3+0.025 1 1/3-0.025])
drawnow

% ============== BEGIN GRID CONSTRUCTION ==========================================
disp([datestr(clock) ': Construction of Streamline-Oriented Grid']);
[net,doagain] = slgrid(ntube,nsec,nx,dx,X,Y,psi,h,phiin,Qin);

if doagain
   error('could not construct the streamline-oriented grid')
end
% ============== END GRID CONSTRUCTION ============================================

% ============== BEGIN TRANSPORT PREPARATION ======================================
nnet = ntube*nsec; % number of cells in the net

% streamline oriented grid 2: storage matrix
disp([datestr(clock) ': Evaluate Volume of Streamline-Oriented Elements']);
[area,porarea]=cellarea(net,ntube,nsec,poros);
Mstore = spdiags(porarea,0,nnet,nnet);

% streamline oriented grid 3: mobility matrix
disp([datestr(clock) ': Evaluate Mobility Matrix']);
Mmob = mob_mat(ntube,nsec,Qin,net,al,at,Dp,porarea./area,1);
% ============== END TRANSPORT PREPARATION ========================================
 
% ============== CALCULATE MIXING RATIO ===========================================
% specific discharge per stream tube
invec = zeros(nnet,1);
invec(1:ntube)=Qin/ntube;

is_in = zeros(nnet,1);
is_in(floor(ntube/2+1)+[-15:15])=1;

rmod=invec.*is_in;

% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mmob);
disp([datestr(clock) ': Solve for Mixing Ratio']);
% mixratio   = reshape(bicgstab(Mmob,rmod,1e-12,10*nnod,L,U),ntube,nsec);
mixratio   = reshape(Mmob\rmod,ntube,nsec);

% plotting
subplot(3,1,3)
pcolor(net.x,net.y,[mixratio mixratio(:,end);mixratio(end,:) mixratio(end,end)]);
shading flat;
caxis([0 1])
daspect([1 1 1]);
xlabel('x_1 [m]');ylabel('x_2 [m]');
colorbar;
title('mixing ratio')
set(gca,'outerposition',[0 0+0.025 1 1/3-0.025])
drawnow;

% ============== ANALYZE MIXING RATIO =============================================
% width
delta_y_net=0.5*(net.y(2:end,1:end-1)-net.y(1:end-1,1:end-1) + ...
                 net.y(2:end,2:end  )-net.y(1:end-1,2:end  ));
% center point of the cell
ycen=0.25*(net.y(1:end-1,1:end-1)+net.y(2:end ,1:end-1)+...
           net.y(1:end-1,2:end  )+net.y(2:end ,2:end  ));
% stream-function value in the center
psicen=[.5:ntube]'*ones(1,nsec)*Qin/ntube;
% normal transverse moments
m0 =sum(mixratio.*delta_y_net);
m1 =sum(mixratio.*ycen.*delta_y_net)./m0;
m2c=sum(mixratio.*(ycen-ones(ntube,1)*m1).^2.*delta_y_net)./m0;
% flux-weighted transverse moments
m0psi =sum(mixratio)*Qin/ntube;
m1psi =sum(mixratio.*psicen)./m0psi*Qin/ntube;
m2cpsi=sum(mixratio.*(psicen-ones(ntube,1)*m1psi).^2)./m0psi*Qin/ntube;
% flux related dilution index
pQ     = mixratio./(ones(ntube,1)*mean(mixratio)*Qin);
pQlnpQ = pQ.*log(pQ); pQlnpQ(pQ<1e-30)=0;
dilind = exp(-Qin*mean(pQlnpQ));

figure(2)
colormap('jet')
phi_line=0.5*(mean(net.phi(:,1:end-1))+mean(net.phi(:,2:end)));
subplot(3,1,1)
AX=plotyy(phi_line,m1,phi_line,sqrt(m2c));
set(AX,'xdir','reverse');
xlabel('h [m]')
ylabel(AX(1),'y_{cen} [m]')
ylabel(AX(2),'w_y [m]')
legend('center position','spread')
title('transverse spatial moments of mixing ratio')
subplot(3,1,2)
AX=plotyy(phi_line,m1psi,phi_line,sqrt(m2cpsi));
set(AX,'xdir','reverse');
xlabel('h [m]')
ylabel(AX(1),'\psi_{cen} [m^2/s]')
ylabel(AX(2),'w_\psi [m^2/s]')
legend('center position','spread')
title('flux-related transverse spatial moments of mixing ratio')
subplot(3,1,3)
plot(phi_line,sqrt(m2cpsi),phi_line,dilind);
set(gca,'xdir','reverse');
xlabel('h [m]')
ylabel('\psi_{cen} [m^2/s]')
ylabel('w_\psi [m^2/s]')
legend('spread based on moment','dilution index')
title('flux-related measure of plume width')


% ============== REACTIVE-SPECIES CONCENTRATIONS BY POSTPROCESSING ================
% compute concentrations for the limiting case of an instantaneous
% reaction
c1inst=2*mixratio-1;
c1inst(mixratio<0.5)=0;

c2inst=1-2*mixratio;
c2inst(mixratio>0.5)=0;

c3inst=1-mixratio;
c3inst(mixratio<0.5)=mixratio(mixratio<0.5);

figure(3)
colormap('jet')
set(gcf,'name','Concentration Distribution');
subplot(3,1,1)
pcolor(net.x,net.y,[c1inst c1inst(:,end);c1inst(end,:) c1inst(end,end)]);
shading flat;
set(gca,'dataaspectratio',[1 1 1]);
title('Compound A');
xlabel('x_1 [m]');ylabel('x_2 [m]');
cb1=colorbar;
ax1=gca;
subplot(3,1,2)
pcolor(net.x,net.y,[c2inst c2inst(:,end);c2inst(end,:) c2inst(end,end)]);
shading flat;
set(gca,'dataaspectratio',[1 1 1]);
title('Compound B');
xlabel('x_1 [m]');ylabel('x_2 [m]');
cb2=colorbar;
ax2=gca;
subplot(3,1,3)
pcolor(net.x,net.y,[c3inst c3inst(:,end);c3inst(end,:) c3inst(end,end)]);
shading flat;
set(gca,'dataaspectratio',[1 1 1]);
title('Product C');
xlabel('x_1 [m]');ylabel('x_2 [m]');
cb3=colorbar;
ax3=gca;

set(ax1,'position',[0.1  2/3+0.075 0.7  0.2]);
set(cb1,'position',[0.85 2/3+0.075 0.05 0.2]);
set(ax2,'position',[0.1  1/3+0.075 0.7  0.2]);
set(cb2,'position',[0.85 1/3+0.075 0.05 0.2]);
set(ax3,'position',[0.1      0.075 0.7  0.2]);
set(cb3,'position',[0.85     0.075 0.05 0.2]);

figure(4)
colormap('jet')
AX=plotyy(phi_line,dilind,phi_line,mean(c3inst)*Qin);
set(AX,'xdir','reverse','ytickmode','auto');
set(AX(1),'ygrid','on');
xlabel('h [m]')
ylabel(AX(1),'E_Q [m^2/s]')
ylabel(AX(2),'F_C [mol/s/m]')
legend('dilution index','mass flux of product')
title('dilution index and total mass flux of product')

