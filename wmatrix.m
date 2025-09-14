function W=wmatrix(x,y,xt,yt,xr,yr)

% WMATRIX - Tomographix weighting matrix
% W = wmatrix(x,y,xt,yt,xr,yr)
% x,y .. grid lines
% (xt,yt),(xr,yr) .. Transmitter/Receiver Points

lx=length(x)-1;ly=length(y)-1;
ways=zeros(lx,ly);
nrays=min([length(xt) length(yt) length(xr) length(yr)]);
W=spalloc(nrays,prod(size(ways)),nrays*max(size(ways)));
for ray=1:nrays, % rays
    ways=ways*0; % reset local ways
    if yr(ray)==yt(ray), % horizontal
       iy=max(find(yr(ray)>y)):min(find(yr(ray)<y))-1;
       xle=min(xt(ray),xr(ray));xri=max(xt(ray),xr(ray));
       ixl=min(find(x>=xle));
       ixr=max(find(x<=xri));
       if (xle<x(ixl))&(ixl>1), ways(ixl-1,iy)=x(ixl)-xle; end
       if (xri>x(ixr))&(ixr<length(x)), ways(ixr,iy)=xri-x(ixr); end
       ways(ixl:ixr-1,iy)=repmat((x(ixl+1:ixr)-x(ixl:ixr-1))',1,length(iy))/length(iy);
    elseif xr(ray)==xt(ray), % vertical
       ix=max(find(xr(ray)>x)):min(find(xr(ray)<x))-1;
       yle=min(yt(ray),yr(ray));yri=max(yt(ray),yr(ray));
       iyl=min(find(y>=yle));
       iyr=max(find(y<=yri));
       if (yle<y(iyl))&(iyl>1), ways(ix,iyl-1)=y(iyl)-yle; end
       if (yri>y(iyr))&(iyr<length(y)), ways(ix,iyr)=yri-y(iyr); end
       ways(ix,iyl:iyr-1)=repmat((y(iyl+1:iyr)-y(iyl:iyr-1)),length(ix),1)/length(ix);
    else
        % section points
        [xs,ys,tx,ty]=xysect(x,y,xt(ray),yt(ray),xr(ray),yr(ray));
        %fx=find((tx>0)&(tx<1));fy=find((ty>0)&(ty<1));
        %xs=xs(fx);tx=tx(fx);ys=ys(fy);ty=ty(fy);
        if tx(end)>tx(1), %checking direction
            ix=min(find(tx>=0))-1;dix=1;
        else
            ix=max(find(tx>=0))+1;dix=-1;
        end
        if ty(end)>ty(1), % checking direction
            iy=min(find(ty>=0))-1;diy=1;
        else
            iy=max(find(ty>=0))+1;diy=-1;
        end
        %[ix dix iy diy]
        ox=xt(ray);oy=yt(ray);
        Way=[];
        while 1, % ray "tracing"
            if (dix==1)&(ix>ly), break; end
            if (diy==1)&(iy>lx), break; end
            if (dix==-1)&(ix==1), break; end
            if (diy==-1)&(iy==1), break; end
            if tx(ix+dix)<ty(iy+diy), %ray cuts y-line
                mm=1;
                ix=ix+dix;
                if(tx(ix)<0)|(tx(ix)>1), break; end
                nx=xs(ix);
                ny=y(ix);
            else % ray cuts x-line
                mm=-1;
                iy=iy+diy;
                if(ty(iy)<0)|(ty(iy)>1), break; end
                nx=x(iy);
                ny=ys(iy);
            end
            if (min(nx,ox)>=min(x))&(min(ny,oy)>=min(y))&...
                    (max(nx,ox)<=max(x))&(max(ny,oy)<=max(y)),
                way=sqrt((nx-ox)^2+(ny-oy)^2);
                if way>1e-10,
                    iix=ix-(mm*dix==1);
                    iiy=iy-(mm*diy==-1);
                    if(iix>0)&(iiy>0)&(iix<=ly)&(iiy<=lx),
                        ways(iiy,iix)=way; end 
                end
            end
            ox=nx;oy=ny;
        end % ray tracing
        nx=xr(ray);ny=yr(ray);
        %mm=1-mm;ix=ix+mm;iy=iy+1-mm;
        if (min(nx,ox)>=min(x))&(min(ny,oy)>=min(y))&...
                (max(nx,ox)<=max(x))&(max(ny,oy)<=max(y)),
            way=sqrt((nx-ox)^2+(ny-oy)^2);
            %iix=ix+(mm*dix==2);iiy=iy-(mm*diy==-2);
            %iix=ix;iiy=iy;
            iix=max(find(y<ny));iiy=max(find(x<nx));
            if isempty(iix), iix=0; end
            if isempty(iiy), iiy=0; end
            if(iix>0)&(iiy>0)&(iix<=ly)&(iiy<=lx),
                ways(iiy,iix)=way; end
        end
%         ww=ways;ww(end+1,end+1)=0;
%         pcolor(x,y,ww');colorbar,axis xy equal tight
%         xline=[xt(ray) xr(ray)];yline=[yt(ray) yr(ray)];
%         line(xline,yline);
%         pause(0.2);
    end
    ways=ways(1:lx,1:ly);
    W(ray,:)=ways(:)';
end % rays

%%% SUBFUCTION XYSECT
function [xs,ys,tx,ty]=xysect(x,y,xt,yt,xr,yr)
% XYSECT - X/Y Section points of ray - grid lines
% [xs,ys,tx,ty]=xysect(x,y,xt,yt,xr,yr)
% x,y .. Gridlines in x/y direction
% (xt,yt),(xr,yr) .. Transmittor/Receiver points
% xs,ys .. where ray cuts x/y grid lines
% tx,ty .. associated line parameters

xs=zeros(size(y));
ys=zeros(size(x));

warning off
xs=xt+(xr-xt)*(y-yt)/(yr-yt); % where ray cuts y_j
ys=yt+(yr-yt)*(x-xt)/(xr-xt); % where ray cuts x_i
tx=(y-yt)/(yr-yt); % associated line parameters
ty=(x-xt)/(xr-xt);  % associated line parameters
warning on

% if yr==yt,
%     tx=0;
% else 
%     tx=(y-yt)/(yr-yt); % associated line parameters
% end
% if xr==xt, 
%     ty=0; 
% else 
%     ty=(x-xt)/(xr-xt);  % associated line parameters
% end 

