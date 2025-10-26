clear variables
close all
clc

% Define parameters
Vtot = 10;              % total volume [L]
Vw   = 0.75*Vtot;       % volume of water [L]
rho_s= 1.5;             % mass density of the resin [kg/L]
m_s  = 0.25*Vtot*rho_s; % mass of the resin [kg]
s_max= 10;              % sorption capacity [mol/kg]
K = [0.5, 5];           % half-saturation concentrations [mol/L]
tol = 1e-6;             % tolerated relative mass-balance error [-]

% Initial problem
c_ini= [1, 0]; % initial concentrations [mol/L]

s_ini= s_max*c_ini./K/(1+sum(c_ini./K));

m_ini_w = c_ini*Vw;         % initial masses in the water [mol]
m_ini_s = s_ini*m_s;        % initial masses sorbed [mol]
m_ini   = m_ini_w+m_ini_s;  % total masses [mol]

fprintf('initial sorbing-phase conc.: %8.3g mol/kg\n',s_ini(1))
fprintf('initial total mass:          %8.3g mol\n',m_ini(1))

% reequilbration problem (total masses [mol]
m_new = [m_ini_s(1), Vw*10];  % compound A: only sorbed
                              % compound B: only in water

% initial guess: both compounds only in the aqueous phase
c = m_new/Vw;
% compute the mass balance errors
mysum = 1+sum(c./K);
s = s_max*c./(K*mysum);
m_error = m_new - c*Vw - s*m_s;

% Picard iteration
iter=0;
while max(abs(m_error)./m_new) > tol
    % increase counter
    iter = iter+1;
    % update aqueous-phase concentrations
    c = m_new./(Vw+m_s*s_max./K/mysum);
    % update 1+sum(c_j/K_j)
    mysum = 1+sum(c./K);
    % update sorbing-phase concentrations
    s = s_max*c./(K*mysum);
    % update mass-balance error
    m_error = m_new - c*Vw - s*m_s;
end
disp('After reequilibration')
fprintf('number of iterations %2.2i\n',iter)
fprintf('c = %8.3g mol/L\n',c)
fprintf('s = %8.3g mol/kg\n',s)
fprintf('mass-balance error = %8.3g mol\n',m_error)