% MATLAB script transient_random_dualMiMen.m
%
% This script generates random 2-D fields, computes heads and
% stream function values, constructs streamline-oriented grids,
% computes transient concentrations for a replacement scenario of solutions
% containing two compounds undergoin dual Michaelis-Menten kinetics
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


clear all;close all;clc
% ============== BEGIN INPUT BLOCK ================================================
% number of elements per direction
nx = [200,100];
% grid spacing
dx = [.01,.01];
% correlation length
lx = [.25, .05];
% rotation angle
ang = 0;
% Exponential (1) or Gaussian (2) Covariance-Model 
Ctype = 1;
% number of stream tubes
ntube = 100;
% number of sections per stream tube
nsec =  200;
% geometric mean of conductivity 
Kg = 1e-4;
% variance of ln(K)
varY=1;
% head difference
phiin = nx(1)*dx(1)*0.01;
% transport parameter
poros = 0.3;
al    = 0.01;
at    = 0.001;
Dp    = 1e-9;
% plot transient concentration rsults?
plottransient=true;
% Crank-Nicolson weight for time integration (0: explicit, 1: implicit)
CN=1;
%%% PARAMETERS RELATED TO DUAL MICHAELIS-MENTEN KINETICS
% Initional concentrations
c0=[0,1,0];
% Inflow concentrations
c_in=[1,0,0];
% Michaelis-Menten coefficients
K_MM = [0.1,0.1];
% Maximum reaction rate [conc./second]
r_max=1e-4;
% derived: maximum pseudo first-order rate-coefficient
c1m=max([c_in(1) c0(1)]);
c2m=max([c_in(2) c0(2)]);
lambda_max=max([1/K_MM(1)*c2m/(c2m+K_MM(2))*r_max,...
                1/K_MM(2)*c1m/(c1m+K_MM(1))*r_max]);
% ============== END INPUT BLOCK ==================================================

doagain=true;
while doagain
% ============== BEGIN FIELD GENERATION BLOCK =====================================
% initialize random-number generator
rng(sum(100*clock),'twister');
% Spatial coordinates
[X,Y]=meshgrid([0:nx(1)]*dx(1),[0:nx(2)]*dx(2));
% Generate the field
K=randomK(nx,dx,lx,ang,varY,Ctype,Kg);

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
% psi   = bicgstab(Mmod,rmod,1e-12,10*nnod,L,U);
psi   = Mmod\rmod;
% remove roundoff errors of bottom and top nodes
psi(topnod)=Qin;
psi(botnod)=0;

% ============== END STREAM FUNCTION CALCULATION ==================================
subplot(3,1,2)
h=reshape(h,nx(2)+1,nx(1)+1);
psi=reshape(psi,nx(2)+1,nx(1)+1);
contour(X,Y,psi,50,'k');
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
end
% ============== END GRID CONSTRUCTION ============================================

% pcolor(net.x,net.y,net.phi);
% set(gca,'dataaspectratio',[1 1 1]);
% shading faceted;
% cb=colorbar;
% ylabel(cb,'h [m]')
% box on;
% daspect([1 1 1]);
% xlabel('x_1');ylabel('x_2');
% title('streamline oriented grid')
% set(gca,'outerposition',[0 1/3+0.025 1 1/3-0.025])
% drawnow;

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

% ============== GROUNDWATER AGE EQUATION =========================================
disp([datestr(clock) ': Temporal-Moment Generation Equations']);
% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mmob);
rhs=porarea(:);
disp([datestr(clock) ': Solve for Mean Groundwater Age']);
% m1=bicgstab(Mmob,rhs,1e-12,10*nnod,L,U);
m1=Mmob\rhs;
m1=reshape(m1,ntube,nsec);

subplot(3,1,3)
pcolor(net.x,net.y,[m1 m1(:,end);m1(end,:) m1(end,end)]);
shading flat;
set(gca,'dataaspectratio',[1 1 1]);
xlabel('x_1 [m]');ylabel('x_2 [m]');
cb=colorbar;ylabel(cb,'\mu_\tau [s]')
set(gca,'outerposition',[0 0.025 1 1/3-0.025])
title('mean groundwater age')
drawnow

% ============== TRANSIENT CONCENTRATIONS =========================================
disp([datestr(clock) ': Solve for Transient Concentration']);

% total time
tend  = 2*max(m1(:));
if CN<1
   % determine time step size so that maximum Courant number is unity
   dt = min(porarea)/Qin*ntube;
else
   % determine time step size so that mean Courant number is unity
   dt = mean(porarea)/Qin*ntube;
end
% make sure explicit calculation of reactions is not leading to negative
% concentrations
if 1/lambda_max<dt
    dt=1/lambda_max;
end
% Remark: Use Crank-Nicolson for transport
% (Mstore/dt + CN*Mmob)*c_new = (Mstore/dt - (1-CN)*Mmob)*c_old + r_source
Mleft  = Mstore/dt + CN*Mmob;
Mright = Mstore/dt - (1-CN)*Mmob;

% initialization
c1 = ones(ntube*nsec,1)*c0(1);
c2 = ones(ntube*nsec,1)*c0(2);
c3 = ones(ntube*nsec,1)*c0(3);

% specific discharge per stream tube
invec = zeros(nnet,1);
invec(1:ntube)=Qin/ntube;

is_in = zeros(nnet,1);
is_in(1:ntube)=1;

% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mleft);
disp([datestr(clock) ': Incomplete LU decomposition']);
[L_M,U_M,P_M,Q_M,R_M] = lu(Mleft);

disp([datestr(clock) ': Solve for Concentration']);
tvec=dt:dt:tend;
BTC1=ones(ntube,length(tvec));
BTC2=ones(ntube,length(tvec));
BTC3=ones(ntube,length(tvec));
cplot1=reshape(c1,ntube,nsec);
cplot2=reshape(c2,ntube,nsec);
cplot3=reshape(c3,ntube,nsec);
if plottransient
   figure(2)
   colormap('jet')
   set(gcf,'outerposition',get(0,'screensize'))
   xcen=0.25*(net.x(1:end-1,1:end-1)+net.x(2:end ,1:end-1)+...
              net.x(1:end-1,2:end )+net.x(2:end ,2:end ));
end
for ii=1:length(tvec)
    t=tvec(ii);
    disp([datestr(clock) ': time =' num2str(t) ' s']);
    days   =floor(t/86400);
    hours  =floor((t-86400*days)/3600);
    minutes=floor((t-86400*days-3600*hours)/60);
    seconds=floor(t-86400*days-3600*hours-60*minutes);

    % Advective-dispersive transport compound 1
    % old time-point contribution to BTC
    BTCold1=cplot1(:,end);
    % determine the right-hand side vector
    rhs=Mright*c1 + ones(nnet,1).*invec.*is_in*c_in(1);
    % evaluate the concentration
%     c1=bicgstab(Mleft,rhs,1e-12,10*nnod,L,U,c1);
     c1=Q_M*(U_M\(L_M\(P_M*(R_M\rhs))));
   
    % Advective-dispersive transport compound 2
    % old time-point contribution to BTC
    BTCold2=cplot2(:,end);
    % determine the right-hand side vector
    rhs=Mright*c2 + ones(nnet,1).*invec.*is_in*c_in(2);
    % evaluate the concentration
%     c2=bicgstab(Mleft,rhs,1e-12,10*nnod,L,U,c2);
    c2=Q_M*(U_M\(L_M\(P_M*(R_M\rhs))));
    
    % Advective-dispersive transport compound 3
    % old time-point contribution to BTC
    BTCold3=cplot3(:,end);
    % determine the right-hand side vector
    rhs=Mright*c3 + ones(nnet,1).*invec.*is_in*c_in(3);
    % evaluate the concentration
%     c3=bicgstab(Mleft,rhs,1e-12,10*nnod,L,U,c3);
    c3=Q_M*(U_M\(L_M\(P_M*(R_M\rhs))));
    
    % Reaction
    % rate law
    r=c1./(c1+K_MM(1)).*c2./(c2+K_MM(2))*r_max;
    c1=c1-dt*r;
    c2=c2-dt*r;
    c3=c3+dt*r;
    
    cplot1=reshape(c1,ntube,nsec);
    cplot2=reshape(c2,ntube,nsec);
    cplot3=reshape(c3,ntube,nsec);
    rplot=reshape(r,ntube,nsec);

    % store the BTCs
    BTC1(:,ii)=(1-CN)*BTCold1+CN*cplot1(:,end);
    BTC2(:,ii)=(1-CN)*BTCold2+CN*cplot2(:,end);
    BTC3(:,ii)=(1-CN)*BTCold3+CN*cplot3(:,end);
    if min(BTC1(:,ii))>0.999,break,end
    if plottransient
       subplot(4,3,1)
       pcolor(net.x,net.y,...
           [cplot1 cplot1(:,end);cplot1(end,:) cplot1(end,end)]);
       daspect([1 1 1])
       xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
       caxis([0 c1m])
       shading flat;
       set(gca,'dataaspectratio',[1 1 1]);
       xlabel('x_1 [m]');ylabel('x_2 [m]');
       cb=colorbar;
       title(sprintf('compound 1 at %3.3id %2.2ih %2.2im %2.2is',[days,hours,minutes,seconds]));
       set(gca,'outerposition',[0   3/4 1/3 0.225])
       subplot(4,3,2)
       plot(xcen(:),cplot1(:),'k.','markersize',4)
       xlabel('x_1 [m]')
       ylabel('c')
       title('compound 1 as function of distance');
       ylim([0 c1m])
       set(gca,'outerposition',[1/3 3/4 1/3 0.225])
       subplot(4,3,3)
       plot(m1(:),cplot1(:),'k.','markersize',4)
       xlabel('groundwater age [s]')
       ylabel('c')
       title('compound 1 as function of groundwater age');
       ylim([0 c1m])
       set(gca,'outerposition',[2/3 3/4 1/3 0.225])

       subplot(4,3,4)
       pcolor(net.x,net.y,...
           [cplot2 cplot2(:,end);cplot2(end,:) cplot2(end,end)]);
       daspect([1 1 1])
       xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
       caxis([0 c2m])
       shading flat;
       set(gca,'dataaspectratio',[1 1 1]);
       xlabel('x_1 [m]');ylabel('x_2 [m]');
       cb=colorbar;
       title(sprintf('compound 2 at %3.3id %2.2ih %2.2im %2.2is',[days,hours,minutes,seconds]));
       set(gca,'outerposition',[0  2/4 1/3 0.225])
       subplot(4,3,5)
       plot(xcen(:),cplot2(:),'k.','markersize',4)
       xlabel('x_1 [m]')
       ylabel('c')
       title('compound 2 as function of distance');
       ylim([0 c2m])
       set(gca,'outerposition',[1/3  2/4 1/3 0.225])
       subplot(4,3,6)
       plot(m1(:),cplot2(:),'k.','markersize',4)
       xlabel('groundwater age [s]')
       ylabel('c')
       title('compound 2 as function of groundwater age');
       ylim([0 c2m])
       set(gca,'outerposition',[2/3  2/4 1/3 0.225])

       subplot(4,3,7)
       pcolor(net.x,net.y,...
           [cplot3 cplot3(:,end);cplot3(end,:) cplot3(end,end)]);
       daspect([1 1 1])
       xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
       shading flat;
       set(gca,'dataaspectratio',[1 1 1]);
       xlabel('x_1 [m]');ylabel('x_2 [m]');
       cb=colorbar;
       title(sprintf('compound 3 at %3.3id %2.2ih %2.2im %2.2is',[days,hours,minutes,seconds]));
       set(gca,'outerposition',[0  1/4 1/3 0.225])
       subplot(4,3,8)
       plot(xcen(:),cplot3(:),'k.','markersize',4)
       xlabel('x_1 [m]')
       ylabel('c')
       title('compound 3 as function of distance');
       set(gca,'outerposition',[1/3 1/4 1/3 0.225])
       subplot(4,3,9)
       plot(m1(:),cplot3(:),'k.','markersize',4)
       xlabel('groundwater age [s]')
       ylabel('c')
       title('compound 3 as function of groundwater age');
       set(gca,'outerposition',[2/3 1/4 1/3 0.225])
       
       subplot(4,3,10)
       pcolor(net.x,net.y,...
           [rplot rplot(:,end);rplot(end,:) rplot(end,end)]);
       daspect([1 1 1])
       xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
       shading flat;
       set(gca,'dataaspectratio',[1 1 1]);
       xlabel('x_1 [m]');ylabel('x_2 [m]');
       cb=colorbar;
       title(sprintf('reaction rate at %3.3id %2.2ih %2.2im %2.2is',[days,hours,minutes,seconds]));
       set(gca,'outerposition',[0    0 1/3 0.225])
       subplot(4,3,11)
       plot(xcen(:),rplot(:),'k.','markersize',4)
       xlabel('x_1 [m]')
       ylabel('r')
       title('reaction rate as function of distance');
       set(gca,'outerposition',[1/3  0 1/3 0.225])
       subplot(4,3,12)
       plot(m1(:),rplot(:),'k.','markersize',4)
       xlabel('groundwater age [s]')
       ylabel('r')
       title('reaction rate as function of groundwater age');
       set(gca,'outerposition',[2/3  0 1/3 0.225])

       drawnow;
    end
end
tvec=tvec(1:ii);
BTC1=BTC1(:,1:ii);
BTC2=BTC2(:,1:ii);
BTC3=BTC3(:,1:ii);

figure(3)
plot(tvec,BTC1,'color',[1 .5 .5])
hold on
plot(tvec,BTC2,'color',[.5 .5 1])
plot(tvec,BTC3,'color',[.5 1 .5])
plot(tvec,mean(BTC1),'color',[1 0 0],'linewidth',4)
plot(tvec,mean(BTC2),'color',[0 0 1],'linewidth',4)
plot(tvec,mean(BTC3),'color',[0 1 0],'linewidth',4)
ylim([0 1])
hold off
xlabel('t [s]')
ylabel('c')

meanprodAB=sum(BTC1(:).*BTC2(:))*Qin/ntube
prodmeanAmeanB=sum(mean(BTC1).*mean(BTC2))*Qin