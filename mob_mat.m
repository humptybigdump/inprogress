function Mmob = mob_mat(ntube,nsec,Qin,net,al,at,Dm,por,Dttype)
% this is a new code by WN / 01.09.2010
% missing functionality: topdiff, botdiff is not implemented!


% -------------------------------------
% initial memory allocation
% -------------------------------------
q               = zeros(ntube*nsec,1);     % local representative velocity within each cell
itot            = zeros(5*ntube*nsec,1);   % i index for sparse mobility matrix
jtot            = zeros(5*ntube*nsec,1);   % j index for sparse mobility matrix
Atot            = zeros(5*ntube*nsec,1);   % value   for sparse mobility matrix

% -------------------------------------
% getting grid data
% -------------------------------------
% basic grid dimensions
n_el            = [ntube   nsec  ];
n_pts           = [ntube+1 nsec+1];
nel             = prod(n_el );
npts            = prod(n_pts);

% local stencil: how to address neighboring element, in relative index
incidence_el    = [0 1 0 1] + n_pts(1)*[0 0 1 1];
% local stencil: how to address neighboring points within the grid, in relative index
incidence_pts   = [-n_pts(1)+[-1 0 1] [-1 0 1] +n_pts(1)+[-1 0 1]];

% -------------------------------------
% assessing indicence information
% -------------------------------------
% formal list of all elements
all_el          = reshape(1:nel,n_el);
all_pts         = reshape(1:npts,n_pts);
% index list for lower left points of all elements
el2pts          = reshape(all_pts(1:n_el(1),1:n_el(2)),n_el);
% incidence matrix that has pointers to all points of all elements
lole            = el2pts+incidence_el(1); % lower left
uple            = el2pts+incidence_el(2); % upper left
lori            = el2pts+incidence_el(3); % lower right
upri            = el2pts+incidence_el(4); % upper right

% -------------------------------------
% geometry of edges
% -------------------------------------
w_lef           = sqrt((net.x(lole)-net.x(uple)).^2 + (net.y(lole)-net.y(uple)).^2);
w_rig           = sqrt((net.x(lori)-net.x(upri)).^2 + (net.y(lori)-net.y(upri)).^2);
w_bot           = sqrt((net.x(lole)-net.x(lori)).^2 + (net.y(lole)-net.y(lori)).^2);
w_top           = sqrt((net.x(uple)-net.x(upri)).^2 + (net.y(uple)-net.y(upri)).^2);

% -------------------------------------
% positions of element centers and edge centers
% -------------------------------------
xcen            = 0.25 * (net.x(lole) + net.x(uple) + net.x(lori) + net.x(upri));
ycen            = 0.25 * (net.y(lole) + net.y(uple) + net.y(lori) + net.y(upri));
xlef            = 0.50 * (net.x(lole) + net.x(uple));
ylef            = 0.50 * (net.y(lole) + net.y(uple));
xrig            = 0.50 * (net.x(lori) + net.x(upri));
yrig            = 0.50 * (net.y(lori) + net.y(upri));
xbot            = 0.50 * (net.x(lole) + net.x(lori));
ybot            = 0.50 * (net.y(lole) + net.y(lori));
xtop            = 0.50 * (net.x(uple) + net.x(upri));
ytop            = 0.50 * (net.y(uple) + net.y(upri));

% -------------------------------------
% local representative velocity in each cell and along edges
% -------------------------------------
% effective width of cells
width           = 0.5*(w_lef + w_rig);
% local representative velocity in each cell
q               = (Qin/ntube)./width;
q               = reshape(q,ntube,nsec);

% -------------------------------------
% reconstruct conductivity field in stramline oriented coordinates
% -------------------------------------
lengthel=0.5*(w_bot+w_top);
deltaphi=net.phi(1,1)-net.phi(1,2);
KK=abs(q.*lengthel./deltaphi);
% reconstrcut effective grain size unsing Hazen
d_eff=((100.*KK).^0.5)./1000; % K in m/s, d in m

% -------------------------------------
% Peclet number in each cell
% -------------------------------------
Pe = d_eff.*q./reshape(por,ntube,nsec)/Dm;

% -------------------------------------
% transverse dispersion coefficient times porosity in each cell
% -------------------------------------
switch Dttype
    case 1
        % Standard Scheidegger model with constant at
        Dt = at*q + Dm*reshape(por,ntube,nsec).^2;
    case 2
        % Standard Scheidegger model with at = d_eff/10
        Dt = 0.1*d_eff.*q + Dm*reshape(por,ntube,nsec).^2;
    case 3
        % according to famous Chiogna
        Dt = d_eff./sqrt(123+Pe).*q + Dm*reshape(por,ntube,nsec).^2;
end

% -------------------------------------
% mobility matrix
% -------------------------------------

% CONNECTION TO LEFT CELL (flux across left edge)
here            = all_el(:,2:end  );      % all cells that have a left neighbor
left            = all_el(:,1:end-1);      % all left neighbors
ii_min          = 1;                      % smallest index of addition to sparse matrix touched here
ii_max          = ii_min + numel(here)-1; % largest  index of addition to sparse matrix touched here
% length of line from cell center via left-egde center to center of left neighbour cell
len             = sqrt((xlef(here)-xcen(left)).^2 + (ylef(here)-ycen(left)).^2) + ...
                  sqrt((xlef(here)-xcen(here)).^2 + (ylef(here)-ycen(here)).^2);
poredge         = 0.5 * (por(here(:)) + por(left(:)));
% longitudinal dispersive flux across left edge
aha             = (Qin/ntube*al+Dm*w_lef(here(:)).*poredge.^2)./len(:);
% preparing sparse matrix
itot(ii_min:ii_max) = here(:);
jtot(ii_min:ii_max) = left(:);
Atot(ii_min:ii_max) = -Qin/ntube-aha; % advective and longitudinal dispersive flux
% summing up all edge terms
huhu            = zeros(n_el);
huhu(here(:))   = aha;

% CONNECTION TO LOWER CELL (flux across lower edge)
here            = all_el(2:end  ,:);      % all cells that have a lower neighbor
belo            = all_el(1:end-1,:);      % all lower neighbors
ii_min          = ii_max+1;               % smallest index of addition to sparse matrix touched here
ii_max          = ii_min + numel(here)-1; % largest  index of addition to sparse matrix touched here
% length of line from cell center via lower-egde center to center of lower neighbour cell
%len             = sqrt((xbot(here)-xcen(belo)).^2 + (ybot(here)-ycen(belo)).^2) + ...
%                  sqrt((xbot(here)-xcen(here)).^2 + (ybot(here)-ycen(here)).^2);
% length of line from cell center to lower-egde center in neighbor cell
lenbelo         = sqrt((xbot(here)-xcen(belo)).^2 + (ybot(here)-ycen(belo)).^2);
% length of line from cell center to lower-egde center in this cell
lenhere         = sqrt((xbot(here)-xcen(here)).^2 + (ybot(here)-ycen(here)).^2);
% transverse dispersive flux across lower edge
%aha             = (0.5*(q(here(:))+q(belo(:)))*at+Dm*0.5.*(por(here(:))+por(belo(:)))).*w_bot(here(:))./len(:);
%aha             = 0.5*(Dt(here(:))+Dt(belo(:))).*w_bot(here(:))./len(:);
% transverse dispersive flux across lower edge with harmonic weighting of Dt
aha             = w_bot(here(:))./(lenhere(:)./Dt(here(:))+lenbelo(:)./Dt(belo(:)));
% preparing sparse matrix
itot(ii_min:ii_max) = here(:);
jtot(ii_min:ii_max) = belo(:);
Atot(ii_min:ii_max) = -aha; % only transverse dispersive flux
% summing up all edge terms
huhu(here(:))       = huhu(here(:)) + aha;

% CONNECTION TO UPPER CELL (flux across upper edge)
here            = all_el(1:end-1,:);      % all cells that have an upper neighbor
abov            = all_el(2:end  ,:);      % all upper neighbors
ii_min          = ii_max+1;               % smallest index of addition to sparse matrix touched here
ii_max          = ii_min + numel(here)-1; % largest  index of addition to sparse matrix touched here
% length of line from cell center via upper-egde center to center of upper neighbour cell
%len             = sqrt((xtop(here)-xcen(abov)).^2 + (ytop(here)-ycen(abov)).^2) + ...
%                  sqrt((xtop(here)-xcen(here)).^2 + (ytop(here)-ycen(here)).^2);
% length of line from cell center to upper-egde center in neighbor cell
lenabov         = sqrt((xtop(here)-xcen(abov)).^2 + (ytop(here)-ycen(abov)).^2);
% length of line from cell center to upper-egde center in this cell
lenhere         = sqrt((xtop(here)-xcen(here)).^2 + (ytop(here)-ycen(here)).^2);
% transverse dispersive flux across upper edge
%aha             = (0.5*(q(here(:))+q(abov(:)))*at+Dm*0.5.*(por(here(:))+por(abov(:)))).*w_top(here(:))./len(:);
%aha             = 0.5*(Dt(here(:))+Dt(abov(:))).*w_top(here(:))./len(:);
% transverse dispersive flux across lower edge with harmonic weighting of Dt
aha             = w_top(here(:))./(lenhere(:)./Dt(here(:))+lenabov(:)./Dt(abov(:)));
% preparing sparse matrix
itot(ii_min:ii_max) = here(:);
jtot(ii_min:ii_max) = abov(:);
Atot(ii_min:ii_max) = -aha; % only transverse dispersive flux
% summing up all edge terms
huhu(here(:))       = huhu(here(:)) + aha;

% CONNECTION TO RIGHT CELL (flux across right edge)
here            = all_el(:,1:end-1);      % all cells that have a right neighbor
righ            = all_el(:,2:end  );      % all right neighbors
ii_min          = ii_max+1;               % smallest index of addition to sparse matrix touched here
ii_max          = ii_min + numel(here)-1; % largest  index of addition to sparse matrix touched here
% length of line from cell center via left-egde center to center of left neighbour cell
len             = sqrt((xrig(here)-xcen(righ)).^2 + (yrig(here)-ycen(righ)).^2) + ...
                  sqrt((xrig(here)-xcen(here)).^2 + (yrig(here)-ycen(here)).^2);
% longitudinal dispersive flux across left edge
poredge=0.5.*(por(here(:))+por(righ(:)));
aha             = (Qin/ntube*al+Dm*w_rig(here(:)).*poredge.^2)./len(:);
% preparing sparse matrix
itot(ii_min:ii_max) = here(:);
jtot(ii_min:ii_max) = righ(:);
Atot(ii_min:ii_max) = -aha; % only longitudinal dispersive flux
% summing up all edge terms
huhu(here(:))       = huhu(here(:)) + aha;

% STORAGE WITHIN CELL
ii_min          = ii_max+1;               % smallest index of addition to sparse matrix touched here
ii_max          = ii_min + numel(huhu)-1; % largest  index of addition to sparse matrix touched here
itot(ii_min:ii_max) = all_el(:);
jtot(ii_min:ii_max) = all_el(:);
Atot(ii_min:ii_max) = Qin/ntube+huhu;

% assessing sparse matrix
Mmob  = sparse(itot(1:ii_max),jtot(1:ii_max),Atot(1:ii_max));






