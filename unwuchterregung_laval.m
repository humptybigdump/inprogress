%Zusammenhang mod. Sommerfeldzahl, Exzentrizität, Verlagerungswinkel
%Feder-/Dämpferparameter
%Stabilit;
clear all;
global smi;
beta=0.4;
%Sou=0.16;
sok=0.5;
gamma(1)=0.05;
gamma(2)=0.1;
gamma(3)=1.;
gamma(4)=10.;
eta=[0.1:0.01:15];
for jj=1:4
ga=gamma(jj);
sigma=beta^2*sqrt(ga)/sok;
for i=1:length(eta)
sm(i)=sigma*eta(i);
smi=sm(i);
if (i>1)
eps(i)=fsolve(@epsilon1,eps(i-1));
else
   eps(i)=fsolve(@epsilon1,0.5);
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

lhs=[1/ga-eta(i)^2 0 -1/ga 0 0 0 0 0;
     0 1/ga-eta(i)^2 0 -1/ga  0 0 0 0;
     -1/ga 0 kxx(i)+1/ga kxy(i) 0 0 cxx(i) cxy(i);
     0 -1/ga kyx(i) kyy(i)+1/ga 0 0 cyx(i) cyy(i);
     0 0     0      0 1/ga-eta(i)^2 0 -1/ga 0;
     0 0     0      0 0 1/ga-eta(i)^2 0 -1/ga;
     0 0 -cxx(i) -cxy(i) -1/ga 0 kxx(i)+1/ga kxy(i);
     0 0 -cyx(i) -cyy(i) 0 -1/ga kyx(i) kyy(i)+1/ga];
rhs=[eps(i)*eta(i)^2; 0; 0; 0; 0; eps(i)*eta(i)^2; 0; 0];
sol=lhs\rhs;
gg(i)=0.5*(sqrt((sol(2)+sol(5))^2+(sol(1)-sol(6))^2)+sqrt((sol(2)-sol(5))^2+(sol(1)+sol(6))^2));
kk(i)=0.5*(sqrt((sol(2)+sol(5))^2+(sol(1)-sol(6))^2)-sqrt((sol(2)-sol(5))^2+(sol(1)+sol(6))^2));     
gg1(i,jj)=gg(i)/eps(i);
kk1(i)=kk(i)/eps(i);
end;
end;
%semilogy(eta*sqrt(gamma(4)),gg1(:,4));
figure2 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure2,'YScale','log','YMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
xlim([0. 1.5]);
ylim([0.5 100]);
box('on');
hold('all');

% Create semilogx
semilogy(eta*sqrt(gamma(1)),gg1(:,1),eta*sqrt(gamma(2)),gg1(:,2),eta,gg1(:,3),eta*sqrt(gamma(4)),gg1(:,4));

% Create xlabel
xlabel({'sqrt(\Gamma) \bar\omega'});

% Create ylabel
ylabel({'G/epsilon'});
%,'XLim',[0.01:10])
