clear all
close all
clc

%% Settings
set(groot,'defaultTextInterpreter','latex')
set(groot,'DefaultLegendInterpreter', 'latex')
set(groot,'defaultFigureColor','w')
set(groot,'defaultAxesFontSize',16)
set(groot,'defaultTextFontSize',16)

sCase    = 'Doppelpendel';    % 'Linear'  |  'Duffing'  |  'Lorenz'  |  'Roessler'  |  Doppelpendel
fLogBase = @log;          % @log      | @log2       |  @log10
nT0      = 0;
nT1      = 5000;
nT_f     = 1;
nT_Samp  = 1/2^5;         % Abtastperiode  f�r die FFT-Analyse
sODE_options = odeset('RelTol',1e-6,'AbsTol',1e-8);

switch sCase 
  case 'Linear'
    xA = [1 2 1; 
          2 1 1;
          1 1 2];
    vParams = xA; 
    vX0  = [0;1;0];
    fODE = @fLinSys;
    fSolver = @ode45;
    sODE_options = odeset(sODE_options,'Event', @(t,x) fLinSys_event(t,x));
  case 'Duffing'
    nBeta = 0.1;
    nP    = 0.3;
    nOm   = 1.2;
    vParams = [nBeta,nP,nOm];
    vX0  = [0;1;0];
    fODE = @fDuffing;
    fSolver = @ode15s;   
    sODE_options = odeset(sODE_options,'Event', @(t,x) fDuffing_event(t,x));
  case 'Lorenz'
    nA = 16;  nB = 45.92;  nC = 4;      % Parameter aus Nayfeh, Balachandran - "Applied Nonlinear Dynamics" (@log2)
    vParams = [nA,nB,nC];
    vX0  = [0;1;0];
    fODE = @fLorenz;
    fSolver = @ode15s;   
    sODE_options = odeset(sODE_options,'Event', @(t,x) fLorenz_event(t,x));
  case 'Roessler'
%     nA = 0.15;  nB = 0.2;  nC = 10;     % Parameter aus Nayfeh, Balachandran - "Applied Nonlinear Dynamics" (@log2)
    nA = -0.5;  nB = -0.4;  nC = 4.5;
    vParams = [nA,nB,nC];
    vX0  = [0;1;0];
    fODE = @fRoessler;
    fSolver = @ode15s;
    sODE_options = odeset(sODE_options,'Event', @(t,x) fRoessler_event(t,x));
  case 'Doppelpendel'
    nM1 = 0.1;
    nM2 = 0.1;
    nL  = 0.2;
    nG  = 9.81;
    vParams = [nM1,nM2,nL,nG];
    vX0  = [pi;pi;0;0.1];
    fODE = @fDoppelpendel;
    fSolver = @ode45;
    sODE_options = odeset(sODE_options,'Event', @(t,x) fDoppelpendel_event(t,x));
end

%% Berechnung der Ljapunov-Exponenten
tic
[vT,xLambda,vT_ges,xX_ges,vT_event,xX_event] = fLjapunovExp_PC_Calc(fODE,vParams, fSolver, fLogBase, sODE_options,vX0,nT0,nT1,nT_f);
toc

%% Berechnung des FFTs
vInd           = find(vT_ges(2:end)-vT_ges(1:end-1)==0);
vT_ges(vInd)   = [];
xX_ges(vInd,:) = [];
nN_Samp        = vT_ges(end)/nT_Samp;
xX_FFT         = spline(vT_ges,xX_ges.',linspace(vT_ges(1),vT_ges(end),nN_Samp)).';
xA_FK_FFT      = NaN(floor(nN_Samp/2+1),size(xX_ges,2));
vFreq_FFT      = 1/nT_Samp*(0:(nN_Samp/2))/nN_Samp;
for nI = 1:size(xX_ges,2)
  vAmp                  = abs(fft(xX_ges(:,nI))/size(xX_ges,1));
  xA_FK_FFT(:,nI)       = vAmp(1:floor(nN_Samp/2+1));
  xA_FK_FFT(2:end-1,nI) = 2*xA_FK_FFT(2:end-1,nI);
end

%% Visualization
figure(1)
subplot(2,2,1)
plot(vT,xLambda)
xlabel('$t$')
ylabel('$\lambda_i$')
title('Ljapunov-Exponenten')
subplot(2,2,2)
plot3(xX_ges(:,1),xX_ges(:,2),xX_ges(:,3))
xlabel('$x_1$')
ylabel('$x_2$')
zlabel('$x_3$')
subplot(2,2,3)
plot(vFreq_FFT,xA_FK_FFT(:,1))
title('FFT-Analyse')
xlabel('$f$')
ylabel('$A_k$')
subplot(2,2,4)
switch sCase
  case 'Linear'
    plot(xX_event(:,1),xX_event(:,2),'*')
    xlabel('$x_1$')
    ylabel('$x_2$')
  case 'Duffing'
    plot(xX_event(:,1),xX_event(:,2),'*')
    xlabel('$x_1$')
    ylabel('$x_2$')
  case 'Lorenz'
    plot(xX_event(:,1),xX_event(:,3),'*')
    xlabel('$x_1$')
    ylabel('$x_3$')
  case 'Roessler'
    plot(xX_event(:,2),xX_event(:,3),'*')
    xlabel('$x_2$')
    ylabel('$x_3$')
  case 'Doppelpendel'
    plot(xX_event(:,1),xX_event(:,2),'*')
    xlabel('$x_1$')
    ylabel('$x_2$')
end
title("Poincar\'{e} Map")
