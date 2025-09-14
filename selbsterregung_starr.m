%Zusammenhang mod. Sommerfeldzahl, Exzentrizität, Verlagerungswinkel
%Feder-/Dämpferparameter
%Stabilit;
clear all;
eps=[0:0.01:1];
for i=1:length(eps)
sm(i)=2*(1-eps(i)^2)^2/(pi*eps(i)*sqrt(1-eps(i)^2+(4*eps(i)/pi)^2));
gam(i)=180*atan((pi/4)*sqrt((1-eps(i)^2)/eps(i)^2))/pi;
gam1(i)=atan((pi/4)*sqrt((1-eps(i)^2)/eps(i)^2));
sm1(i)=(1-eps(i)^2)^2/(eps(i)*sqrt(16*eps(i)^2+pi^2*(1-eps(i)^2)));
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

% tilde-Größen nach Gasch, starrer Laeufer
A0(i)=kxx(i)*kyy(i)-kxy(i)*kyx(i);
A1(i)=kxx(i)*cyy(i)+kyy(i)*cxx(i)-kxy(i)*cyx(i)-kyx(i)*cxy(i);
A21(i)=kxx(i)+kyy(i);
A22(i)=cxx(i)*cyy(i)-cxy(i)*cyx(i);
A3(i)=cxx(i)+cyy(i);
om(i)=A1(i)/A3(i);
etaz(i)=A1(i)*A22(i)*A3(i);
etan(i)=A1(i)*A1(i)+A0(i)*A3(i)*A3(i)-A1(i)*A21(i)*A3(i);
eta(i)=sqrt((A1(i)*A22(i)*A3(i))/(A1(i)*A1(i)+A0(i)*A3(i)*A3(i)-A1(i)*A21(i)*A3(i)));
so(i)=(0.4)^2/sm(i);
soo(i)=so(i)*eta(i);
%Größen nach San Andrés
keq(i)=A1(i)/A3(i);
whirl(i)=sqrt(((keq(i)-kxx(i))*(keq(i)-kyy(i))-kxy(i)*kyx(i))/A22(i));
ps(i)=sqrt(keq(i)/(whirl(i)*whirl(i)));
end;


figure2 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure2);
% Uncomment the following line to preserve the X-limits of the axes
xlim([0. 1.]);
ylim([0 1]);
box('on');
hold('all');

% Create semilogx
plot(eps,whirl);

% Create xlabel
xlabel({'Exzentrizitaet epsilon'});

% Create ylabel
ylabel({'Schwingfrequenz an der Stabilitätsgrenze'});
%,'XLim',[0.01:10])

figure3 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure3,'XScale','log','XMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
xlim([0.01 10]);
ylim([0 1]);
box('on');
hold('all');

% Create semilogx
semilogx(sm,whirl);

% Create xlabel
xlabel({'modifizierte Sommerfeldzahl'});

% Create ylabel
ylabel({'Schwingfrequenz an der Stabilitätsgrenze'});
%,'XLim',[0.01:10])

figure4 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure4);
% Uncomment the following line to preserve the X-limits of the axes
xlim([0. 1.]);
ylim([0 10]);
box('on');
hold('all');

% Create semilogx
plot(eps(1:76),eta(1:76));

% Create xlabel
xlabel({'Exzentrizitaet epsilon'});

% Create ylabel
ylabel({'Grenzdrehgeschwindigkeit $\bar{\omega}$'});
%,'XLim',[0.01:10])

figure3 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure3,'XScale','log','XMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
xlim([0.01 10]);
ylim([0 10]);
box('on');
hold('all');

% Create semilogx
semilogx(sm(1:76),eta(1:76));

% Create xlabel
xlabel({'modifizierte Sommerfeldzahl'});

% Create ylabel
ylabel({'Grenzdrehgeschwindigkeit $\bar{\omega}$'});
%,'XLim',[0.01:10])


