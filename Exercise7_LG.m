%% InvTomo Ex8 - SS2022
clearvars; close all; clc

m1=0:0.1:10;
m21=-2*cos(m1*pi/2)+6;
m22=-m1+11;

figure
plot(m1,m21)
hold on
plot(m1,m22)
title('Two functions')
xlabel('m1')
ylabel('m2')
legend('m21','m22')

[m1range,m2range]=meshgrid(0:0.1:10,0:0.1:10);
Em=0.5*((2*cos(m1range*pi/2)+m2range-6).^2+(m1range+m2range-11).^2);

figure('units','normalized','outerposition',[0.2 0.2 0.6 0.4])
subplot(1,2,1)
imagesc(0:0.1:10,0:0.1:10,Em)
hold all
contour(0:0.1:10,0:0.1:10,Em,[1:5 6:2:10 15:5:50 60:10:70],'-k')
title('Misfit plot - 2D')
xlabel('m1')
ylabel('m2')
colorbar
set(gca,'YDir','normal')

for ii=1:4
%%%%%%%%%%%
Tmin=0.001;
T0=10;
%%number of maximum iterations
n_of_tries=1000;
alpha=0.95;
pertmax=0.6;

m1_0=3;%4.5;
m2_0=6;%3.0;

n=1;% model iterations (only updated)
l=1;% total iterations (with updated and non-updated)

E=zeros(n_of_tries,1);
m=zeros(2,n_of_tries);


%%initial model
m(:,1)=[m1_0;m2_0];
% initial temperature
T=T0;
% initial misfit
E(1)=0.5*( (2*cos(m(1,1)*pi/2) +m(2,1)-6)^2 + (m(1,1) + m(2,1) -11)^2 );

while T>Tmin && l<n_of_tries
    %perturb the model randomly
    mdist=[m(1,n)+pertmax*(rand(1)-0.5)*2;m(2,n)+pertmax*(rand(1)-0.5)*2];
    %calculte the misfit
    E_test=0.5*((2*cos(mdist(1)*pi/2)+mdist(2)-6)^2+(mdist(1)+mdist(2) -11)^2 );

    if E_test<E(n) % the new model is better than the old one, accept it
        E(n+1)=E_test;
        m(:,n+1)=mdist;
        n=n+1;
        %lower the temperature
        T=T*alpha;
    else            % the new model is worse than the old one.
        % Boltzman probablity 
        r=rand(1);
        P=exp((E(n)-E_test)/(1.*T));
        if P>r  % if the boltzman probability is higher than the random number
            E(n+1)=E_test;
            m(:,n+1)=mdist;
            n=n+1;
            T=T*alpha;
        end
    end
    l=l+1;
end
mend=m(:,n);% final model
m=m(:,1:n); % 
E=E(1:n);

subplot(1,2,1)
plot(m(1,:),m(2,:),'-')
plot(m(1,n),m(2,n),'k*')
title(['m_0=[',num2str(m1_0),',',num2str(m2_0),'], T0=',num2str(T0),', alpha=',num2str(alpha)])
xlabel('m1')
ylabel('m2')
colorbar
set(gca,'YDir','normal')

subplot(1,2,2)
hold all
plot(0:n-1,E)
text(350,20-ii*2.5,['Run ',num2str(ii),': ',num2str(n),' iterations, E=',num2str(E(n))])
grid on
box on
legend('Run 1','Run 2','Run 3','Run 4')
xlabel('Iteration')
ylabel('Misfit')
title('Misfit evolution')
end

% set(gcf,'Units','Inches');
% pos = get(gcf,'Position');
% set(gcf,'PaperPositionMode','Auto','PaperUnits','Inches','PaperSize',[pos(3), pos(4)])
% print(gcf,['Exercise7a_T0_',num2str(T0),'_alpha_',num2str(alpha)],'-dpdf','-r600','-fillpage')
