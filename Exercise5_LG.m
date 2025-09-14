%% InvTomo Ex5 - SS2020
clearvars; close all; clc

x=0:0.1:1;
y=0:0.1:1;

s=ones(10);
sa=s;
sa(2:4,3:5)=2;

load('hv130.mat')

figure('units','normalized','outerposition',[0.1 0.3 0.8 0.6])
subplot(2,4,1)
draw(x,y,sa,xt,yt,xr,yr,0)
title('Without rays')
subplot(2,4,1)
draw(x,y,sa,xt,yt,xr,yr)
title('With rays')


%%% determin the ray path for all pairs
W=wmatrix(x,y,xt,yt,xr,yr); %% compressed 
Wf=full(W);

n=5;
%single ray
w=W(n,:);
%sum all rays
wsum=sum(Wf);

subplot(2,4,2)
draw(x,y,w,xt,yt,xr,yr,n)
title('Ray 5')
axis square
% 
subplot(2,4,3)
draw(x,y,wsum,xt,yt,xr,yr)
title('Full ray coverage')
axis square

r=60;

[U,S,V]=svds(W,100);
[Up,Sp,Vp]=svds(W,r);

N=Up*Up';
R=Vp*Vp';

%sp=subplot(1,2,1);
%sp.Position = sp.Position + [0.022 0.022 -0.04 -0.04];
subplot(2,4,5)
semilogy(diag(S),'-o')
hold on
plot([r r],[min(diag(S)) max(diag(S))],'-r')
%plot([1 100],[0.01 0.01],'-r')
%plot([1 100],[0.001 0.001],'-r')
title('Singular value spectrum')
grid on
axis tight square

subplot(2,4,6)
imagesc(N)
title(['Data resolution matrix, r=',num2str(r)])
axis square
caxis([0 r/100])
% 
subplot(2,4,7)
imagesc(R)
title(['Model resolution matrix, r=',num2str(r)])
axis square
caxis([0 r/100])


%forward simulation
t=W*s(:);
ta=W*sa(:);


%%%pseud inverse
H=Vp*inv(Sp)*Up';
sa_inv=H*ta;

td=zeros(130,1);
for ii=1:130
    if t(ii,1)~=ta(ii,1)
        td(ii,1)=1;
    end
end
ray=find(td);

% % subplot(2,4,3)
% % draw(x,y,sa,xt,yt,xr,yr,0)
% % title('Model with anomaly')
% 
subplot(2,4,4)
draw(x,y,sa,xt,yt,xr,yr,ray)
title('Rays covering anomaly')

%subplot(1,2,2)
subplot(2,4,8)
draw(x,y,sa_inv,xt,yt,xr,yr,0)
title(['Inverted model r=',num2str(r)])
