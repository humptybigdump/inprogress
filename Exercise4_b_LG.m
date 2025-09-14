clearvars; close all; clc
% %% %%%%%%%
% %Exercise 4d)
% %%%%%%%%
% %Load data 
data=load('Data_Ex4c_1.mat');
 %%% structure of the data, please output the datan, it would explode your 
 %%matlab
datan=data.dataEx4c_1;
[Ud, Sd, Vd]=svd(datan);
% 
figure('units','normalized','outerposition',[0.2 0.5 0.6 0.4])
%semilogy(X,Y) plots x- and y-coordinates using a linear scale on 
% the x-axis and a base-10 logarithmic scale on the y-axis.
semilogy(diag(Sd),'-r')
hold on
title('Singular value spectrum')
ylabel('Singular value');
xlabel('Rank');
grid on
% 
data2=load('Data_Ex4c_2.mat');
datan2=data2.dataEx4c_2;
[Ud2, Sd2, Vd2]=svd(datan2);
semilogy(diag(Sd2),'-g')
% 
data3=load('Data_Ex4c_3.mat');
datan3=data3.dataEx4c_3;
[Ud3, Sd3, Vd3]=svd(datan3);
semilogy(diag(Sd3),'-b')
legend('R','G','B')
axis tight
ylim([1 10^5])
% % 


set(gcf,'Units','Inches');
pos = get(gcf,'Position');
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
print(gcf,'Exercise4c1.pdf','-dpdf','-r600','-fillpage')


% 
figure('units','normalized','outerposition',[0.1 0.1 0.8 0.8]);

%plot grayscale pictures and calculate RMSE
n=[1,10,20,50,100,200,256,1359];

rms=zeros(1,length(n));
for i=1:length(n)
 scut=Sd(1:n(i),1:n(i));
 Sdn=zeros(size(Sd));
 Sdn(1:n(i),1:n(i))=scut;
 Gd=Ud*Sdn*Vd';
 er2=(datan-Gd).^2; %calculate RMS
 rms(i)=sqrt(mean(er2(:)));
% 
 subplot(2,4,i)
 imagesc(Gd);
 caxis=([0 256]);
 colormap gray;
 title('n = '+string(n(i))+', RMS = '+string(rms(i)));
end
% 
set(gcf,'Units','Inches');
pos = get(gcf,'Position');
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
%print(gcf,'Exercise4c2.pdf','-dpdf','-r600','-fillpage')
% 
figure(); 
plot(n,rms,'.')
grid on
ylim([0 60])




%%%%%%%
%Take x values and do SVD for all three channels
take=10;
% 
scut=Sd(1:take,1:take);
Sdn=zeros(size(Sd));
Sdn(1:take,1:take)=scut;
Gd=Ud*Sdn*Vd';
Gd=uint8(Gd);
% 
scut2=Sd2(1:take,1:take);
Sdn2=zeros(size(Sd2));
Sdn2(1:take,1:take)=scut2;
Gd2=Ud2*Sdn2*Vd2';
Gd2=uint8(Gd2);
% 
scut3=Sd3(1:take,1:take);
Sdn3=zeros(size(Sd3));
Sdn3(1:take,1:take)=scut3;
Gd3=Ud3*Sdn3*Vd3';
Gd3=uint8(Gd3); %make integer values
%  
RGB=cat(3,Gd, Gd2, Gd3); %put all channels together
% 
figure('units','normalized','outerposition',[0.1 0.1 0.8 0.8]) %show color picture
subplot(1,3,1)
imshow(RGB);
title('10 singular values')
% 
take=50;
% 
scut=Sd(1:take,1:take);
Sdn=zeros(size(Sd));
Sdn(1:take,1:take)=scut;
Gd=Ud*Sdn*Vd';
Gd=uint8(Gd);
% 
scut2=Sd2(1:take,1:take);
Sdn2=zeros(size(Sd2));
Sdn2(1:take,1:take)=scut2;
Gd2=Ud2*Sdn2*Vd2';
Gd2=uint8(Gd2);
% 
scut3=Sd3(1:take,1:take);
Sdn3=zeros(size(Sd3));
Sdn3(1:take,1:take)=scut3;
Gd3=Ud3*Sdn3*Vd3';
Gd3=uint8(Gd3); %make integer values
% 
RGB=cat(3,Gd, Gd2, Gd3); %put all channels together
% 
subplot(1,3,2)
imshow(RGB);
title('50 singular values')
% 
take=200;
% 
scut=Sd(1:take,1:take);
Sdn=zeros(size(Sd));
Sdn(1:take,1:take)=scut;
Gd=Ud*Sdn*Vd';
Gd=uint8(Gd);
% 
scut2=Sd2(1:take,1:take);
Sdn2=zeros(size(Sd2));
Sdn2(1:take,1:take)=scut2;
Gd2=Ud2*Sdn2*Vd2';
Gd2=uint8(Gd2);
% 
scut3=Sd3(1:take,1:take);
Sdn3=zeros(size(Sd3));
Sdn3(1:take,1:take)=scut3;
Gd3=Ud3*Sdn3*Vd3';
Gd3=uint8(Gd3); %make integer values
% 
RGB=cat(3,Gd, Gd2, Gd3); %put all channels together
% 
subplot(1,3,3)
imshow(RGB);
title('200 singular values')
% 
set(gcf,'Units','Inches');
pos = get(gcf,'Position');
set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% % print(gcf,'Exercise4c3.pdf','-dpdf','-r600','-fillpage')
