%PARAMETER
%E = 210e9;  I0 = 1/12*0.05*(0.04)^3;   mu0= 7850*(0.05*0.04);   l = 1.0; 

disp('---------------------------------------------------------------------------------- ')
disp('                         BEIDSEITIG GELAGERTER BALKEN ')
disp('                                             ')
disp('                     o===================================o ')
disp('                    / \                                 / \ ')
disp('---------------------------------------------------------------------------------- ')

%-------------------------------------------------------------------------
N = 2;      %N=0,1,2,3,4 means 1.,2.,3.,4.,5. shape functions
%-------------------------------------------------------------------------
%ANFANGSBEDINGUNG FÜR rho UND d(rho)/dt
switch N
    case 0
        y0 = [1 0]';
    case 1
        y0 = [1 0 5e-5 0]';
    case 2
        y0 = [1 0 5e-5 0  0 0]';
%	case 3
%        y0 = [0.001 0 5e-5 0  0 0  0 0]';
%    case 4
%        y0 = [0.001 0 5e-5 0  0 0  0 0  0 0]';
end

%ODE-BERECHNUNG
t_span = [0 0.01];
  disp(['Anzahl der Eigenformen: ' num2str(length(y0)/2)])
  disp('Berechnung läuft erfolgreich, bitte warten Sie einen Augenblick ...')
sol = ode45(@Ritz_ausMAPLE_Beidseitig,t_span,y0,[],E,I0,mu0,l,N);
  disp('Berechnung beendet. Sie können Ihre ausgewerteten Evaluierungsergebnisse.')

%BERECHNUNG UND PLOT DER LÖSUNG
x = 0:l/20:l;
T = t_span(1):0.5e-4:t_span(2);
rho = deval(sol,T)'; % Evaluierung der Lösung.

%EIGENFORM U_k
U = zeros(N+1,length(x));
for k=0:N
    U(k+1,:)= sin(pi/l*((k+1))*x);
end
plot(x,U,'LineWidth',4), 
axis([0 1 -1.5*l 1.5*l]); set(gca,'FontSize',16);
xlabel('Lage x'), title('Eigenschwingungsformen')
legend('1.Eigenform','2.Eigenform','3.Eigenform')

%ANFANGSBEDINGUNG u(x,t=0)
u0 = zeros(1,length(x));
for k=0:N
    u0 = u0 + y0(1+k)*U(k+1,:);
end
%subplot(2,1,2), plot(x,u0,'LineWidth',4), title('Initial displacment')
%set(gca,'FontSize',14);
%xlabel('Location x'), ylabel('Displacement')

%========================================================================================
% NUMERISCHE LÖSUNG u(x,t)
u = zeros(length(T),length(x));
for t = 1:length(T)
    for k=0:N
        u(t,:) = u(t,:) + rho(t,1+2*k)*U(k+1,:);
    end
end

% ANALYTISCHE LÖSUNG (für N=2 -> 3.EIGENFORM)
if N==2
    omega(1) = (1*pi)^2*sqrt(E*I0/(l^4*mu0));
    omega(2) = (2*pi)^2*sqrt(E*I0/(l^4*mu0));
    omega(3) = (3*pi)^2*sqrt(E*I0/(l^4*mu0));
    c = y0([1,3,5]); % Anfangsauslenkung 
    s = [0 0 0];     % Anfangsgeschwindigkeit
    u_ana = zeros(length(T),length(x));
    for t = 1:length(T)
        for k=1:3
            u_ana(t,:) = u_ana(t,:)+(c(k)*cos(omega(k)*T(t))+s(k)*sin(omega(k)*T(t)))*U(k,:);
        end
    end
end

% ANIMATION 
set(gcf,'CloseRequestFcn','stop=1; closereq;');
figure, p1 = plot(x,u(1,:),'LineWidth',3); Leg{1} = 'Numerisch';
if N==2 % Analytische Lösung
    hold on, p2 = plot(x,u_ana(1,:),'r-.','LineWidth',3); Leg{2} = 'Analytisch'; 
end 
u_max = max(max(u));
axis([0,l,-u_max,u_max]), legend(Leg,'location','northwest')
for t = 1:length(T)
    set(p1,'YData',u(t,:))
    if N==2, set(p2,'YData',u_ana(t,:)); end   % Analytical solution
    set(gca,'FontSize',16), xlabel('Lage x'),
    title(['Zeit t = ' num2str(T(t),'%6.5f')]) 
    pause(0.00005);
    drawnow
end

