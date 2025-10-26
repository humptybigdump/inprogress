function [Mmod,rmod]=gwdiri(M,r,noddir,phidir);
% GWDIRI creates  Dirichlet boundary conditions at the
% first and last colon of nodes
% INPUT
% M : original stiffness matrix (nnod x nnod)
% r : original right-hand side matrix (nnod x 1)
% noddir: vector of the node numbers
% phidir: vector of the head values
% OUTPUT
% Mmod: modified stiffness matrix
% rmod: modified right-hand side vector

%disp('Incorporate Dirichlet boundary conditions')

rmod=r;

rmod=rmod-M(:,noddir)*phidir';
rmod(noddir)=phidir;

% Modify the matrix
Mmod=rowcoldel(M,noddir,1);
