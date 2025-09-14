%% Exercise 3
clearvars; close all; clc

%% Excercise 3a
G=[1 -1;
   2 -1;
   1  1];
d=[-1; 0; 2.5];

m=inv(G'*G)*G'*d;

%x = A\b is computed differently
% than x = inv(A)*b and is recommended 
% for solving systems of linear equations.

m2=(G'*G)\(G'*d);

m1=0:2;

% %%%%%%%%
figure()
% %%%%%%%%%%%%%%
subplot(1,2,1)
% %%%%%%%%%%%%%%
plot(m1,  1+1*m1)
hold all
plot(m1,  0+2*m1)
plot(m1,2.5-1*m1)
plot(m(1),m(2),'x')
legend('Line 1', 'Line 2', 'Line 3', 'Solution')
title('Exercise 3a')
xlabel('m1')
ylabel('m2')

%% Exercise 3b
x=1:10; x=x';
y=[-0.5 -0.2 -0.1 0.9 0.6 1.2 2.3 2.1 2.8 3.2]-0.5; y=y';

[a,b,Gb]=linreg(x,y);

%%%%%%%%%%%%%%
subplot(1,2,2)
%%%%%%%%%%%%%%
plot(x,y,'*')
hold on;
plot(x,a+b*x)
title('Exercise 3b')
xlabel('x')
ylabel('y')

% calculate squared sum
sum_sq=sum(((a+b*x)-y).^2);

% calculate variance
epsilon=y-Gb*[a;b];
Qinv=inv(Gb'*Gb);
% collums of (Gb)
delta_m=zeros(size(Gb,2),1);

for i=1:size(Gb,2)
    delta_m(i)=1/(length(x)-size(Gb,2))*(epsilon'*epsilon)*Qinv(i,i);
end

%% Excercise 3c
%%%%%%%%%%%%%%%%%%%
% Solution Alicia %
%%%%%%%%%%%%%%%%%%%

% time series
% w=[1,-0.5,0,0,0,0,0,0,0,0];%,0,0,0,0,0,0,0,0,0];
% d=[1,0,0,0,0,0,0,0,0,0];%,0,0,0,0,0,0,0,0,0];
% 
% N=length(w);
% %%%%autocorrelation from matlab
% ww=xcorr(w);
% select the right branch
% psiw=ww(N:2*N-1);
% 
% wd=xcorr(w,d);
% psid=fliplr(wd(1:N));

% alternative
% wd=xcorr(d,w);
% psid=wd(N:2*N-1));


% Toep=toeplitz(psiw);
% f=inv(Toep)*psid';
% 
% d2=conv(w,f);
% d3=d2(1:N);
% 
% er=sum((d'-d3).^2);

%%%%%%%%%%%%%%%%%
% Solution Niko %

%%%%%%%%%%%%%%%%%

% w=[1,-0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]';
% d=[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
% 
% % operator length
% m=10;
% 
% % use built-in functions (not correct!)
% X=sqrt(20)*corrmtx(w,m-1);
% 
% y=xcorr(d,w);
% y=y(20:length(w)+m-1);
% 
% % filter coefficients
% f=X(1:m,:)\y';
% 
% % convolution
% d_f=conv(w,f);
% d_f=d_f(1:length(d));
% 
% d_fh=conv(w,[21/16,-21/128]);
% d_fh=d_fh(1:length(d));
% 
% % calculate error
% err_sq=sum((d_f-d').^2);
% err_sqh=sum((d_fh-d').^2);

%%%%%%%%%%%%%%%%%%
% Solution Laura %
%%%%%%%%%%%%%%%%%%
%seismic signal
w=zeros(100,1);
w(1)=1;
w(2)=-0.5;
%time shifted signal
d=zeros(100,1);
d(1)=1;

%%%auto correlation
for k=1:10
    for i=1:10
        phi(i)=w(i+(k-1))*w(i);
    end
    phik(k)=sum(phi);
end


% cross-correlation
for k=1:10
    for i=1:10
        phixd(i)=d(i+(k-1))*w(i);
    end
    phikxd(k)=sum(phixd);
end

AK=zeros(10,10);

for j=1:9
    AK(j,j)=phik(1);
    AK(j+1,j+1)=phik(1);
    AK(j+1,j)=phik(2);
    AK(j,j+1)=phik(2);
end



KK=phikxd;


%filter
f=inv(AK)*KK';

% plot(f)

ds=conv(w,f);
ds=ds(1:100);

% plot(x,d(1:10),x,ds(1:10))

% for i=1:10
%     LE(i)=(ds(i)-d(i))^2;
%     LEs=sum(LE);
% end

LE=sum((ds-d).^2);

%% %%%%%%%%%%%%%%%%%%%%%%%%%
function [a,b,G]=linreg(x,y)

% calculate G
G=[ones(length(x),1) x];

% set d
d=y;

% solve
m=inv(G'*G)*(G'*d);

% prepare output
a=m(1);
b=m(2);

end
