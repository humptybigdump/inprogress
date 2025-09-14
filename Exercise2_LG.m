%% Exercise 2 - InvTomo - Radon Transform
clearvars; close all; clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%% job 1
NX=101;
NY=101;
vp=200*ones(NY,NX);
vp(25:50,30:70)=300;
vp(51:80,30:50)=400;
vp(51:80,51:70)=500;
% vp(51:100,:)=500;
% vp(:,51:100)=500;
%%%%%%%%%%%%

xorig=-50:50;
yorig=-50:50;

figure('units','normalized','outerposition',[0.2 0.2 0.6 0.6])
subplot(2,2,1)
imagesc(xorig,yorig,vp)
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
caxis([100 600])
axis equal tight



%%%%%%%%%%%%%%%%% job2
theta=1:180;
%%%diagonal 
diag=ceil(sqrt(101^2+101^2));
A=zeros(diag,diag);
A(22:122,22:122)=vp;

%fulfilling the diag size!
xorig=-71:71; % (143-1)/2
yorig=-71:71;
% xorig=1:143;
% yorig=1:143;

%%% mesh the new coordinates
[Xo,Yo] = meshgrid(xorig,yorig);

sino=zeros(diag,length(theta));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% the first way
%%%%%% loop the theta % anti-clockwise rotate for all points
%%%%%% of the model equivalent to clockwise rotate the coordinates
for ii=1:length(theta)
    %%%% rotate (actually new position of model grids)
     X=cosd(theta(ii))*Xo - sind(theta(ii))*Yo;
     Y=sind(theta(ii))*Xo + cosd(theta(ii))*Yo;
     vpint=interp2(Xo,Yo,A,X,Y);
     vpint(isnan(vpint)) = 0;
     sino(:,ii)=sum(vpint);
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% the second way
sino2=zeros(diag,length(theta));
for ii=1:length(theta)
      vpint=imrotate(A,theta(ii),'bilinear','crop');
      sino2(:,ii)=sum(vpint);
end

%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%now display the original figure
subplot(2,2,1)
imagesc(xorig,yorig,A)
title('Original Figure')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
caxis([100 600])

%%%%%%%%%%%now display the rotated figure
subplot(2,2,2)
imagesc(xorig,yorig,vpint)
title('Rotate 180 ')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
caxis([100 600])


subplot(2,2,3)
%%rotates array A counterclockwise 
% by k*90 degrees, where k is an 
% integer.
imagesc(rot90(sino,2))
title('Own solution')
xlabel('Angle in degree')
ylabel('Receiver number')
colorbar


Rvp=radon(vp);

subplot(2,2,4)
imagesc(Rvp)
title('MATLAB solution')
xlabel('Angle in degree')
ylabel('Receiver number')
colorbar


%%%% difference
subplot(2,2,4)
% imagesc(Rvp_alt)
imagesc(rot90(sino,2)-Rvp(2:end-1,:))
title('Difference to MATLAB solution')
xlabel('Angle in degree')
ylabel('Receiver number')
caxis([-10 10])
colorbar

subplot(2,2,2)
imagesc(rot90(sino,2))
title('Own solution')
xlabel('Angle in degree')
ylabel('Receiver number')
colorbar

% set(gcf,'Units','Inches');
% pos = get(gcf,'Position');
% set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% print(gcf,'Exercise2a','-dpdf','-r600','-bestfit')
%%



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure('units','normalized','outerposition',[0.2 0.2 0.6 0.6])
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

xorig=-51.5:51.5;
yorig=-51.5:51.5;

%%%%%%%%%%%%
angmin=1;
angincr=1;
angplus=180;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);
%%%size of Rvplim is 145,180
Rvplim_plot=zeros(145,180);
Rvplim_plot(:,1:angplus)=Rvplim;

subplot(2,4,1)
imagesc(Rvplim_plot)
title('Sinogram up to 180°')
xlabel('Angle in degree')
ylabel('Receiver number')
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus);%,'linear','none');

subplot(2,4,5)
imagesc(xorig,yorig,vpinv)
title('1:1:180')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

%%%%%%%%%%%%
angmin=1;
angincr=1;
angplus=135;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);
Rvplim_plot=zeros(145,180);
Rvplim_plot(:,1:angplus)=Rvplim;

subplot(2,4,2)
imagesc(Rvplim_plot)
title('Sinogram up to 135°')
xlabel('Angle in degree')
ylabel('Receiver number')
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus);%,'linear','none');

subplot(2,4,6)
imagesc(xorig,yorig,vpinv)
title('1:1:135')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

%%%%%%%%%%%%
angmin=1;
angincr=1;
angplus=90;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);
Rvplim_plot=zeros(145,180);
Rvplim_plot(:,1:angplus)=Rvplim;

subplot(2,4,3)
imagesc(Rvplim_plot)
title('Sinogram up to 90°')
xlabel('Angle in degree')
ylabel('Receiver number')
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus);%,'linear','none');

subplot(2,4,7)
imagesc(xorig,yorig,vpinv)
title('1:1:90')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

%%%%%%%%%%%%
angmin=1;
angincr=1;
angplus=45;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);
Rvplim_plot=zeros(145,180);
Rvplim_plot(:,1:angplus)=Rvplim;

subplot(2,4,4)
imagesc(Rvplim_plot)
title('Sinogram up to 45°')
xlabel('Angle in degree')
ylabel('Receiver number')
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus);%,'linear','none');

subplot(2,4,8)
imagesc(xorig,yorig,vpinv)
title('1:1:45')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

% set(gcf,'Units','Inches');
% pos = get(gcf,'Position');
% set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% print(gcf,'Exercise2b','-dpdf','-r600','-bestfit')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure('units','normalized','outerposition',[0.2 0.2 0.6 0.6])
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%
angmin=1;
angincr=1;
angplus=180;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);

subplot(2,4,1)
imagesc(angmin:angincr:angplus,1:145,Rvplim)
title('Sinogram in 1° steps')
xlabel('Angle in degree')
ylabel('Receiver number')
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus);%,'linear','none');

subplot(2,4,5)
imagesc(xorig,yorig,vpinv)
title('1:1:180')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

%%%%%%%%%%%%
angmin=1;
angincr=2;
angplus=180;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);

subplot(2,4,2)
imagesc(angmin:angincr:angplus,1:145,Rvplim)
title('Sinogram in 2° steps')
xlabel('Angle in degree')
ylabel('Receiver number')
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus);%,'linear','none');

subplot(2,4,6)
imagesc(xorig,yorig,vpinv)
title('1:2:180')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

%%%%%%%%%%%%
angmin=1;
angincr=5;
angplus=180;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);

subplot(2,4,3)
imagesc(angmin:angincr:angplus,1:145,Rvplim)
title('Sinogram in 5° steps')
xlabel('Angle in degree')
ylabel('Receiver number')
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus);%,'linear','none');

subplot(2,4,7)
imagesc(xorig,yorig,vpinv)
title('1:5:180')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

%%%%%%%%%%%%
angmin=1;
angincr=10;
angplus=180;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);

subplot(2,4,4)
imagesc(angmin:angincr:angplus,1:145,Rvplim)
title('Sinogram in 10° steps')
xlabel('Angle in degree')
ylabel('Receiver number')
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus);%,'linear','none');

subplot(2,4,8)
imagesc(xorig,yorig,vpinv)
title('1:10:180')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar

caxis([100 600])
axis equal tight

% set(gcf,'Units','Inches');
% pos = get(gcf,'Position');
% set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% print(gcf,'Exercise2c','-dpdf','-r600','-bestfit')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure('units','normalized','outerposition',[0 0.2 1.0 0.6])
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%
angmin=1;
angincr=1;
angplus=180;
%%%%%%%%%%%%

Rvplim=radon(vp,angmin:angincr:angplus);
vpinv=iradon(Rvplim,angmin:angincr:angplus,'linear');%,'linear','none');

subplot(2,5,1)
imagesc(xorig,yorig,vpinv)
title('Filtered backprojection')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

vpinv=iradon(Rvplim,angmin:angincr:angplus,'linear','none')/101;

subplot(2,5,2)
imagesc(xorig,yorig,vpinv)
title('Unfiltered backprojection')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

%%%%%%%%%%%%%%%%%%%
r45 = Rvplim(:,45);
vpinv = iradon([r45 r45], [45 45],'linear','none')/202;

subplot(2,5,3)
imagesc(xorig,yorig,vpinv)
title('Unfiltered backprojection at 45°')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

subplot(2,5,[6 7])
plot(vpinv(51,:))
hold all

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
vpinv = iradon([r45 r45], [45 45])/2;

subplot(2,5,4)
imagesc(xorig,yorig,vpinv)
title('Filtered backprojection at 45°, Ram-Lak filter')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

subplot(2,5,[6 7])
plot(vpinv(51,:))

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
vpinv = iradon([r45 r45], [45 45],'linear','Shepp-Logan')/2;

subplot(2,5,5)
imagesc(xorig,yorig,vpinv)
title('Shepp-Logan filter')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

subplot(2,5,[6 7])
plot(vpinv(51,:))

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
vpinv = iradon([r45 r45], [45 45],'linear','Cosine')/2;

subplot(2,5,8)
imagesc(xorig,yorig,vpinv)
title('Cosine filter')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

subplot(2,5,[6 7])
plot(vpinv(51,:))
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
vpinv = iradon([r45 r45], [45 45],'linear','Hamming')/2;

%'Ram-Lak' (default) | 'Shepp-Logan' | 'Cosine' | 'Hamming' | 'Hann' | 'None'

subplot(2,5,9)
imagesc(xorig,yorig,vpinv)
title('Hamming filter')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

subplot(2,5,[6 7])
plot(vpinv(51,:))

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
vpinv = iradon([r45 r45], [45 45],'linear','Hann')/2;

subplot(2,5,10)
imagesc(xorig,yorig,vpinv)
title('Hann filter')
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
colorbar
caxis([100 600])
axis equal tight

subplot(2,5,[6 7])
plot(vpinv(51,:))
xlim([1 102])
title('Comparison of filters')
legend('None','Ram-Lak','Shepp-Logan','Cosine','Hamming','Hann')

% set(gcf,'Units','Inches');
% pos = get(gcf,'Position');
% set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% print(gcf,'Exercise2d','-dpdf','-r600','-bestfit')
%
% https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0405/HAYDEN/Slice_Reconstruction.html