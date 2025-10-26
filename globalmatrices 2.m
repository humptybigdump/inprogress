function [Mstoreglob,Mmobglob,Mrechglob] = globalmatrices(vert,tria,T,S)
% Set up global storage and mobility matrices for 1-D groundwater flow
nel  = size(tria,1); % number of elements
nnod = size(vert,1); % number of nodes

% initialize vectors of row- and column-indices and of element entries
ivec = zeros(nel*9,1);     % global row index
jvec = zeros(nel*9,1);     % global column index
storevec = zeros(nel*9,1); % element entries of the global storage matrix
mobvec = zeros(nel*9,1);   % element entries of the global mobility matrix
A = zeros(nel,1);          % vector of all element areas [m2]

% loop over all elements
for iel=1:nel
    nodes = tria(iel,:); % nodes of the element
    % local storage, mobility matrices and area of element
    [Mstoreloc,Mmobloc,A(iel)] = localmatrices(vert(nodes,:),T(iel),S(iel));
    ivec((iel-1)*9+(1:9)) = [nodes(1);nodes(2);nodes(3);...
                             nodes(1);nodes(2);nodes(3);...
                             nodes(1);nodes(2);nodes(3)];
    jvec((iel-1)*9+(1:9)) = [nodes(1);nodes(1);nodes(1);...
                             nodes(2);nodes(2);nodes(2);...
                             nodes(3);nodes(3);nodes(3)];
    storevec((iel-1)*9+(1:9))=Mstoreloc(:);
    mobvec((iel-1)*9+(1:9))=Mmobloc(:);
end
% Define sparse matrices
Mstoreglob=sparse(ivec,jvec,storevec);
Mmobglob  =sparse(ivec,jvec,mobvec);

% And now for the recharge matrix
ivec = zeros(nel*3,1);     % global row index
jvec = zeros(nel*3,1);     % global column index
rechvec = zeros(nel*3,1);  % element entries of the recharge matrix
for iel=1:nel
    nodes = tria(iel,:); % nodes of the element
    % local storage, mobility, and recharge matrices
    ivec((iel-1)*3+(1:3)) = nodes';
    jvec((iel-1)*3+(1:3)) = ones(3,1)*iel;
    rechvec((iel-1)*3+(1:3)) = ones(3,1)*A(iel)/3;
end
Mrechglob =sparse(ivec,jvec,rechvec,nnod,nel);
