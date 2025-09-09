function [Mstoreglob,Mmobglob,Mleakglob] = ...
    globalmatrices_leaky(xnod,incidence,K,S0,A,L)
% Set up global storage and mobility matrices for 1-D groundwater flow
nel  = size(incidence,1); % number of elements
nnod = size(xnod,1);      % number of nodes

% initialize vectors of row- and column-indices and of element entries
ivec = zeros(nel*4,1);     % global row index
jvec = zeros(nel*4,1);     % global column index
storevec = zeros(nel*4,1); % element entries of the global storage matrix
leakvec = zeros(nel*4,1);  % element entries of the global leakage matrix
mobvec = zeros(nel*4,1);   % element entries of the global mobility matrix

% loop over all elements
for iel=1:nel
    nodes = incidence(iel,:); % nodes of the element
    % local storage and mobility matrices
    [Mstoreloc,Mmobloc,Mleakloc] = localmatrices_leaky(...
                                  xnod(nodes),K(iel),S0(iel),A(iel),L(iel));
    ivec((iel-1)*4+(1:4)) = [nodes(1);nodes(2);nodes(1);nodes(2)];
    jvec((iel-1)*4+(1:4)) = [nodes(1);nodes(1);nodes(2);nodes(2)];
    storevec((iel-1)*4+(1:4))=Mstoreloc(:);
    leakvec((iel-1)*4+(1:4))=Mleakloc(:);
    mobvec((iel-1)*4+(1:4))=Mmobloc(:);
end
% Define sparse matrices
Mstoreglob=sparse(ivec,jvec,storevec);
Mleakglob=sparse(ivec,jvec,leakvec);
Mmobglob  =sparse(ivec,jvec,mobvec);