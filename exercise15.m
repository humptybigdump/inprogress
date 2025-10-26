clear all
close all
clc

% Compute reductive complete dechlorination of PCE
% parameters
r_max = [200, 100, 100, 50]; % [umol/L/d]
K_CE  = [0.4,   1,   1,  3]; % MiMen coeff. of chlorinated ethene [umol/L]
K_EtOH= 150;                 % MiMen coeff. of EtOH

c0 = [200,0,0,0,0,400];     % [umol/L/d]

tspan=[0:.1:30];
options=odeset('NonNegative',1:6);
[Tnon,Cnon]=ode15s(@myode,tspan,c0,options,r_max,K_CE,K_EtOH,false);
[Tcomp,Ccomp]=ode15s(@myode,tspan,c0,options,r_max,K_CE,K_EtOH,true);

set(gcf,'outerposition',get(0,'ScreenSize'))
tiledlayout(1,2,"TileSpacing","compact")
nexttile(1)
plot(Tnon,Cnon,'LineWidth',1)
xlabel('t [d]')
ylabel('c [\mumol/L]')
title('Without Competitive Inhibition')
legend('PCE','TCE','DCE','VC','ETH','EtOH')

nexttile(2)
plot(Tcomp,Ccomp,'LineWidth',1)
xlabel('t [d]')
ylabel('c [\mumol/L]')
title('With Competitive Inhibition')
legend('PCE','TCE','DCE','VC','ETH','EtOH')

function dcdt=myode(t,c,r_max,K_CE,K_EtOH,iscompetitive)
dcdt=zeros(size(c));
% concentrations [umol/L]
% 1: PCE
% 2: TCE
% 3: DCE
% 4: VC
% 5: ETH
% 6: EtOH
c_PCE=c(1);
c_TCE=c(2);
c_DCE=c(3);
c_VC= c(4);
c_ETH=c(5);
c_EtOH=c(6);
K_PCE=K_CE(1);
K_TCE=K_CE(2);
K_DCE=K_CE(3);
K_VC =K_CE(4);
r_max_PCE=r_max(1);
r_max_TCE=r_max(2);
r_max_DCE=r_max(3);
r_max_VC =r_max(4);

if iscompetitive
   % common factor in the denominator
   same=c_EtOH/(K_EtOH+c_EtOH)/...
       (1+c_PCE/K_PCE+c_TCE/K_TCE+c_DCE/K_DCE+c_VC/K_VC);
   r_PCE = r_max_PCE*c_PCE/K_PCE*same;
   r_TCE = r_max_TCE*c_TCE/K_TCE*same;
   r_DCE = r_max_DCE*c_DCE/K_DCE*same;
   r_VC  = r_max_VC *c_VC /K_VC *same;
else
   r_PCE = r_max_PCE*c_EtOH/(K_EtOH+c_EtOH)*c_PCE/(c_PCE+K_PCE);
   r_TCE = r_max_TCE*c_EtOH/(K_EtOH+c_EtOH)*c_TCE/(c_TCE+K_TCE);
   r_DCE = r_max_DCE*c_EtOH/(K_EtOH+c_EtOH)*c_DCE/(c_DCE+K_DCE);
   r_VC  = r_max_VC *c_EtOH/(K_EtOH+c_EtOH)*c_VC /(c_VC +K_VC);
end


dcdt(1)=-r_PCE;
dcdt(2)=+r_PCE-r_TCE;
dcdt(3)=+r_TCE-r_DCE;
dcdt(4)=+r_DCE-r_VC;
dcdt(5)=+r_VC;
dcdt(6)=-0.5*(r_PCE+r_TCE+r_DCE+r_VC);
end