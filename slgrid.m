function [net,doagain] = slgrid(ntube,nsec,nx,dx,X,Y,psi,h,phiin,Qin)
% generates streamline oriented grid
% version 02. september 2010 / WN
doagain=false;
nnod = prod(nx+1);
botnod = [1:nx(2)+1:nnod];
topnod = botnod + nx(2);

% compute contour lines of streamlines
Cpsi=contourc([0:nx(1)]*dx(1),[0:nx(2)]*dx(2),psi,[0:ntube]/ntube*Qin);

% initialize net variables
net.x = zeros(ntube+1,nsec+1);
net.y = zeros(ntube+1,nsec+1);
[net.phi,net.psi]=meshgrid([nsec:-1:0]*phiin/nsec,[0:ntube]*Qin/ntube);

% discretization of phi
phi_int = [nsec:-1:0]*phiin/nsec;

if (~doagain)
  % get the length of all contour lines
  iC=1;
  npts   = zeros(ntube+1,1);
  nstart = zeros(ntube+1,1);
  nend   = zeros(ntube+1,1);
  for ii=1:ntube+1
    npts(ii)   = Cpsi(2,iC);
    nstart(ii) = iC + 1;
    nend(ii)   = iC + npts(ii);
    iC=iC+npts(ii)+1;
  end
  npts_max = max(npts);
  
  % get all lines from contour variable
  line.x   = zeros(ntube+1,npts_max);
  line.y   = zeros(ntube+1,npts_max);
  for ii=1:ntube+1
    line.x(ii,1:npts(ii))   = Cpsi(1,nstart(ii):nend(ii));
    line.y(ii,1:npts(ii))   = Cpsi(2,nstart(ii):nend(ii));
  end
  
  % artificially fix first and last line
  line.x  (1,:) = 0;
  line.y  (1,:) = 0;
  line.x  (1,1:nx+1) = [0:nx(1)]*dx(1);
  npts(1)       = nx(1)+1;
  line.x  (end,:) = 0;
  line.y  (end,:) = nx(2)*dx(2);
  line.x  (end,1:nx+1) = [0:nx(1)]*dx(1);
  npts(end)       = nx(1)+1;
  
  % get phi values at line x/y positions
  line.phi = interp2(X,Y,h,line.x,line.y);
  
  % artificially fix first and last line
  line.phi(1,1:nx+1) = h(botnod)';
  line.phi(end,1:nx+1) = h(topnod)';
  
  % check for pathological case
  for ii=1:ntube+1
    if (max(diff(line.phi(ii,1:npts(ii))))>=0)
      doagain=true;
    end
  end
  
  if doagain == true, return, end
  
  % interpolate to get x positions
  for ii=1:ntube+1
    net.x(ii,:)=interp1(line.phi(ii,1:npts(ii)),line.x(ii,1:npts(ii)),...
                        phi_int,'linear','extrap');
    net.y(ii,:)=interp1(line.phi(ii,1:npts(ii)),line.y(ii,1:npts(ii)),...
                        phi_int,'linear','extrap');
    if (max(diff(line.phi(ii,1:npts(ii))))>=0)
      doagain=true;
    end
  end
  
  % artificially fix first and last line
  net.x(:,1  ) = 0;
  net.x(:,end) = dx(1)*nx(1);
  net.y(1,:  ) = 0;
  net.y(end,:) = dx(2)*nx(2);
end