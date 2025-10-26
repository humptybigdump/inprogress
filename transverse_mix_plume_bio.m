% MATLAB script transverse_mix_plume_bio.m
%
% This script computes 2-D fields of heads and
% stream function values, constructs streamline-oriented grids,
% computes steady-state concentrations, and concentrations of
% reactive compounds undergoing a microbially mediated reaction
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
% September 21, 2013
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
% head difference
phiin = nx(1)*dx(1)*0.01;
% transport parameter
poros = 0.3;
al    = 0.01;  % longitudinal dispersivity [-]
at    = 0.001; % transverse dispersivity [-]
Dp    = [.3e-9 1e-9 .8e-9 .1e-9]; % pore diffusion coefficient of DOC, 
                                  % oxygen, product, and mobile biomass

% time control
dt_max = 86400*5;
dt_ini = 86400;
dt = dt_ini;
t_end = 365*86400;
% convergence criterion: maximum norm of the residuals
resnormmax=1e-13; 

% biokinetic parameters
% A + B -> C
% biomass in steady state
% stoichiometry
stoch_a = 1;     % reactant 1
stoch_b = 1;     % reactant 2
stoch_c = 1;     % product
% concentrations in the inflow
Ain = 0.33;      % mmol/L = 4 mg/L Corg 
Bamb = 0.25;     % mmol/L = 8 mg/L O2
bioin = 1e-3;    % mg/L biomass (permanent inocculation)
% Monod-related coefficients
KA = 8.33e-2;    % mmol/L Monod coeff. = 1 mg/L Corg
KB = 3.13e-2;    % mmol/L Monod coeff. = 1 mg/L O2
mumax = 1/86400; % 1/s max. spec. growth rate
Yield = 1;       % mg/mmol specific yield
% additional biomass related coefficients
kdec =0.1/86400; % 1/s decay rate coeff.
R_bio=100;       % retardation factor for transport of biomass

names={'substrate','oxygen','product','biomass'};
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
colormap('jet')
tiledlayout(3,1,'TileSpacing','compact')
nexttile(1)
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
[Mmod,rhs]=gwdiri(M,r,[innod outnod],[phiin*ones(1,nx(2)+1) zeros(1,nx(2)+1)]);

% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mmod);
disp([datestr(clock) ': Solve for Head']);
% h     = bicgstab(Mmod,rmod,1e-12,10*nnod,L,U);
h     = Mmod\rhs;
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
[Mmod,rhs]=gwdiri(M,r,[botnod topnod],[zeros(1,nx(1)+1) Qin*ones(1,nx(1)+1)]);

% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mmod);
disp([datestr(clock) ': Solve for Stream Function']);
%psi   = bicgstab(Mmod,rmod,1e-12,10*nnod,L,U);
psi   = Mmod\rhs;
% remove roundoff errors of bottom and top nodes
psi(topnod)=Qin;
psi(botnod)=0;

% ============== END STREAM FUNCTION CALCULATION ==================================
nexttile(2)
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
Mstore = spdiags([porarea;porarea;porarea;porarea],0,4*nnet,4*nnet);

% streamline oriented grid 3: mobility matrix
disp([datestr(clock) ': Evaluate Mobility Matrices']);
% using average Dp-value for mixing ratio
Mmob  = mob_mat(ntube,nsec,Qin,net,al,at,mean(Dp(1:3)),porarea./area,1);
% for DOC
Mmob1 = mob_mat(ntube,nsec,Qin,net,al,at,Dp(1),porarea./area,1);
% for oxygen
Mmob2 = mob_mat(ntube,nsec,Qin,net,al,at,Dp(2),porarea./area,1);
% for product
Mmob3 = mob_mat(ntube,nsec,Qin,net,al,at,Dp(3),porarea./area,1);
% for mobile biomass
Mmob4 = mob_mat(ntube,nsec,Qin,net,al,at,Dp(4),porarea./area,1);
% ============== END TRANSPORT PREPARATION ========================================
 
% ============== CALCULATE MIXING RATIO ===========================================
% specific discharge per stream tube
invec = zeros(nnet,1);
invec(1:ntube)=Qin/ntube;

%!!! + + + + + + + + + + + + + + + + + + + !!!
%!!! Here the injection boundary is defined!!!
is_in1 = zeros(nnet,1);
is_in1(floor(ntube/2+1)+[-15:15])=1;
is_in2 = zeros(nnet,1);
is_in2(1:ntube)=1;
is_in2(floor(ntube/2+1)+[-15:15])=0;
%!!! + + + + + + + + + + + + + + + + + + + !!!

rhs=invec.*is_in1;

% LU decomposition
% disp([datestr(clock) ': Incomplete LU decomposition']);
% [L,U] = ilu(Mmob);
disp([datestr(clock) ': Solve for Mixing Ratio']);
% mixratio   = reshape(bicgstab(Mmob,rmod,1e-12,10*nnod,L,U),ntube,nsec);
mixratio   = reshape(Mmob\rhs,ntube,nsec);

% plotting
nexttile(3)
pcolor(net.x,net.y,[mixratio mixratio(:,end);mixratio(end,:) mixratio(end,end)]);
shading flat;
caxis([0 1])
daspect([1 1 1]);
xlabel('x_1 [m]');ylabel('x_2 [m]');
colorbar;
title('mixing ratio')
drawnow;


% ============== STEADY-STATE REACTIVE-SPECIES CONCENTRATIONS =====================
figure(2)
tiledlayout(4,1,'TileSpacing','compact')
colormap('jet')
set(gcf,'outerposition',get(0,'screensize'))
% define transport matrix and right-hand side vector for all four
% components
Mtot=[Mmob1 spalloc(nnet,3*nnet,0); ...
      spalloc(nnet,nnet,0) Mmob2 spalloc(nnet,2*nnet,0); ...
      spalloc(nnet,2*nnet,0) Mmob3 spalloc(nnet,nnet,0); ...
      spalloc(nnet,3*nnet,0) Mmob4/R_bio];
rhs =[invec.*is_in1*Ain;...
      invec.*is_in2*Bamb;...
      zeros(nnet,1);...
      invec*bioin/R_bio];

% initialization: steady-state transport without reactions
c=Mtot\rhs;
c1=c(       1:  nnet);
c2=c(  nnet+1:2*nnet);
c3=c(2*nnet+1:3*nnet);
c4=c(3*nnet+1:4*nnet);
c=[c1;c2;c3;c4];
cold=c;

% specific discharge per stream tube
invec = zeros(nnet,1);
invec(1:ntube)=Qin/ntube;

t=0;
while t<t_end
t=t+dt;
disp([datestr(clock) ': Solve for Concentrations at t = ' num2str(t)]);
done=false;

iter=0;

% reaction rate
mu=c1./(c1+KA).*c2./(c2+KA)*mumax.*c4;
r_tot=[-porarea.*mu/Yield*stoch_a;...
       -porarea.*mu/Yield*stoch_b;...
        porarea.*mu/Yield*stoch_c;...
        porarea.*mu-porarea.*c4*kdec];

% Matrices
Mleft=Mtot+Mstore/dt;
Mright=Mstore/dt;

% compute residuals
res=Mleft*c-rhs-r_tot-Mright*cold;
resnorm=norm(res);
disp([datestr(clock) ': norm of residuals ' num2str(resnorm)]);

AX=zeros(4,1);
while ~done
    % plotting
    cplot=nan(ntube,nsec,4);
    cplot(:,:,1)=reshape(c1,ntube,nsec);
    cplot(:,:,2)=reshape(c2,ntube,nsec);
    cplot(:,:,3)=reshape(c3,ntube,nsec);
    cplot(:,:,4)=reshape(c4,ntube,nsec);
    for ic=1:4
        nexttile(ic)
        pcolor(net.x,net.y,...
           [cplot(:,:,ic) cplot(:,end,ic);cplot(end,:,ic) cplot(end,end,ic)]);
        daspect([1 1 1])
        xlim([0 nx(1)*dx(1)]);ylim([0 nx(2)*dx(2)]);
        shading flat;
        daspect([1 1 1]);
        xlabel('x_1 [m]');ylabel('x_2 [m]');
        if ic==4,caxis([0 prctile(c4,99)]);end
        colorbar;
        AX(ic)=gca;
        title([names{ic} sprintf(': t = %10.1fd, iteration %3i',[t/86400,iter])])
    end
    drawnow;
    
    % check norm of residuals
    if resnorm<resnormmax
       done=true;
    else
       iter=iter+1;
       resold=resnorm;
       disp([datestr(clock) ': iteration ' num2str(iter)]);
       % evaluate Jacobian
       dmudc1=KA./(c1+KA).^2 .*c2./(c2+KB)   *mumax.*c4.*porarea;
       dmudc1=spdiags(dmudc1,0,nnet,nnet);
       dmudc2=c1./(c1+KA)     *KB./(c2+KB).^2*mumax.*c4.*porarea;
       dmudc2=spdiags(dmudc2,0,nnet,nnet);
       dmudc4=c1./(c1+KA)    .*c2./(c2+KB)   *mumax    .*porarea;
       dmudc4=spdiags(dmudc4,0,nnet,nnet);
       
       J11=Mmob1+dmudc1/Yield*stoch_a;
       J12=dmudc2/Yield*stoch_a;
       J13=spalloc(nnet,nnet,0);
       J14=dmudc4/Yield*stoch_a;
       
       J21=dmudc1/Yield*stoch_b;
       J22=Mmob2+dmudc2/Yield*stoch_b;
       J23=spalloc(nnet,nnet,0);
       J24=dmudc4/Yield*stoch_b;

       J31=-dmudc1/Yield*stoch_c;
       J32=-dmudc2/Yield*stoch_c;
       J33=Mmob3;
       J34=-dmudc4/Yield*stoch_c;

       J41=-dmudc1;
       J42=-dmudc2;
       J43=spalloc(nnet,nnet,0);
       J44=Mmob4/R_bio-dmudc4+spdiags(porarea*kdec,0,nnet,nnet);

       J=[J11 J12 J13 J14;...
          J21 J22 J23 J24;...
          J31 J32 J33 J34;...
          J41 J42 J43 J44]+Mstore/dt;
       % update
%        disp([datestr(clock) ': Incomplete LU decomposition']);
%        [L,U] = ilu(J);
       disp([datestr(clock) ': Update Concentration']);
%        delta_c=bicgstab(J,-res,1e-12,10*nnod,L,U);
       delta_c=-J\res;
       clast=c;
       relinc=1;
       
       while resnorm>=resold
             c =clast+relinc*delta_c;
             c(c<0)=0;
             c1=c(       1:  nnet);
             c2=c(  nnet+1:2*nnet);
             c3=c(2*nnet+1:3*nnet);
             c4=c(3*nnet+1:4*nnet);

             % reaction rate
             mu=c1./(c1+KA).*c2./(c2+KA)*mumax.*c4;
             r_tot=[-porarea.*mu/Yield*stoch_a;...
                    -porarea.*mu/Yield*stoch_b;...
                     porarea.*mu/Yield*stoch_c;...
                     porarea.*mu-porarea.*c4*kdec];

             % compute residuals
             res=Mleft*c-rhs-r_tot-Mright*cold;
             resnorm=norm(res);
             disp([datestr(clock) ': norm of residuals ' num2str(resnorm)]);
             if resnorm>=resold
                 relinc=relinc/2;
                 disp([datestr(clock) ': reduce step size to ' num2str(relinc)]);
             end
       end
    end
end
cold=c;
if iter<5
   dt=min(dt*2,dt_max);
   disp(['new dt =' num2str(dt) 's'])
elseif iter>10
   dt=dt/2;
   disp(['new dt =' num2str(dt) 's'])
end
end