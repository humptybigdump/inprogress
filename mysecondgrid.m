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
          700,  350;... % well (node 7)
            0,  250;... % mid point at inlet face
         1000,  250];   % mid point at outlet face
% Definition of edges
edges = [1, 2;
         2, 3;
         3, 9;
         9, 8;
         8, 1;
         9, 4;
         4, 5;
         5, 6;
         6, 8];
parts{1} = [1 2 3 4 5];
parts{2} = [6 7 8 9 4];
% node number of the well
wellnode = 7;
% Call mesh generator
hmin = 1;
hmax = 10;
range = 100;
xy_well = nodes(wellnode,:);
opts.rho2=1;
[vert,etri,tria,tnum] = refine2(nodes,edges,parts,opts,...
                                @hfun,xy_well,hmin,hmax,range);
% vert (nnod x 2): coordinates of all nodes
% etri (nedge x 2): list of edges belonging to boundaries
% tria (nelem x 3): list of triangles
% tnum (nelem x 1): which element belongs to which part
subplot(2,1,1)
triplot(tria,vert(:,1),vert(:,2))
daspect([1 1 1])
% find an edge that involves the well node
% a) find all elements involving the well node
well_elem = tria(ismember(tria(:,1),wellnode)|ismember(tria(:,2),wellnode)|ismember(tria(:,3),wellnode),:);
% b) pick the first and find the first vertex that is not the well node
well_neigh=well_elem(1,find(well_elem(1,:)~=wellnode,1));
% c) add the corresponding edge to etri to preserve both vertices
etri=[etri;wellnode well_neigh];
% now smooth the grid
[vert,etri,tria,tnum] = smooth2(vert,etri,tria,tnum);
% take extra edge out
etri = etri(1:end-1,:);

% identify vertices at the intersection of part 1 and part 2
boundvert=intersect(unique(tria(tnum==1,:)),unique(tria(tnum==2,:)));

% find the edges at the intersection
select = ismember(etri(:,1),boundvert) & ismember(etri(:,2),boundvert);
edge_inter = etri(select,:);

% store the grid
save mygreatgrid.mat vert etri tria tnum wellnode edge_inter

% plot the grid
subplot(2,1,2)
triplot(tria,vert(:,1),vert(:,2))
daspect([1 1 1])
hold on
plot(vert(7,1),vert(7,2),'ko')
% plot vertices at the intersection
plot(vert(boundvert,1),vert(boundvert,2),'pr')
% plot vertices at the original edges
% plot(vert(unique(etri),1),vert(unique(etri),2),'*g')
for ii=1:size(edge_inter,1)
    text(0.5*(vert(edge_inter(ii,1),1)+vert(edge_inter(ii,2),1)), ...
         0.5*(vert(edge_inter(ii,1),2)+vert(edge_inter(ii,2),2)),num2str(ii),...
         'HorizontalAlignment','center','VerticalAlignment','middle')
end
hold off


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


