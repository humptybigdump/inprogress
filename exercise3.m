% Modeling of Reactions
% Exercise 3: Freundlich sorption
% s = K*c^n
% total mass:
% m = Vw*c + ms*s = (Vw + ms*K*c^(n-1))*c
% Picard iteration:
% c_new = m/(Vw + ms*K*c_old^(n-1))
clear variables
close all
clc

% coefficients
n_Fr  = 0.7;
K_Fr  = 2;    % [mol^.3m^2.1/kg]
rho_s = 2650; % [kg/m3]
poros = 0.4;

% relative mass-balance error
tol=1e-7;

% mass of solids and volume of water in 1m3 of bulk volume
ms = rho_s*(1-poros);
Vw = poros;

% total mass from initial concentration
c0 = 10; % [mol/m3]
s0 = 0;  % [mol/kg]
m  = Vw*c0 + ms*s0; % [mol]

%% Picard iteration
disp('Solve equilibration using Picard iteration')
tic
% iteration
c = c0;
s = c^n_Fr*K_Fr;
m_error = m-Vw*c-ms*s;
iter = 0;
while abs(m_error)>tol*m
      iter=iter+1;
      c = m/(Vw + ms*K_Fr*c^(n_Fr-1));
      s = K_Fr*c^n_Fr;
      m_error = m-Vw*c-ms*s;
      fprintf('iteration %2.2i: c = %8.3g mol/m3, error = %8.3g mol\n',...
              [iter,c,m_error])
end
fprintf('sorbing-phase concentration %g mol/kg\n',s)
toc

%% Newton iteration
disp('Solve equilibration using Newton iteration')
tic
% iteration
c = c0;
iter = 0;
s = K_Fr*c^n_Fr;
res = m-Vw*c-ms*s;
while abs(res)>tol*m
      iter=iter+1;
      dresdc = -Vw -ms*K_Fr*n_Fr*c^(n_Fr-1);
      dc = - res/dresdc;
      fac= 1;
      while c+fac*dc < 0
         fac = fac*.9;
      end
      c = c + fac*dc;
      s = K_Fr*c^n_Fr;
      res = m - Vw*c - ms*s;
      fprintf('iteration %2.2i: c = %8.3g mol/m3, error = %8.3g mol\n',...
              [iter,c,res])
end
fprintf('sorbing-phase concentration %g mol/kg\n',s)
toc
