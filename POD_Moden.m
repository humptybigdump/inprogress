clear;
mkdir('Results')
%% Settings
Modes=[1,2,3,4,5,6]; %Moden die geplottet werden sollen


%% Lade POD Ergebnisse
load('Data/POD_Results.mat')
% Psi: Moden psi(Freiheitsgrade jeder Mode [hier U und V], Modennummer)
% lambda: Diagonalmatrix mit Eigenwerten/ lambda_2: Vektor mit Eigenwerten
% a:Rekonstruierte Koeffizienten der Moden a(Coefficients of the modes, timesteps)
% Netz: xx,yy

[X_size,Y_size]=size(xx);
%% Plotte Eigenwerte der Moden
f=figure
set(f,'Position',[10 50 400 350],'Color','w')
set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto')
bar(lambda_2(1:15));
xlabel('j');
ylabel('lambda_j');
xlim([0,16])
shoudlbe1=sum(lambda_2);

mkdir('Results/Modes')
print(f,'-dpng',['Results/Modes/PowerDistr.png'],'-r100')


%% Plotte mehrere Moden


for i=Modes
    f=figure;
    set(f,'Position',[10 50 1800 1200],'Color','w')
    set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');
    U_mode=reshape(psi(1:X_size*Y_size,i),[X_size,Y_size]);
    V_mode=reshape(psi(X_size*Y_size+1:X_size*Y_size*2,i),[X_size,Y_size]);
    quiver(xx,yy,U_mode,V_mode,2);
    
    title(['Mode',num2str(i)])
    xlabel('x');
    ylabel('y');
    
    axis equal

    print(f,'-dpng',['Results/Modes/Mode_No_',num2str(i),'.png'],'-r100')
end


% hold on
%     U_mode=reshape(psi(1:X_size*Y_size,2),[X_size,Y_size]);
%     V_mode=reshape(psi(X_size*Y_size+1:X_size*Y_size*2,2),[X_size,Y_size]);
%     quiver(xx,yy,U_mode,V_mode,2,'r');
    
