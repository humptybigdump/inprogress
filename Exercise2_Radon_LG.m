%% Exercise 2 - InvTomo - Radon Transform
clearvars; close all; clc

%%%%%%%%%%%%
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

theta=1:180;
Rvp=radon(vp);
% Rvp_alt=radon_alt(vp,theta);

diag=ceil(sqrt(101^2+101^2));
A=zeros(diag,diag);
A(22:122,22:122)=vp;

xorig=-71:71;
yorig=-71:71;

% [Xo,Yo] = meshgrid(xorig,yorig);

sino=zeros(diag,length(theta));

for ii=1:length(theta)
    vpint=imrotate(A,theta(ii),'bilinear','crop');
    sino(:,ii)=sum(vpint);
end

subplot(2,2,1)
imagesc(vpint)
xlabel('x in grid points')
ylabel('y in grid points')
c = colorbar;
c.Label.String = 'v_p in m/s';
caxis([100 600])

subplot(2,2,3)
imagesc(Rvp)
title('MATLAB solution')
xlabel('Angle in degree')
ylabel('Receiver number')
colorbar

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
