clear;
mkdir('Results')

%Lade Geschwindigkeitsdaten
load('Data/VelData.mat')
% Netz: xx,yy
% Geschwindigkeitsdaten U_3D(x-Koord,y-Koord,Zeitschrit)
% Wirbelstärke omega(x-Koord,y-Koord,Zeitschrit)


[X_size,Y_size,tsteps]=size(U_3D);

%% Zeitlicher Mittelwert

% Berechne Mittelwert von U_3D und V_3D
U_3D_sum=zeros(X_size,Y_size);
V_3D_sum=zeros(X_size,Y_size);
for i=1:tsteps
    U_3D_sum=U_3D_sum+U_3D(:,:,i);
    V_3D_sum=V_3D_sum+V_3D(:,:,i);
    
end
U_3D_mean=U_3D_sum/tsteps;
V_3D_mean=V_3D_sum/tsteps;

% Plotte Mittleres Geschwindigkeitsfeld
f=figure
set(f,'Position',[10 50 1800 1200],'Color','w')
set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');
quiver(xx,yy,U_3D_mean,V_3D_mean);
axis equal
title('U-mean')

mkdir('Results/Statistik')

print(f,'-dpng',['Results/Statistik/U_mittel.png'],'-r100')

%% Standardabweichung

% Berechne Abweichung vom Mittelwert für jeden Zeitschritt
U_3D_var=nan(size(U_3D));
V_3D_var=nan(size(V_3D));
for i=1:tsteps
    U_3D_var(:,:,i)=U_3D(:,:,i)-U_3D_mean;
    V_3D_var(:,:,i)=V_3D(:,:,i)-V_3D_mean;
    %   disp('dada')
end


% Berechne Standardabweichung
U_der=zeros(X_size,Y_size);
V_der=zeros(X_size,Y_size);
for i=1:tsteps
    U_der=U_der+U_3D_var(:,:,i).^2;
    V_der=V_der+V_3D_var(:,:,i).^2;
end
U_der=U_der/tsteps;
V_der=V_der/tsteps;

%Ausgabe Standardabweichung U
f=figure
set(f,'Position',[10 50 1800 1200],'Color','w')
set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');
contourf(xx,yy,U_der,40,'LineStyle','None');
axis equal
title('Standardabweichung U')

print(f,'-dpng',['Results/Statistik/StdAbwU.png'],'-r100')


%Ausgabe Standardabweichung V
f=figure
set(f,'Position',[10 50 1800 1200],'Color','w')
set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');
contourf(xx,yy,V_der,40,'LineStyle','None');
axis equal
title('Standardabweichung V')
print(f,'-dpng',['Results/Statistik/StdAbwV.png'],'-r100')


%Ausgabe Standardabweichung Betrag der Geschwindigkeit
Umagn=sqrt(U_der.^2+V_der.^2);
f=figure
set(f,'Position',[10 50 1800 1200],'Color','w')
set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');

contourf(xx,yy,Umagn,40,'LineStyle','None');
axis equal
title('Standardabweichung Betrag U,V')
print(f,'-dpng',['Results/Statistik/StdAbwUV.png'],'-r100')


