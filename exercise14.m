close all
clear all
clc

% Vector of State Variables (terminal electron acceptors)
% 1: dissolved oxygen
% 2: nitrate
% 3: sulfate
% 4: DOC
% 5: Methane

% define parameters
gamma = [1, 0.8, 0.5, 0.5]; % stoich. coeff. of the DO,nitrate, sulfate, ...
                            % and methane vs. DOC  [-]
rmax  = [0.6, 0.4, 0.3, 0.2]; % rate coefficient of DOC-decay [mmol/L/d]
K     = [0.016, 0.16, 0.005, 0.011]; % MiMen coefficients [mmol/L]
I     = [3e-3, 4e-3, 6e-3]; % inihibition constants [mmol/L]
% put parameters into a structure
par=struct('gamma',gamma,'rmax',rmax,'K',K,'I',I);

% initial condition
c0    = [0.25, 0.8, 2, 10, 0]; % initial concentration [mmol/L]

% time span
tspan= [0 50];

options=odeset('NonNegative',1:4);
[T,C]=ode15s(@myode,tspan,c0,options,par);

% postprocess rates
R=nan(size(C(:,1:4)));
for ii=1:length(T)
    bla = myode(T(ii),C(ii,1:4),par);
    R(ii,1)=-bla(1)/gamma(1);
    R(ii,2)=-bla(2)/gamma(2);
    R(ii,3)=-bla(3)/gamma(3);
    R(ii,4)= bla(5)/gamma(4);
end

set(gcf,'outerposition',get(0,'ScreenSize'))
tiledlayout(1,2,"TileSpacing","compact")
nexttile(1)
CO=colororder;
yyaxis left
h1=plot(T,C(:,1),'-','Color',CO(1,:),'LineWidth',1);
hold on
h2=plot(T,C(:,2),'-','Color',CO(2,:),'LineWidth',1);
h3=plot(T,C(:,3),'-','Color',CO(3,:),'LineWidth',1);
h5=plot(T,C(:,5),'-','Color',CO(5,:),'LineWidth',1);
hold off
set(gca,'YColor','k')
xlabel('t [d]')
ylabel('c [mmol/L] (O_2, NO_3^-, SO_4^{2-}, CH_4)')
yyaxis right
h4=plot(T,C(:,4),'-','Color',CO(4,:),'LineWidth',1);
set(gca,'YColor','k')
ylabel('c [mmol/L] (DOC)')
ll=legend([h1 h2 h3 h4 h5],'O_2','NO_3^-','SO_4^{2-}','DOC','CH_4',...
          Location='best');
title(ll,'Compound')
title('Concentrations')

nexttile(2)
% remark: the methanogenesis rate is multiplied by 0.5 because half of the
% DOC involved is used as electron acceptor
plot(T,R.*[1 1 1 0.5],'LineWidth',1)
xlabel('t [d]')
ylabel('r_{DOC}^{(i)} [mmol/L/d]')
ll=legend('O_2','NO_3^-','SO_4^{2-}','DOC',Location='best');
title(ll,'TEA')
title('Reaction Rates of DOC as e^--Donor')

function dcdt=myode(t,c,par)
% concentrations [mmol/L]
c_DO  = c(1);
c_nit = c(2);
c_sul = c(3);
c_DOC = c(4);
% Stoichiometry TEA:DOC [-]
gamma_DO =par.gamma(1);
gamma_nit=par.gamma(2);
gamma_sul=par.gamma(3);
gamma_CH4=par.gamma(4);
% rate coefficient for different TEA [1/d]
rmax_DO =par.rmax(1);
rmax_nit=par.rmax(2);
rmax_sul=par.rmax(3);
rmax_DOC=par.rmax(4);
% Michaelis-Menten coefficient of the TEAs [mmol/l]
K_DO =par.K(1);
K_nit=par.K(2);
K_sul=par.K(3);
K_DOC=par.K(4);
% Inhibition constant of teh TEAs [mmol/L]
I_DO =par.I(1);
I_nit=par.I(2);
I_sul=par.I(3);

% reaction rate of DOC with different TEA
% MiMen term of DOC
fDOC  =c_DOC/(c_DOC+K_DOC);
% inhibition terms
fI_DO =I_DO/(c_DO+I_DO);
fI_nit=I_nit/(c_nit+I_nit);
fI_sul=I_sul/(c_sul+I_sul);

r_DO =rmax_DO *fDOC*c_DO/(c_DO +K_DO);
r_nit=rmax_nit*fDOC*c_nit/(c_nit+K_nit)*fI_DO;
r_sul=rmax_sul*fDOC*c_sul/(c_sul+K_sul)*fI_DO*fI_nit;
r_DOC=rmax_DOC*fDOC*fI_DO*fI_nit*fI_sul;

dcdt = zeros(size(c));
dcdt(1) = -gamma_DO *r_DO;
dcdt(2) = -gamma_nit*r_nit;
dcdt(3) = -gamma_sul*r_sul;
dcdt(4) = -r_DOC-r_DO-r_nit-r_sul;
dcdt(5) =  gamma_CH4*r_DOC;
end
