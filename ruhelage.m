%Zusammenhang mod. Sommerfeldzahl, Exzentrizität, Verlagerungswinkel
%Feder-/Dämpferparameter
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
kxx(i)=k(1,1);
kxy(i)=k(1,2);
kyx(i)=k(2,1);
kyy(i)=k(2,2);
cxx(i)=c(1,1);
cxy(i)=c(1,2);
cyy(i)=c(2,2);
end;
figure7 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure7,'YScale','log','YMinorTick','on','XScale','log','XMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
xlim([0.01 10]);
ylim([0.1 100]);
box('on');
hold('all');

% Create semilogx
loglog(sm,sm.*cxx,sm,sm.*cxy,sm,sm.*cyy);
legend('cxx','cxy','cyy','Location','southeast');

% Create xlabel
xlabel({'modifizierte Sommerfeldzahl'});

% Create ylabel
ylabel({'bezogene Dämpfung'});
%,'XLim',[0.01:10])


figure6 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure6,'YScale','log','YMinorTick','on','XScale','log','XMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
xlim([0.01 10]);
ylim([0.1 100]);
box('on');
hold('all');

% Create semilogx
loglog(sm,sm.*kxx,sm,sm.*kxy,sm,abs(sm.*kyx),sm,sm.*kyy);
legend('kxx','kxy','|kyx|','kyy','Location','southeast');

% Create xlabel
xlabel({'modifizierte Sommerfeldzahl'});
ylabel({'bezogene Steifigkeit'});

figure5 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure5,'YScale','log','YMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
ylim([0.1 100]);
box('on');
hold('all');

% Create semilogx
semilogy(eps,sm.*cxx,eps,sm.*cxy,eps,sm.*cyy);
legend('cxx','cxy','cyy','Location','southwest');

% Create xlabel
xlabel({'bezogene Verlagerung {\epsilon}'});

% Create ylabel
ylabel({'bezogene Dämpfung'});
%,'XLim',[0.01:10])


figure4 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure4,'YScale','log','YMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
ylim([0.1 100]);
box('on');
hold('all');

% Create semilogx
semilogy(eps,sm.*kxx,eps,sm.*kxy,eps,abs(sm.*kyx),eps,sm.*kyy);
legend('kxx','kxy','|kyx|','kyy','Location','southwest');

% Create xlabel
xlabel({'bezogene Verlagerung {\epsilon}'});

% Create ylabel
ylabel({'bezogene Steifigkeit'});
%,'XLim',[0.01:10])


figure3 = figure('PaperSize',[20.98 29.68]);

% Create axes
%axes('Parent',figure3,'XScale','log','XMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
%xlim([0.01 10]);
%box('on');
%hold('all');

% Create semilogx
polar(gam1,eps);

% Create xlabel
%xlabel({'modifizierte Sommerfeldzahl S_m'});

% Create ylabel
%ylabel({'Verlagerungswinkel gamma [°]'});
%,'XLim',[0.01:10])

figure2 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure2,'XScale','log','XMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
xlim([0.01 10]);
box('on');
hold('all');

% Create semilogx
semilogx(sm,gam);

% Create xlabel
xlabel({'modifizierte Sommerfeldzahl S_m'});

% Create ylabel
ylabel({'Verlagerungswinkel  {\gamma} [°]'});
%,'XLim',[0.01:10])
semilogx(sm,gam)
%stop;

%semilogx(sm,eps)
figure1 = figure('PaperSize',[20.98 29.68]);

% Create axes
axes('Parent',figure1,'XScale','log','XMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
xlim([0.01 10]);
box('on');
hold('all');

% Create semilogx
semilogx(sm,eps);

% Create xlabel
xlabel({'modifizierte Sommerfeldzahl S_m'});

% Create ylabel
ylabel({'bezogene Verlagerung  {\epsilon}'});
%,'XLim',[0.01:10])
