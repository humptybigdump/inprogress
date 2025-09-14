function draw(x,y,ways,xt,yt,xr,yr,rays)

% MALMIT - Draw tomographic field with rays
% draw(x,y,field,xt,yt,xr,yr,rays)
% x,y .. Grid Lines
% field .. Field to draw (size(field)=(length(x)-1,length(y)-1)
% (xt,yt),(xr,yr) .. Transmitter/Receiver Points
% plot ray paths for rays (default=all, 0=none)

if nargin<3, error('At least three input arguments required!'); end
if nargin<8,
    rays=0; 
    if nargin>6, rays=1:length(yr); end
end

me=mean(ways(:));
if size(ways)~=[length(x)-1 length(y)-1],
    ways=reshape(ways,length(x)-1,length(y)-1);
end
ways(:,end+1)=me;
ways(end+1,:)=me;
pcolor(x,y,ways');
f=colorbar;
set(get(f,'ylabel'),'string','slowness (ms/m)');


axis xy equal tight
if nargin>6,
    hold on
    plot(xt,yt,'kx');
    plot(xr,yr,'ko');
    xx=[x(:);xr(:);xt(:)];yy=[y(:);yr(:);yt(:)];
    set(gca,'XLim',[min(xx) max(xx)],'YLim',[min(yy) max(yy)+0.0001]);
    if length(x)<=11, set(gca,'XTick',x); end
    if length(y)<=11, set(gca,'YTick',y); end
    grid on
    for l=1:length(rays),
        ray=rays(l);
        if ray>0,
            plot([xt(ray) xr(ray)],[yt(ray) yr(ray)],'k*-');
        end
    end
    hold off
end
xlabel('x (m)');
ylabel('y (m)');
