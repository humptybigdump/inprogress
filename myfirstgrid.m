close all
clear all
clc

initmsh

% Definition of nodes
nodes = [   0,    0;...
          500, -100;...
         1000,    0;...
         1000,  500;...
          500,  600;...
            0,  500;...
          700,  350];
% Definition of edges
edges = [1, 2;
         2, 3;
         3, 7;
         7, 4;
         4, 5;
         5, 6;
         6, 1;
         3, 4;
         4, 7;
         7, 3];
parts{1} = [1 2 3 4 5 6 7];
parts{2} = [8 9 10];
% Call mesh generator
hmin = 5;
hmax = 50;
range = 100;
xy_well = nodes(7,:);
opts.rho2=2;
[vert,etri,tria,tnum] = refine2(nodes,edges,parts,opts,...
                                @hfun,xy_well,hmin,hmax,range);
% plot the grid
subplot(2,1,1)
triplot(tria,vert(:,1),vert(:,2))
daspect([1 1 1])
hold on
plot(vert(7,1),vert(7,2),'ko')
hold off
% tricost(vert,etri,tria,tnum)

% smooth the grid
[vert,etri,tria,tnum] = smooth2(vert,etri,tria,tnum);
figure(1)
subplot(2,1,2)
triplot(tria,vert(:,1),vert(:,2))
daspect([1 1 1])
hold on
plot(vert(7,1),vert(7,2),'ko')
hold off
% tricost(vert,etri,tria,tnum)


function spacing = hfun(xy,xy_well,hmin,hmax,range)
% required grid spacing
% xy: coordinates of points
% xy_well: coordinates of the well
% hmin: minimum grid apcing
% hmax: maximum grid spacing
% range: range over which spacing increases

% determine distances to the well
d = sqrt((xy(:,1)-xy_well(1)).^2 + (xy(:,2)-xy_well(2)).^2);

spacing = hmin + (hmax-hmin)*d/range;
spacing(d>range)=hmax;

end


