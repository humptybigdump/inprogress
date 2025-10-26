% Exercise No. 6 of Modeling of Reactions
clear all
close all
clc

H = 2;         % Henry's law coefficient [-]
Vw = 1e-3;     % volume of water [m3]
Vg = 1e-3;     % volume of gas [m3]
vwg= 1e-3/60;  % gas-transfer velocity [m/s]
Awg= 0.01;     % interfacial area [m2]
kmt=vwg*Awg/Vw; % rate coefficient of gas transfer [1/s]
fprintf('rate coeff. of gas transfer in the aqueous phase: %g/s\n\n',kmt)
kdecvec=[0 1/86400 1/3600 1/60 1];  % first-order decay coefficient [1/s]

set(gcf,"OuterPosition",get(0,"ScreenSize"))
tiledlayout('flow')
for ii=1:length(kdecvec)
    kdec=kdecvec(ii);
    fprintf('kdec = %g/s, kdec/kmt = %g\n',[kdec,kdec/kmt])
    % Coefficient matrix [1/s]
    A=[-kmt-kdec    +kmt/H;...
       kmt*Vw/Vg    -kmt*Vw/Vg/H]

    % A little eigen analysis of the coefficient matrix
    [E,K]=eig(A);
    fprintf('1st eigenvector: [%g;%g]; 1st eigenvalue: %g/s\n',[E(:,1);K(1,1)]);
    fprintf('2nd eigenvector: [%g;%g]; 2nd eigenvalue: %g/s\n',[E(:,2);K(2,2)]);
    disp(' ')
 
    % initial condition
    c0=[0;1];
    dt=60;   % time step size [s]
    nt=1440; % number of time steps
    cmat=zeros(2,nt);
    % compute analytical solution
    for i=1:nt
        t=i*dt;
        cmat(:,i)=expm(A*t)*c0;
    end
    % graphical output
    nexttile
    plot([1:nt]*dt/3600,cmat);
    xlabel('t [h]')
    ylabel('c/c_g^{ini} [-]');
    legend('water','gas')
    title(sprintf('k_{dec} = %10.3g/s',kdec))

    % compare to numerical solution
    tspan=[0 nt*dt]; % time span
    [tvec,cmat2]=ode15s(@linSysODE,tspan,c0,[],kmt,kdec,H,Vw,Vg);
    hold on
    plot(tvec/3600,cmat2,'kx');
    hold off
    legend('water','gas','ODE15s')
    drawnow
end
%
function dcdt = linSysODE(t,c,kmt,kdec,H,Vw,Vg)
dcdt=zeros(size(c));

dcdt(1)= kmt*(c(2)/H-c(1)) -c(1)*kdec;
dcdt(2)= kmt*Vw/Vg*(c(1)-c(2)/H);
end