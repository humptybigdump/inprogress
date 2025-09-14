%% SS12 - Inversion und Tomographie
% Übung: Least-squares Inversion eines linearen Problems
%

clearvars; close all; clc

%%% build up the system
 G=[1 -1;2 -1;1 1];
 d=[-1 0 2.5];
%%% svd decomposition
 [U,S,V]=svd(G);
%%% build Up and Vp and Sp
 Sp=S(1:2,1:2); %abandon the last row and collun since singular equal to 0
 Up=U(:,1:2);
 Vp=V(:,1:2);
% 
 H=Vp*inv(Sp)*Up';
% 
 m=H*d';
 N=G*H; %Up*Up';
 R=H*G; %Vp*Vp';
% 
% disp('Modell-Auslösungsmatrix R')
% disp(R)

% 4a


%%% alternative


% G=[1 -1;2 -1;1 1];
% d=[-1; 0; 2.5];
%%% svd decomposition
%[U,S,V]=svd(G);
%%% original G
%G_test=U*S*V';

%%singular matrix inverse
%s=diag(1./S).*eye(2);

%s_new=zeros(2,3);
%s_new(1:2,1:2)=s;
%H=V*s_new*U';
%
%m=H*d;

%N=G*H; %Data resolution
%R=H*G; %Model resolution



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure('units','normalized','outerposition',[0.2 0.5 0.6 0.4])
subplot(1,2,1);
imagesc(N);
text(0,3.5,'a)','Fontweight','bold','Fontsize',20)
title('Data information matrix');
xlabel('data point')
ylabel('data point')
colorbar;
xticklabels({'','1','','2','','3',''})
yticklabels({'','1','','2','','3',''})
set(gca,'YDir','reverse')
caxis([0 1])
axis equal tight
subplot(1,2,2);
imagesc(R);
title('Model resolution matrix');
xlabel('model parameter')
ylabel('model parameter')
xticklabels({'','1','','2',''})
yticklabels({'','1','','2',''})
colorbar;
set(gca,'YDir','reverse')
axis equal tight

% 4a Solution of an over-determined problem using SVD
% Ga=[1 -1; 2 -1; 1 1];
% % 1. SVD
% [U,S,V]=svd(Ga);
% % 2.Generalized inverse
% Sz=zeros(2,3);
% Sz(1:2,1:2)=S(1:2,1:2);
% Sz(1,1)=1/Sz(1,1);
% Sz(2,2)=1/Sz(2,2);
% H=V*Sz*U';
% %3. solution
% d=[-2; -1; 2.5];
% m=H*d;
% %4. Resolution matrix for model and data space
% %data space
% N=U*U';
% %model space
% R=V*V';

%% Aufgabe 4b

A=[1 1 0; 0 0 1];
y=[1;1];
% 
[U,S,V]=svd(A);
% 
Sp=S(1:2,1:2);
Up=U(:,1:2);
Vp=V(:,1:2);
% 
H=Vp*inv(Sp)*Up';

x=H*y;

N=A*H; %Up*Up';
R=H*A; %Vp*Vp';
% 
% disp('Modell-Auslösungsmatrix R')
% disp(R)
% 
xs=A\y;
% 
% disp('Ergebnis mit A\y')
% disp(xs)

% 4b
%% alternative
%A=[1,1,0;0,0,1];
%y=[1;1];

%[Ua,Sa,Va]=svd(A);

%sa=diag(1./Sa).*eye(2);
%sa_new=zeros(3,2);
%sa_new(1:2,1:2)=sa;
%Ha=Va*sa_new*Ua';
%%ma=Ha*y;
%Na=A*Ha;
%Ra=Ha*A;

%%% alternative 
% 4b Solution of an under-determined problem by using SVD
% A=[1 1 0;0 0 1];
% y=[1;1];
% %1.SVD
% [Ub,Sb,Vb]=svd(A);
% % 2.Generalized inverse
% Szb=zeros(3,2);
% Szb(1:2,1:2)=Sb(1:2,1:2);
% Szb(1,1)=1/Szb(1,1);
% Szb(2,2)=1/Szb(2,2);
% Ag=Vb*Szb*Ub';
% %3. solution
% x=Ag*y;
% %4. Resolution matrix for model and data space
% %data space
% Nb=Ub*Ub';
% %model space
% Rb=Vb(:,1:2)*Vb(:,1:2)';


figure('units','normalized','outerposition',[0.2 0.1 0.6 0.4])
subplot(1,2,1);
imagesc(N);
text(0.16,2.5,'b)','Fontweight','bold','Fontsize',20)
title('Data information matrix');
xlabel('data point')
ylabel('data point')
xticklabels({'','1','','2',''})
yticklabels({'','1','','2',''})
colorbar;
set(gca,'YDir','reverse')
axis equal tight
subplot(1,2,2);
imagesc(R);
title('Model resolution matrix');
xlabel('model parameter')
ylabel('model parameter')
xticklabels({'','1','','2','','3',''})
yticklabels({'','1','','2','','3',''})
colorbar;
set(gca,'YDir','reverse')
axis equal tight


% %% %%%%%%%
% %Exercise 4d)
% %%%%%%%%
% %Load data 
% data=load('Data_Ex4c_1.mat');
% datan=data.dataEx4c_1;
% [Ud, Sd, Vd]=svd(datan);
% 
% % figure('units','normalized','outerposition',[0.2 0.5 0.6 0.4])
% % semilogy(diag(Sd),'-r')
% % hold on
% % title('Singular value spectrum')
% % ylabel('Singular value');
% % xlabel('Rank');
% % grid on
% 
% data2=load('Data_Ex4c_2.mat');
% datan2=data2.dataEx4c_2;
% [Ud2, Sd2, Vd2]=svd(datan2);
% % semilogy(diag(Sd2),'-g')
% 
% data3=load('Data_Ex4c_3.mat');
% datan3=data3.dataEx4c_3;
% [Ud3, Sd3, Vd3]=svd(datan3);
% % semilogy(diag(Sd3),'-b')
% % legend('R','G','B')
% % axis tight
% % ylim([1 10^5])
% % 
% % set(gcf,'Units','Inches');
% % pos = get(gcf,'Position');
% % set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% % print(gcf,'Exercise4c1.pdf','-dpdf','-r600','-fillpage')
% 
% % figure('units','normalized','outerposition',[0.1 0.1 0.8 0.8]);
% %plot grayscale pictures and calculate RMSE
% n=[1,10,20,50,100,200,256,1359];
% rms=zeros(1,length(n));
% for i=1:length(n)
% scut=Sd(1:n(i),1:n(i));
% Sdn=zeros(size(Sd));
% Sdn(1:n(i),1:n(i))=scut;
% Gd=Ud*Sdn*Vd';
% er2=(datan-Gd).^2; %calculate RMS
% rms(i)=sqrt(mean(er2(:)));
% 
% % subplot(2,4,i)
% % imagesc(Gd);
% % caxis=([0 256]);
% % colormap gray;
% % title('n = '+string(n(i))+', RMS = '+string(rms(i)));
% % 
% % axis equal tight
% end
% 
% % set(gcf,'Units','Inches');
% % pos = get(gcf,'Position');
% % set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% % print(gcf,'Exercise4c2.pdf','-dpdf','-r600','-fillpage')
% 
% % figure(); plot(n,rms,'.')
% % grid on
% % ylim([0 60])
% 
% %Take x values and do SVD for all three channels
% take=10;
% 
% scut=Sd(1:take,1:take);
% Sdn=zeros(size(Sd));
% Sdn(1:take,1:take)=scut;
% Gd=Ud*Sdn*Vd';
% Gd=uint8(Gd);
% 
% scut1=Sd3(1:take,1:take);
% Sdn1=zeros(size(Sd2));
% Sdn1(1:take,1:take)=scut1;
% Gd2=Ud2*Sdn1*Vd2';
% Gd2=uint8(Gd2);
% 
% scut2=Sd3(1:take,1:take);
% Sdn2=zeros(size(Sd3));
% Sdn2(1:take,1:take)=scut2;
% Gd3=Ud3*Sdn2*Vd3';
% Gd3=uint8(Gd3); %make integer values
% 
% RGB=cat(3,Gd, Gd2, Gd3); %put all channels together
% 
% figure('units','normalized','outerposition',[0.1 0.1 0.8 0.8]) %show color picture
% subplot(1,3,1)
% imshow(RGB);
% title('10 singular values')
% 
% take=50;
% 
% scut=Sd(1:take,1:take);
% Sdn=zeros(size(Sd));
% Sdn(1:take,1:take)=scut;
% Gd=Ud*Sdn*Vd';
% Gd=uint8(Gd);
% 
% scut1=Sd3(1:take,1:take);
% Sdn1=zeros(size(Sd2));
% Sdn1(1:take,1:take)=scut1;
% Gd2=Ud2*Sdn1*Vd2';
% Gd2=uint8(Gd2);
% 
% scut2=Sd3(1:take,1:take);
% Sdn2=zeros(size(Sd3));
% Sdn2(1:take,1:take)=scut2;
% Gd3=Ud3*Sdn2*Vd3';
% Gd3=uint8(Gd3); %make integer values
% 
% RGB=cat(3,Gd, Gd2, Gd3); %put all channels together
% 
% subplot(1,3,2)
% imshow(RGB);
% title('50 singular values')
% 
% take=200;
% 
% scut=Sd(1:take,1:take);
% Sdn=zeros(size(Sd));
% Sdn(1:take,1:take)=scut;
% Gd=Ud*Sdn*Vd';
% Gd=uint8(Gd);
% 
% scut1=Sd3(1:take,1:take);
% Sdn1=zeros(size(Sd2));
% Sdn1(1:take,1:take)=scut1;
% Gd2=Ud2*Sdn1*Vd2';
% Gd2=uint8(Gd2);
% 
% scut2=Sd3(1:take,1:take);
% Sdn2=zeros(size(Sd3));
% Sdn2(1:take,1:take)=scut2;
% Gd3=Ud3*Sdn2*Vd3';
% Gd3=uint8(Gd3); %make integer values
% 
% RGB=cat(3,Gd, Gd2, Gd3); %put all channels together
% 
% subplot(1,3,3)
% imshow(RGB);
% title('200 singular values')
% 
% % set(gcf,'Units','Inches');
% % pos = get(gcf,'Position');
% % set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% % print(gcf,'Exercise4c3.pdf','-dpdf','-r600','-fillpage')
