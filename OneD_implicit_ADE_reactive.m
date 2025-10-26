function OneD_implicit_ADE_reactive
% Generic reactive transport model
% 1-D ADE coupled to reactions using the global implicit coupling approach
% This program is written as function to allow for multiple sub-functions
%
% On the internal numbering
% n_mob and n_imm are the numbers of mobile and immobile compounds
% n_comp is the total number of compounds
% n_cells is the number of cells
% c(1:n_comp:end) is the vector of concentrations of the first compound in
% all cells
% c(2:n_comp:end) is the vector of concentrations of the second compound in
% all cells
% and so forth
%
% Note: The first n_mob compounds are the mobile compounds
%
% c((ix-1)*n_comp+1:ix*c_comp) is the vector of all concentrations within
% cell ix
%
% Olaf A. Cirpka, University of Tuebingen, Center for Applied Geoscience
% (c) 2013

clc
close all

% Parameters

% Geometry of the domain
dx = 0.01;           % grid spacing [m]
L = 1;               % length [m]
x = [0.5*dx:dx:L];   % spatial coordinates of the cell centers [m] 
n_cells = length(x); % number of cells
A = pi*0.025^2;      % bulk cross-sectional area [m^2]

% Flow
Q = 1e-3/3600;       % discharge [m^3/s]
poros=0.4;           % porosity [-]
v=Q/A/poros;         % seepage velocity

% Number of mobile and immobile compounds
n_mob = 3;           % number of mobile compounds
n_imm = 0;           % number of immobile compounds
n_comp=n_mob+n_imm;  % number of compounds

names={'A','B','Product'}; % names of the compounds

% Dispersive transport parameters
alpha = 0.01;        % dispersivity [m] - same for all compounds
Dp = [1e-9,0.3e-9,0.5e-9];  % pore diffusion coefficient [m^2/s] 
                     % - one value for each mobile compound
D = alpha*abs(v)+Dp; % dispersion coefficient of all mobile compounds [m2/s]

% TVD scheme for advection ?
TVD=false;

% Reactive parameters
r_max = 1e-3;        % maximum reaction rate [mol/m^3/s]
K1    = 0.1;         % Michaelis-Menten coefficient compound 1 [mol/m^3]
K2    = 0.1;         % Michaelis-Menten coefficient compound 2 [mol/m^3]

%Initial concentrations
c0 = zeros(n_cells*n_comp,1); % can be modified to account for different 
                              % initial values

c_in = [1.0,1.5,0];    % inflow concentration [mol/m^3]
                       % - one value for each mobile compound

% Time span of simulation
tspan = [0 43200];


% Things needed for the ODE solver
% sparsity pattern for ODE solver
S = transsparse(n_comp,n_cells);
% set options of ODE solver
options =odeset('OutputFcn',@plot_profile,'jpattern',S);

% Initialize graphical output
figure (1)
set(gcf,'outerposition',get(0,'screensize'))

% call the ODE solver
[T_sim,C_sim]=ode15s(@ode_transport,tspan,c0,options);

figure(2)
plot(T_sim,C_sim(:,(n_cells-1)*n_comp+[1:n_mob]));
xlabel('t [s]')
ylabel('c [mmol/L]')
legend(names)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function dcdt=ode_transport(t,c)
% ODE function for reactive transport
% This is an embedded function so that all local variables of the calling
% function are available
%
% t       : current time [s]
% c       : vector of all concentrations [mol/m^3]
% dcdt    : rate of change of concentrations [mol/m^3/s]
%
% n_cells : number of cells
% dx      : grid spacing
% Q       : discharge at profiles [m3/s]
% D       : dispersion coefficient at profile [m2/s]
% A       : cross-sectional area at profile [m2]
% c_in    : input concentration 

% initialize rate of change of concentrations
dcdt = zeros(size(c));

% loop over all mobile compounds
for ic=1:n_mob
    cvec=c(ic:n_comp:end);
    % spatial derivative
    gradc=diff(cvec)/dx;
    % advection
    if TVD
       % extend the concentration vector :
       % upstream end: inflow concentration
       % downstream end: gradient assumed zero
       cext = [c_in(ic);cvec;cvec(end)];
       % reconstruct gradient within the cells
       s_1  = [diff(cext)/dx;0]; s_1(1) = 0;
       s_2  = [0;diff(cext)/dx];
       s = zeros(size(s_1));
       % van Leer limiter
       s(s_1.*s_2>0)= 2*s_1(s_1.*s_2>0).*s_2(s_1.*s_2>0)./...
                     (s_1(s_1.*s_2>0)+s_2(s_1.*s_2>0));
       % now construct concentration at interface
       c_up = cext(1:end-1)+s(1:end-1)*dx/2; 
    else
       % advection of the substrate with upwind differentiation
       c_up = [c_in(ic);cvec]; 
    end
    % resulting concentration change
    dcdt(ic:n_comp:end)=-diff(c_up)*v/dx;
    % dispersion
    dcdt(ic:n_comp:end)=dcdt(ic:n_comp:end) + ([gradc;0]-[0;gradc])*D(ic)/dx;
end

% reactions
% CHANGE HERE THE REACTION LAW ACCORDING TO YOUR NEEDS
% current example: A+B->product according to dual Michaelis-Menten kinetics
% unpack column vectors of individual concentrations:
c_A =  c(1:n_comp:end);
c_B =  c(2:n_comp:end);

% double Michaelis-Menten rate law (vectorized)
rate  =  r_max*c_A./(K1+c_A).*c_B./(K2+c_B);

% Rate of change of concentration (compound 1)
dcdt(1:n_comp:end) = dcdt(1:n_comp:end) - rate;
% Rate of change of concentration (compound 2)
dcdt(2:n_comp:end) = dcdt(2:n_comp:end) - rate;
% Rate of change of concentration (compound 3)
dcdt(3:n_comp:end) = dcdt(3:n_comp:end) + rate;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function status=plot_profile(t,c,flag)
% Generic plot function
% This is an embedded function so that all local variables of the calling
% function are available
%
% t       : current time [s]
% c       : vector of all concentrations [mol/m^3]
% dcdt    : rate of change of concentrations [mol/m^3/s]

switch flag
    case 'init'
    case 'done'
    otherwise
    figure(1)
    for ii=1:size(t,1)
        cplot = reshape(c(:,ii),n_comp,n_cells);
        for ic=1:n_comp
            subplot(n_comp,1,ic)
            plot(x,cplot(ic,:),'k');
            set(gca,'fontsize',10);
            xlim([0 L]);
            xlabel('x [m]');
            ylabel('c [mmol/l');
            title([names{ic} sprintf(' at t= %10.3g s',t(ii))])
        end
        drawnow;
    end
end
status=0;
end

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function S = transsparse(n_comp,n_cells)
% computes sparsity pattern for transport
% order of entries
% (ii-1)*n_comp + 1,2...n_aq_comp : 
% aqueous-phase concentrations in cell ii
% (ii-1)*n_comp + n_mob + 1,2...n_imm :
% immobile concentrations in cell ii

% vectors of the sparse matrix
ivec=zeros(3*n_cells*(n_comp)^2,1);
jvec=zeros(size(ivec));
avec= ones(size(ivec));
counter=1;
for ii=1:n_cells
    % connection between all components within a cell
    for jj=1:n_comp
        for kk=1:n_comp
            ivec(counter)=(ii-1)*n_comp+jj;
            jvec(counter)=(ii-1)*n_comp+kk;
            counter=counter+1;
            % transport connection to upstream node
            if (ii>1)
                ivec(counter)=(ii-1)*n_comp+jj;
                jvec(counter)=(ii-2)*n_comp+kk;
                counter=counter+1;
            end
            % transport connection to downstream node
            if (ii<n_cells)
               ivec(counter)=(ii-1)*n_comp+jj;
               jvec(counter)=ii*n_comp+kk;
               counter=counter+1;
            end
        end
    end
end
S=sparse(ivec(1:counter-1),jvec(1:counter-1),avec(1:counter-1));
end
