%% InvTomo Ex6 - SS2020
clearvars; close all; clc

m1=0:0.1:10;
m21=-2*cos(m1*pi/2)+6;
m22=-m1+11;

figure%('units','normalized','outerposition',[0.1 0.1 0.8 0.8])
% subplot(2,3,1)
plot(m1,m21)
hold on
plot(m1,m22)
title('Two functions')
xlabel('m1')
ylabel('m2')
legend('m21','m22')

%%
[m1range,m2range]=meshgrid(0:0.2:10,0:0.2:10);
Em=0.5*((2*cos(m1range*pi/2)+m2range-6).^2+(m1range+m2range-11).^2);

figure
% subplot(2,3,2)
surf(0:0.2:10,0:0.2:10,Em)
title('Misfit plot - 3D')
xlabel('m1')
ylabel('m2')
zlabel('E')

[m1range,m2range]=meshgrid(0:0.1:10,0:0.1:10);
Em=0.5*((2*cos(m1range*pi/2)+m2range-6).^2+(m1range+m2range-11).^2);

% subplot(2,3,3)
figure
imagesc(0:0.1:10,0:0.1:10,Em)
hold on
contour(0:0.1:10,0:0.1:10,Em,[1:5 6:2:10 15:5:50 60:10:70],'-k')
title('Misfit plot - 2D')
xlabel('m1')
ylabel('m2')
colorbar
set(gca,'YDir','normal')

%%%%%%%%%%%%%
stepsize=0.1;
nmax=100;
alpha=0.01;
%%%%%%%%%%%%

%%%%%%%%%
m1_0=4.5;
m2_0=3.0;
%%%%%%%%%

n=1;
next=1;
m=[m1_0;m2_0];
E=0.5*((2*cos(m(1,1)*pi/2)+m(2,1)-6).^2+(m(1,1)+m(2,1)-11).^2);

while next==1
    gradE=[-pi*sin(m(1,n)*pi/2)*(2*cos(m(1,n)*pi/2)+m(2,n)-6)+m(1,n)+m(2,n)-11 ; 2*cos(m(1,n)*pi/2)+2*m(2,n)+m(1,n)-17];
    dir=gradE/norm(gradE);
    m(:,n+1)=m(:,n)-dir*stepsize;
    E(1,n+1)=0.5*((2*cos(m(1,n+1)*pi/2)+m(2,n+1)-6).^2+(m(1,n+1)+m(2,n+1)-11).^2);
    if n >= nmax
        next=0;
    elseif E(n)==0
        next=0;
    elseif n>3
        deltaE=abs(E(n)-E(n-2))/E(n-2);
        if deltaE<alpha
            next=0;
        end
    end
    n=n+1;
end

subplot(2,3,4)
imagesc(0:0.1:10,0:0.1:10,Em)
hold on
contour(0:0.1:10,0:0.1:10,Em,[1:5 6:2:10 15:5:50 60:10:70],'-k')
plot(m(1,:),m(2,:),'-r')
title(['m_0=[',num2str(m1_0),',',num2str(m2_0),'], ',num2str(n),' iterations, E=',num2str(E(n))])
xlabel('m1')
ylabel('m2')
colorbar
set(gca,'YDir','normal')

% %%%%%%%%%
% m1_0=7.0;
% m2_0=1.0;
% %%%%%%%%%
% 
% n=1;
% next=1;
% m=[m1_0;m2_0];
% E=0.5*((2*cos(m(1,1)*pi/2)+m(2,1)-6).^2+(m(1,1)+m(2,1)-11).^2);
% 
% while next==1
%     gradE=[-pi*sin(m(1,n)*pi/2)*(2*cos(m(1,n)*pi/2)+m(2,n)-6)+m(1,n)+m(2,n)-11 ; 2*cos(m(1,n)*pi/2)+2*m(2,n)+m(1,n)-17];
%     dir=gradE/norm(gradE);
%     m(:,n+1)=m(:,n)-dir*stepsize;
%     E(1,n+1)=0.5*((2*cos(m(1,n+1)*pi/2)+m(2,n+1)-6).^2+(m(1,n+1)+m(2,n+1)-11).^2);
%     if n >= nmax
%         next=0;
%     elseif E(n)==0
%         next=0;
%     elseif n>3
%         deltaE=abs(E(n)-E(n-2))/E(n-2);
%         if deltaE<alpha
%             next=0;
%         end
%     end
%     n=n+1;
% end
% 
% subplot(2,3,5)
% imagesc(0:0.1:10,0:0.1:10,Em)
% hold on
% contour(0:0.1:10,0:0.1:10,Em,[1:5 6:2:10 15:5:50 60:10:70],'-k')
% plot(m(1,:),m(2,:),'-r')
% title(['m_0=[',num2str(m1_0),',',num2str(m2_0),'], ',num2str(n),' iterations, E=',num2str(E(n))])
% xlabel('m1')
% ylabel('m2')
% colorbar
% set(gca,'YDir','normal')
% 
% %%%%%%%%%
% m1_0=3.0;
% m2_0=5.0;
% %%%%%%%%%
% 
% n=1;
% next=1;
% m=[m1_0;m2_0];
% E=0.5*((2*cos(m(1,1)*pi/2)+m(2,1)-6).^2+(m(1,1)+m(2,1)-11).^2);
% 
% while next==1
%     gradE=[-pi*sin(m(1,n)*pi/2)*(2*cos(m(1,n)*pi/2)+m(2,n)-6)+m(1,n)+m(2,n)-11 ; 2*cos(m(1,n)*pi/2)+2*m(2,n)+m(1,n)-17];
%     dir=gradE/norm(gradE);
%     m(:,n+1)=m(:,n)-dir*stepsize;
%     E(1,n+1)=0.5*((2*cos(m(1,n+1)*pi/2)+m(2,n+1)-6).^2+(m(1,n+1)+m(2,n+1)-11).^2);
%     if n >= nmax
%         next=0;
%     elseif E(n)==0
%         next=0;
%     elseif n>3
%         deltaE=abs(E(n)-E(n-2))/E(n-2);
%         if deltaE<alpha
%             next=0;
%         end
%     end
%     n=n+1;
% end
% 
% subplot(2,3,6)
% imagesc(0:0.1:10,0:0.1:10,Em)
% hold on
% contour(0:0.1:10,0:0.1:10,Em,[1:5 6:2:10 15:5:50 60:10:70],'-k')
% plot(m(1,:),m(2,:),'-r')
% title(['m_0=[',num2str(m1_0),',',num2str(m2_0),'], ',num2str(n),' iterations, E=',num2str(E(n))])
% xlabel('m1')
% ylabel('m2')
% colorbar
% set(gca,'YDir','normal')
