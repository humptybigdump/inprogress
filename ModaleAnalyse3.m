function [m,c,w,phi]= ModaleAnalyse3(M,C,x0,t)
% Matrizenschreibweise :
%    M  - Massenmatrix
%    C  - Steifigkeitsmatrix
%    phi- Eigenvektor des Systems
%--------------------------------------------------------------------------
% Ermittlung der Eigenfrequenzen und der Eigenvektoren
[V,wn]=eig(C,M);
[W,k]=sort(diag(wn));
V=V(:,k); 
Faktor=diag(V'*M*V);
Phi=V*inv(sqrt(diag(Faktor)));
Omega=diag(sqrt(Phi'*C*Phi)); 

% Bestimmung der Modalmatrix phi
w = diag(Omega(1:length(M)));
phi1 = Phi(:,1:length(M)) ;
phi  = [phi1(:,1)/phi1(1,1)   phi1(:,2)/phi1(1,2)  phi1(:,3)/phi1(1,3)];

% Matrix M,C -> Diagonalmatrix m,c -> entkoppelte DGL
m = phi'*M*phi ;
c = phi'*C*phi ;

% Anfangsbedingungen
inv_phi = inv(m)*phi'*M;
y0 = inv_phi * x0;

% Lösung in die generalisierten Koordinaten y(t)
y1 = y0(1,1)*cos(w(1,1)*t);
y2 = y0(2,1)*cos(w(2,2)*t);
y3 = y0(3,1)*cos(w(3,3)*t);
subplot(2,1,1), plot(t,y1, t,y2, t,y3,'r','LineWidth',2)
set(gca,'FontSize',16)
title('Lösung in die generalisierten Koordinaten y(t)')
xlabel('t'), ylabel('y(t)')
legend('m_1','m_2','m_3')

% Lösung in die Originalkoordinaten x(t)
x1 = phi(1,1)*y1 + phi(1,2)*y2 + phi(1,3)*y3;
x2 = phi(2,1)*y1 + phi(2,2)*y2 + phi(2,3)*y3;
x3 = phi(3,1)*y1 + phi(3,2)*y2 + phi(3,2)*y3;
subplot(2,1,2), plot(t,x1, t,x2, t,x3,'r','LineWidth',2)
set(gca,'FontSize',16)
title('Lösung in die Originalkoordinaten x(t)')
xlabel('t'), ylabel('x(t)')
legend('m_1','m_2','m_3')
