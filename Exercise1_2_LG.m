%%
clearvars; 
close all; 
clc

layer6dat=load("layer6.dat")
%%%load the coordinates
x_coord = layer6dat(:,1);
y_coord = layer6dat(:,2);
%%%load the velocity value
data = layer6dat(:,3);
%%% intensify the nodes for plotting
x = min(x_coord):5:max(x_coord);% 5 km in step-length
y = min(y_coord):10:max(y_coord); % 10 km in step-length
%%% meshgrid x y 
%%% size (size(y),size(x))
[X,Y] = meshgrid(x,y); %X and Y have the same size

interpolated = griddata(x_coord,y_coord,data,X,Y,'linear');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%figure('units','normalized','outerposition',[0 0 1 1])
%subplot(1,2,1)
%plot(X,Y,'.r')
%hold on
%plot(x_coord,y_coord,'*k')
%title('Data points and grid')
%xlabel('x in km')
%ylabel('y in km')
%axis equal tight
%hold off

%figure('units','normalized','outerposition',[0 0 1 2])
%subplot(1,2,2)
%imagesc(x,y,interpolated)
%set(gca,"YDir","normal")
%hold on
%title('Linearly interpolated matrix with original data points')
%plot(x_coord,y_coord,'*k')
%c=colorbar;
%cl=get(c,'ylabel');
%set(cl,'String','\Delta v_S (km/s)')
%caxis([-2 2])
%xlabel('x in km')
%ylabel('y in km')
%axis equal tight
%hold off

%pause
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%https://ch.mathworks.com/help/matlab/ref/griddata.html
%https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation
interpolated_nearest = griddata(x_coord,y_coord,data,X,Y,'nearest');
interpolated_natural = griddata(x_coord,y_coord,data,X,Y,'natural');
interpolated_cubic = griddata(x_coord,y_coord,data,X,Y,'cubic');
interpolated_v4 = griddata(x_coord,y_coord,data,X,Y,'v4');

%%%original
figure('units','normalized','outerposition',[0 0 1 1])
subplot(2,4,1)
%plot grid points
plot(X,Y,'.r')
hold on
%plot original points
plot(x_coord,y_coord,'*k')
title('Data points and grid')
xlabel('x in km')
ylabel('y in km')
axis equal tight


%%%linear interpolation
subplot(2,4,2)
imagesc(x,y,interpolated)
hold on
plot(x_coord,y_coord,'*k')
set(gca,'YDir','normal')
title('Linear interpolation')
xlabel('x in km')
ylabel('y in km')
axis equal tight
c=colorbar;
cl=get(c,'xlabel');
set(cl,'String','\Delta v_S (km/s)')
caxis([-2 2])

%plot y= 20 km
subplot(2,4,[3 4])
%plot certain row 
% find the nearst grid point for a certain depth
[~,ans] = (min(abs(y - 20)))
disp(ans)
plot(x,interpolated(ans,:),'-','Linewidth',2)
hold all
plot(x,interpolated_nearest(ans,:),'-','Linewidth',2)
plot(x,interpolated_natural(ans,:),'-','Linewidth',2)
plot(x,interpolated_cubic(ans,:),'-','Linewidth',2)
plot(x,interpolated_v4(ans,:),'-','Linewidth',2)
grid on
axis tight
legend('Linear','Nearest','Natural','Cubic','V4','Location','SouthEast')

%find points near the 20 km
index_near=find(abs(y_coord-20)<50);
x_new=x_coord(index_near)
data_new=data(index_near)
plot(x_new,data(index_near),'*k')
title('Comparison of interpolation methods at y=20km')
xlabel('x in km')
ylabel('Interpolated \Delta v_S')


%nearest
subplot(2,4,5)
imagesc(x,y,interpolated_nearest)
hold on
plot(x_coord,y_coord,'*k')
set(gca,'YDir','normal')
title('Nearest interpolation')
xlabel('x in km')
ylabel('y in km')
axis equal tight
c=colorbar;
cl=get(c,'xlabel');
set(cl,'String','\Delta v_S (km/s)')
caxis([-2 2])

%natural
subplot(2,4,6)
imagesc(x,y,interpolated_natural)
hold on
plot(x_coord,y_coord,'*k')
set(gca,'YDir','normal')
title('Natural interpolation')
xlabel('x in km')
ylabel('y in km')
axis equal tight
c=colorbar;
cl=get(c,'xlabel');
set(cl,'String','\Delta v_S (km/s)')
caxis([-2 2])

%cubic
subplot(2,4,7)
imagesc(x,y,interpolated_cubic)
hold on
plot(x_coord,y_coord,'*k')
set(gca,'YDir','normal')
title('Cubic interpolation')
xlabel('x in km')
ylabel('y in km')
axis equal tight
c=colorbar;
cl=get(c,'xlabel');
set(cl,'String','\Delta v_S (km/s)')
caxis([-2 2])

%V4
subplot(2,4,8)
imagesc(x,y,interpolated_v4)
hold on
plot(x_coord,y_coord,'*k')
set(gca,'YDir','normal')
title('V4 interpolation')
xlabel('x in km')
ylabel('y in km')
axis equal tight
c=colorbar;%('horizontal');
cl=get(c,'xlabel');
set(cl,'String','\Delta v_S (km/s)')
caxis([-2 2])
%print(fig,'MySavedPlot','-dpdf')
set(gcf,'Units','Inches');
pos = get(gcf,'Position');
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
print(gcf,'Exercise1_Add2','-dpdf','-r600','-bestfit')
