% MATLAB script steady_state_random_dualMiMen.m
%
% This script generates random 2-D fields, computes heads and
% stream function values, constructs streamline-oriented grids,
% computes steady-state concentrations for the joint injection 
% of reactants undergoing dual Michaelis-Menten kinetics
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
%%% PARAMETERS RELATED TO DUAL MICHAELIS-MENTEN KINETICS
% Inflow concentrations
c_in=[2,1,0];
% Michaelis-Menten coefficients
K_MM = [0.1,0.1];
% Maximum reaction rate [conc./second]
r_max=5e-6;
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
set(gcf,'outerposition',get(0,'screensize'))
colormap('jet')
tiledlayout(2,2,'TileSpacing','tight')
nexttile(1)
pcolor(X,Y,log10([K K(:,1);K(1,:) K(1,1)]));
shading flat;
xlim([0,nx(1)*dx(1)]);
ylim([0,nx(2)*dx(2)]);
cb=colorbar;
box on;
daspect([1 1 1]);
xlabel('x');ylabel('y');
ylabel(cb,'log_{10} K (K in m/s)')
title('Log-Conductivity Field')
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
nexttile(2)
h=reshape(h,nx(2)+1,nx(1)+1);
psi=reshape(psi,nx(2)+1,nx(1)+1);
contour(X,Y,psi,50,'k');
hold on
contour(X,Y,h,100);
hold off
box on;
daspect([1 1 1]);
xlabel('x');ylabel('y');
clim([0 phiin]);
cb=colorbar;
ylabel(cb,'h [m]');
title('Flow Net')
drawnow

% ============== BEGIN GRID CONSTRUCTION ==========================================
disp([datestr(clock) ': Construction of Streamline-Oriented Grid']);
[net,doagain] = slgrid(ntube,nsec,nx,dx,X,Y,psi,h,phiin,Qin);
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

nexttile(3)
plot(net.x,net.y,'k')
hold on
plot(net.x.',net.y.','k')
hold off
set(gca,'dataaspectratio',[1 1 1]);
xlabel('x [m]');ylabel('y [m]');
title('Streamline-Oriented Grid')

nexttile(4)
pcolor(net.x,net.y,[m1 m1(:,end);m1(end,:) m1(end,end)]/86400);
shading flat;
set(gca,'dataaspectratio',[1 1 1]);
xlabel('x [m]');ylabel('y [m]');
cb=colorbar;ylabel(cb,'\mu_\tau [d]')
title('Mean Groundwater Age')
drawnow

% ============== ODE SYSTEM FOR REACTIVE TRANSPORT ========================
[T_ODE,C_ODE] = ode15s(@(t,c) MiMenODE(t,c,K_MM,r_max),[0 max(m1(:))],c_in);

% ============== STEADY-STATE REACTIVE TRANSPORT ==========================
disp([datestr(clock) ': Solve for Transient Concentration']);

% initialization
c1 = interp1(T_ODE,C_ODE(:,1),m1(:));
c2 = interp1(T_ODE,C_ODE(:,2),m1(:));
c3 = interp1(T_ODE,C_ODE(:,3),m1(:));
c=[c1;c2;c3];

% specific discharge per stream tube
invec = zeros(nnet,1);
invec(1:ntube)=Qin/ntube;

% selection of inflow
is_in = zeros(nnet,1);
is_in(1:ntube)=1;

% define transport matrix and right-hand side vector for all three
% components
Mtot=[Mmob spalloc(nnet,2*nnet,0); ...
      spalloc(nnet,nnet,0) Mmob spalloc(nnet,nnet,0); ...
      spalloc(nnet,2*nnet,0) Mmob];
rhs =[invec.*is_in*c_in(1);invec.*is_in*c_in(2);invec.*is_in*c_in(3)];

done=false;

iter=0;
figure(2)
colormap('jet')
set(gcf,'outerposition',get(0,'screensize'))
% center point of the cell
xcen=0.25*(net.x(1:end-1,1:end-1)+net.x(2:end ,1:end-1)+...
           net.x(1:end-1,2:end )+net.x(2:end ,2:end ));
       
% reaction rate
r=c1./(c1+K_MM(1)).*c2./(c2+K_MM(2))*r_max;
r_tot=[-porarea.*r;-porarea.*r;porarea.*r];

% compute residuals
res=Mtot*c-rhs-r_tot;
resnorm=norm(res);
disp([datestr(clock) ': norm of residuals ' num2str(resnorm)]);

while ~done
    % plotting
    cplot1=reshape(c1,ntube,nsec);
    cplot2=reshape(c2,ntube,nsec);
    cplot3=reshape(c3,ntube,nsec);
    rplot =reshape(r ,ntube,nsec);
    
    tiledlayout(4,3,'TileSpacing','tight')
    nexttile(1)
    pcolor(net.x,net.y,...
           [cplot1 cplot1(:,end);cplot1(end,:) cplot1(end,end)]);
    daspect([1 1 1])
    xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
    clim([0 c_in(1)])
    shading flat;
    set(gca,'dataaspectratio',[1 1 1]);
    xlabel('x [m]');ylabel('y [m]');
    cb=colorbar;
    title(sprintf('Reactant 1 at Iteration %3i',iter));
    nexttile(2)
    plot(xcen(:),cplot1(:),'k.','markersize',2)
    xlabel('x [m]')
    ylabel('c [conc.]')
    title('Reactant 1 as Function of Distance');
    ylim([0 c_in(1)])
    nexttile(3)
    plot(m1(:)/86400,cplot1(:),'k.','markersize',2,'DisplayName','2-D')
    hold on
    plot(T_ODE/86400,C_ODE(:,1),'r','DisplayName','ODE')
    hold off
    legend
    xlabel('\mu_\tau [d]')
    ylabel('c [conc.]')
    title('Reactant 1 as Function of Groundwater Age');
    ylim([0 c_in(1)])

    nexttile(4)
    pcolor(net.x,net.y,...
           [cplot2 cplot2(:,end);cplot2(end,:) cplot2(end,end)]);
    daspect([1 1 1])
    xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
    clim([0 c_in(2)])
    shading flat;
    xlabel('x [m]');ylabel('y [m]');
    cb=colorbar;
    title(sprintf('Reactant 2 at Iteration %3i',iter));
    nexttile(5)
    plot(xcen(:),cplot2(:),'k.','markersize',2)
    xlabel('x [m]')
    ylabel('c [conc.]')
    title('Reactant 2 as Function of Distance');
    ylim([0 c_in(2)])
    nexttile(6)
    plot(m1(:)/86400,cplot2(:),'k.','markersize',2,'DisplayName','2-D')
    hold on
    plot(T_ODE/86400,C_ODE(:,2),'r','DisplayName','ODE')
    hold off
    legend
    xlabel('\mu_\tau [d]')
    ylabel('c [conc.]')
    title('Reactant 2 as Function of Groundwater Age');
    ylim([0 c_in(2)])

    nexttile(7)
    pcolor(net.x,net.y,...
           [cplot3 cplot3(:,end);cplot3(end,:) cplot3(end,end)]);
    daspect([1 1 1])
    xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
    shading flat;
    xlabel('x [m]');ylabel('y [m]');
    cb=colorbar;
    title(sprintf('Product at Iteration %3i',iter));
    nexttile(8)
    plot(xcen(:),cplot3(:),'k.','markersize',2)
    xlabel('x [m]')
    ylabel('c [conc.]')
    title('Product as Function of Distance');
    nexttile(9)
    plot(m1(:)/86400,cplot3(:),'k.','markersize',2,'DisplayName','2-D')
    hold on
    plot(T_ODE/86400,C_ODE(:,3),'r','DisplayName','ODE')
    hold off
    legend
    xlabel('\mu_\tau [d]')
    ylabel('c [conc.]')
    title('Product as Function of Groundwater Age');
       
    nexttile(10)
    pcolor(net.x,net.y,...
           [rplot rplot(:,end);rplot(end,:) rplot(end,end)]*86400);
    daspect([1 1 1])
    xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
    shading flat;
    set(gca,'dataaspectratio',[1 1 1]);
    xlabel('x [m]');ylabel('y [m]');
    cb=colorbar;
    title(sprintf('Reaction Rate at Iteration %3i',iter));
    nexttile(11)
    plot(xcen(:),rplot(:)*86400,'k.','markersize',2)
    xlabel('x [m]')
    ylabel('r [conc./d]')
    title('Reaction Rate as Function of Distance');
    nexttile(12)
    plot(m1(:)/86400,rplot(:)*86400,'k.','markersize',2,'DisplayName','2-D')
    r_ODE = C_ODE(:,1)./(K_MM(1)+C_ODE(:,1)).* ...
            C_ODE(:,2)./(K_MM(2)+C_ODE(:,2))*r_max;
    hold on
    plot(T_ODE/86400,r_ODE*86400,'r','DisplayName','ODE')
    hold off
    legend
    xlabel('\mu_\tau [d]')
    ylabel('r [conc./d]')
    title('Reaction Rate as Function of Groundwater Age');

    drawnow;
    
    % check norm of residuals
    if resnorm<1e-16
       done=true;
    else
       iter=iter+1;
       resold=resnorm;
       disp([datestr(clock) ': iteration ' num2str(iter)]);
       % evaluate Jacobian
       drdc1=spdiags(K_MM(1)./(c1+K_MM(1)).^2.*c2./(c2+K_MM(2))*r_max.*porarea,0,nnet,nnet);
       drdc2=spdiags(K_MM(2)./(c2+K_MM(2)).^2.*c1./(c1+K_MM(1))*r_max.*porarea,0,nnet,nnet);
       J=[Mmob+drdc1      drdc2 spalloc(nnet,nnet,0);...
               drdc1 Mmob+drdc2 spalloc(nnet,nnet,0);...
              -drdc1     -drdc2 Mmob];
       % update
%        disp([datestr(clock) ': Incomplete LU decomposition']);
%        [L,U] = ilu(J);
       disp([datestr(clock) ': Update Concentration']);
%        delta_c=bicgstab(J,-res,1e-12,10*nnod,L,U);
       delta_c=-J\res;
       cold=c;
       relinc=1;
       
       while resnorm>=resold
             c =cold+relinc*delta_c;
             c(c<0)=0;
             c1=c(       1:  nnet);
             c2=c(  nnet+1:2*nnet);
             c3=c(2*nnet+1:3*nnet);
       
             % reaction rate
             r=c1./(c1+K_MM(1)).*c2./(c2+K_MM(2))*r_max;
             r_tot=[-porarea.*r;-porarea.*r;porarea.*r];

             % compute residuals
             res=Mtot*c-rhs-r_tot;
             resnorm=norm(res);
             disp([datestr(clock) ': norm of residuals ' num2str(resnorm)]);
             if resnorm>=resold
                 relinc=relinc/2;
                 disp([datestr(clock) ': reduce step size to ' num2str(relinc)]);
             end
       end
    end
end

% interpolation onto regular travel-time increments
tmax=quantile(m1(:,end),0.9);
treg=[0:2*nsec]/(2*nsec)*tmax;

c1_treg=zeros(ntube,2*nsec+1);
c2_treg=zeros(ntube,2*nsec+1);
c3_treg=zeros(ntube,2*nsec+1);
 r_treg=zeros(ntube,2*nsec+1);
for ii=1:ntube
    c1_treg(ii,:)=interp1(m1(ii,:),cplot1(ii,:),treg,'pchip',nan);
    c2_treg(ii,:)=interp1(m1(ii,:),cplot2(ii,:),treg,'pchip',nan);
    c3_treg(ii,:)=interp1(m1(ii,:),cplot3(ii,:),treg,'pchip',nan);
     r_treg(ii,:)=interp1(m1(ii,:),rplot(ii,:),treg,'pchip',nan);
end

figure(3)
subplot(4,1,1)
hh=plot(treg/86400,prctile(c1_treg,[2.5 25 50 75 97.5]),'k');
set(hh([1 5]),'linestyle',':')
set(hh([2 4]),'linestyle','--')
hold on
plot(T_ODE/86400,C_ODE(:,1),'r','DisplayName','ODE')
hold off
xlabel('\mu_\tau [d]')
ylabel('c [conc.]')
title('Reactant 1 as Function of Groundwater Age')

subplot(4,1,2)
hh=plot(treg/86400,prctile(c2_treg,[2.5 25 50 75 97.5]),'k');
set(hh([1 5]),'linestyle',':')
set(hh([2 4]),'linestyle','--')
hold on
plot(T_ODE/86400,C_ODE(:,2),'r','DisplayName','ODE')
hold off
xlabel('\mu_\tau [d]')
ylabel('c [conc.]')
title('Reactant 2 as Function of Groundwater Age')

subplot(4,1,3)
hh=plot(treg/86400,prctile(c3_treg,[2.5 25 50 75 97.5]),'k');
set(hh([1 5]),'linestyle',':')
set(hh([2 4]),'linestyle','--')
hold on
plot(T_ODE/86400,C_ODE(:,3),'r','DisplayName','ODE')
hold off
xlabel('\mu_\tau [d]')
ylabel('c [conc.]')
title('Product as Function of Groundwater Age')

subplot(4,1,4)
hh=plot(treg/86400,prctile(r_treg,[2.5 25 50 75 97.5])*86400,'k');
set(hh([1 5]),'linestyle',':')
set(hh([2 4]),'linestyle','--')
hold on
plot(T_ODE/86400,r_ODE*86400,'r','DisplayName','ODE')
hold off
xlabel('\mu_\tau [d]')
ylabel('r [conc./s]')
title('Reaction Rate as Function of Groundwater Age')

function dcdt = MiMenODE(t,c,K_MM,r_max)
r = c(1)/(K_MM(1)+c(1))*c(2)/(K_MM(2)+c(2))*r_max;
dcdt = r*[-1;-1;1];
end
