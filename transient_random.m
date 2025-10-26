% MATLAB script transient_random.m
%
% This script generates random 2-D fields, computes heads and
% stream function values, constructs streamline-oriented grids,
% computes transient concentrations for a step-input inflow condition, 
% and evaluates breakthrough curves for all stream tubes
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
% update October 4, 2019


clear all;close all;clc
% ============== BEGIN INPUT BLOCK ================================================
% number of elements per direction
nx = [500,250];
% grid spacing
dx = [.01,.01];
% correlation length
lx = [.50, .10];
% rotation angle
ang = 0;
% Exponential (1) or Gaussian (2) Covariance-Model 
Ctype = 1;
% number of stream tubes
ntube = 250;
% number of sections per stream tube
nsec =  500;
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
CN=0.5;
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
set(gcf,'outerposition',get(0,'screensize'),'paperunits','centimeters',...
    'paperposition',[0 0 20 10])
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
drawnow;
% print -djpeg100 -r300 Kfield.jpg
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
drawnow
% print -djpeg100 -r300 flownet.jpg

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

pcolor(net.x,net.y,[m1 m1(:,end);m1(end,:) m1(end,end)]);
shading flat;
set(gca,'dataaspectratio',[1 1 1]);
xlabel('x_1 [m]');ylabel('x_2 [m]');
cb=colorbar;ylabel(cb,'\mu_\tau [s]')
title('mean groundwater age')
drawnow
% print -djpeg100 -r300 gw_age.jpg

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
% Remark: Use Crank-Nicolson for transport
% (Mstore/dt + CN*Mmob)*c_new = (Mstore/dt - (1-CN)*Mmob)*c_old + r_source
Mleft  = Mstore/dt + CN*Mmob;
Mright = Mstore/dt - (1-CN)*Mmob;

% initialization
c = zeros(ntube*nsec,1);

% specific discharge per stream tube
invec = zeros(nnet,1);
invec(1:ntube)=Qin/ntube;

cin = zeros(nnet,1);
cin(1:ntube)=1;

% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mleft);
disp([datestr(clock) ': LU decomposition']);
[L_M,U_M,P_M,Q_M,R_M] = lu(Mleft);

disp([datestr(clock) ': Solve for Concentration']);
tvec=dt:dt:tend;
BTC=ones(ntube,length(tvec));
cplot=reshape(c,ntube,nsec);
if plottransient
    figure(2)
    set(gcf,'outerposition',get(0,'screensize'),'paperunits',...
        'centimeters','paperposition',[0 0 20 10])
    colormap('jet')
    iplot=0;
end
for ii=1:length(tvec)
    t=tvec(ii);
    disp([datestr(clock) ': time =' num2str(t) ' s']);
    days   =floor(t/86400);
    hours  =floor((t-86400*days)/3600);
    minutes=floor((t-86400*days-3600*hours)/60);
    seconds=floor(t-86400*days-3600*hours-60*minutes);
    % old time-point contribution to BTC
    BTCold=cplot(:,end);
    % determine the right-hand side vector
    rhs=Mright*c + ones(nnet,1).*invec.*cin;
    % evaluate the concentration
%     c=bicgstab(Mleft,rhs,1e-12,10*nnod,L,U,c);
    c=Q_M*(U_M\(L_M\(P_M*(R_M\rhs))));
    cplot=reshape(c,ntube,nsec);
    % store the BTC
    BTC(:,ii)=(1-CN)*BTCold+CN*cplot(:,end);
    if min(BTC(:,ii))>0.999,break,end
    if plottransient && mod(ii,40)==1
       pcolor(net.x,net.y,[cplot cplot(:,end);cplot(end,:) cplot(end,end)]);
       caxis([0 1])
       shading flat;
       set(gca,'dataaspectratio',[1 1 1]);
       xlabel('x_1 [m]');ylabel('x_2 [m]');
       cb=colorbar;ylabel(cb,'c/c_{in} [-]')
       title(sprintf('concentration at %3.3id %2.2ih %2.2im %2.2is',[days,hours,minutes,seconds]));
       drawnow;
       iplot=iplot+1;
%        print('-djpeg','-r130',sprintf('picture%4.4i.jpg',iplot))
    end
end
tvec=tvec(1:ii);
BTC=BTC(:,1:ii);

% take derivative to obtain travel-time pdf of each streamtube
ptau=zeros(ntube,length(tvec));
ptaurel=zeros(ntube,length(tvec));
% time scaled by mean groundwater age
trel=1./m1(:,end)*tvec;
for ii=1:ntube
    ptau(ii,:)=gradient(BTC(ii,:),tvec);
    ptaurel(ii,:)=gradient(BTC(ii,:),trel(ii,:));
end
figure(3)
set(gcf,'outerposition',get(0,'screensize'),'paperunits','centimeters',...
    'paperposition',[0 0 20 10])
subplot(1,2,1)
plot(tvec,ptau,'color',[.5 .5 .5])
hold on
plot(tvec,mean(ptau),'color','k','linewidth',2);
hold off
xlabel('\tau [s]')
ylabel('p(\tau) [1/s]')
box on
title('Local Travel-Time Distributions at the Outlet Face')
axis tight
subplot(1,2,2)
plot(trel,ptaurel,'color',[.5 .5 .5])
xlabel('\tau/\mu_\tau [-]')
ylabel('p(\tau/\mu_\tau) [-]')
box on
title('Local Travel-Time Distributions Scaled by Local Mean Groundwater Age')
xlim([0 tvec(end)/mean(m1(:,end))]);
ylim([0,max(ptaurel(:))]);
% print -djpeg100 -r300 BTC.jpg

figure(4)
plot(tvec,mean(ptau),tvec,std(ptau))
xlabel('\tau [s]')
legend('mean p(\tau)','std. of p(\tau)')

% save BTC.mat BTC tvec ptau trel ptaurel

%%%% REPLACEMENT SCENARIO %%% A+B > C with 1:1:1 stoichiometry
%%%% Initial concentration of B: 1
%%%% Injected concentration of A: 1

% Use local breakthrough curves
BTC_A=2*BTC-1; BTC_A(BTC_A<0)=0;
BTC_B=1-2*BTC; BTC_B(BTC_B<0)=0;
BTC_C=BTC-BTC_A;

% use averaged BTC of mixing ratio
BTC_Am=2*mean(BTC)-1; BTC_Am(BTC_Am<0)=0;
BTC_Bm=1-2*mean(BTC); BTC_Bm(BTC_Bm<0)=0;
BTC_Cm=mean(BTC)-BTC_Am;

figure(5)
subplot(2,1,1)
plot(tvec,BTC_A,'color',[.5 .5 1])
hold on
plot(tvec,BTC_B,'color',[1 .5 .5])
plot(tvec,BTC_C,'color',[.5 1 .5])
plot(tvec,mean(BTC_A),'color','b','linewidth',4)
plot(tvec,mean(BTC_B),'color','r','linewidth',4)
plot(tvec,mean(BTC_C),'color','g','linewidth',4)
hold off
xlabel('t [s]')
ylabel('c_{reac}')
box on
title('Reactive-Species Concentrations at the Outlet Face')
axis tight

subplot(2,1,2)
plot(tvec,mean(BTC_A),'color','b','linewidth',2)
hold on
plot(tvec,BTC_Am,'b--','linewidth',2)
plot(tvec,mean(BTC_B),'color','r','linewidth',2)
plot(tvec,BTC_Bm,'r--','linewidth',2)
plot(tvec,mean(BTC_C),'color','g','linewidth',2)
plot(tvec,BTC_Cm,'g--','linewidth',2)
hold off
legend('correct average','from average mixing ratio')
xlabel('t [s]')
ylabel('c_{reac}')
box on
title('Mean Reactive-Species Concentrations at the Outlet Face')
axis tight

