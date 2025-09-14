%Zusammenhang mod. Sommerfeldzahl, Exzentrizität, Verlagerungswinkel
%Feder-/Dämpferparameter
%Stabilit;
clear all;
global smi;
eta=[0.1:0.01:4];
beta=0.4;
Sou(1)=0.16;
Sou(2)=1.6;
for jj=1:2
sigma=beta^2/Sou(jj);
for i=1:length(eta)
sm(i)=sigma*eta(i);
smi=sm(i);
if (i>1)
eps(i)=fsolve(@epsilon,eps(i-1));
else
   eps(i)=fsolve(@epsilon,0.5);
end;
%stop;
%sm(i)=2*(1-eps(i)^2)^2/(pi*eps(i)*sqrt(1-eps(i)^2+(4*eps(i)/pi)^2));
gam(i)=180*atan((pi/4)*sqrt((1-eps(i)^2)/eps(i)^2))/pi;
gam1(i)=atan((pi/4)*sqrt((1-eps(i)^2)/eps(i)^2));
%sm1(i)=(1-eps(i)^2)^2/(eps(i)*sqrt(16*eps(i)^2+pi^2*(1-eps(i)^2)));
krr(i)=4*eps(i)*(1+eps(i)^2)/(1-eps(i)^2)^3;
krp(i)=pi/(2*(1-eps(i)^2)^(3/2));
kpr(i)=-pi*(1+2*eps(i)^2)/(2*(1-eps(i)^2)^(5/2));
kpp(i)=2*eps(i)/(1-eps(i)^2)^2;
crr(i)=pi*(1+2*eps(i)^2)/((1-eps(i)^2)^(5/2));
crp(i)=-4*eps(i)/(1-eps(i)^2)^2;
cpp(i)=pi/((1-eps(i)^2)^(3/2));
tmat=[cos(gam1(i)) -sin(gam1(i)); sin(gam1(i)) cos(gam1(i))];
k=tmat*[krr(i) krp(i); kpr(i) kpp(i)]*tmat';
c=tmat*[crr(i) crp(i); crp(i) cpp(i)]*tmat';
kxx(i)=sm(i)*k(1,1);
kxy(i)=sm(i)*k(1,2);
kyx(i)=sm(i)*k(2,1);
kyy(i)=sm(i)*k(2,2);
cxx(i)=sm(i)*c(1,1);
cxy(i)=sm(i)*c(1,2);
cyx(i)=cxy(i);
cyy(i)=sm(i)*c(2,2);

lhs=[kxx(i)-eta(i)^2 kxy(i) cxx(i) cxy(i); 
    kyx(i) kyy(i)-eta(i)^2 cyx(i) cyy(i);
    -cxx(i) -cxy(i) kxx(i)-eta(i)^2 kxy(i);
    -cyx(i) -cyy(i) kyx(i) kyy(i)-eta(i)^2];
rhs=[eps(i)*eta(i)^2; 0; 0; eps(i)*eta(i)^2];
sol=lhs\rhs;

gg(i)=0.5*(sqrt((sol(2)+sol(3))^2+(sol(1)-sol(4))^2)+sqrt((sol(2)-sol(3))^2+(sol(1)+sol(4))^2));
kk(i)=0.5*(sqrt((sol(2)+sol(3))^2+(sol(1)-sol(4))^2)-sqrt((sol(2)-sol(3))^2+(sol(1)+sol(4))^2));   
gg1(i,jj)=gg(i)/eps(i);
kk1(i,jj)=kk(i)/eps(i);
end;
end;

figure2 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure2);
% Uncomment the following line to preserve the X-limits of the axes
%xlim([0. 1.]);
%ylim([0 1]);
box('on');
hold('all');

% Create semilogx
plot(eta,gg1(:,1),eta,gg1(:,2));

% Create xlabel
xlabel({'$\bar{\omega}$'});

% Create ylabel
ylabel({'$G/\epsilon$'});
%,'XLim',[0.01:10])


figure3 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure3);
% Uncomment the following line to preserve the X-limits of the axes
%xlim([0. 1.]);
%ylim([0 1]);
box('on');
hold('all');
% Create semilogx
plot(eta,abs(kk1(:,1)),eta,abs(kk1(:,2)));

% Create xlabel
xlabel({'$\bar{\omega}$'});

% Create ylabel
ylabel({'$K/\epsilon$'});
%,'XLim',[0.01:10])


figure4 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure4);
% Uncomment the following line to preserve the X-limits of the axes
%xlim([0. 1.]);
%ylim([0 1]);
box('on');
hold('all');
% Create semilogx
plot(eta,gg1(:,1)-abs(kk1(:,1)),eta,gg1(:,2)-abs(kk1(:,2)));

% Create xlabel
xlabel({'$\bar{\omega}$'});

% Create ylabel
ylabel({'$G-K/\epsilon$'});
%,'XLim',[0.01:10])

stop;


