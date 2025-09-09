function [Mstore,Mmob,Mleak] = localmatrices_leaky(xnod,K,S0,A,L)
% xnod: coordinates of the two nodes
% K: conductivity in the element [m/s]
% S0: specific storativity in the element [1/m]
% A: corss-sectional area [m^2]
% L: leakance = (conductivity of leaky layer)*(width of leaky
% layer)/(thickness of leaky layer) [m/s]

dx = diff(xnod);
Mstore = A*S0*dx*[1/3, 1/6;...
                  1/6, 1/3];     % [m2]
Mmob   = A*K/dx *[  1,  -1;...
                   -1,   1];     % [m2/s]
Mleak  = L*dx*   [1/3, 1/6;...
                  1/6, 1/3];     % [m2/s]
