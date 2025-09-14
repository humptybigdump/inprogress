clear;
mkdir('Results')

%% Settings
modes=[1:11]; % Moden welche zur Rekonstruktion verwendet werden sollen

%% Lade Geschwindigkeitsdaten
load('Data/VelData.mat')

% Netz: xx,yy
% Geschwindigkeitsdaten U_3D(x-Koord,y-Koord,Zeitschrit)
% Wirbelstärke omega(x-Koord,y-Koord,Zeitschrit)

[X_size,Y_size,tsteps]=size(U_3D);
%% Lade POD Ergebnisse
load('Data/POD_Results.mat')
% Psi: Moden psi(Freiheitsgrade jeder Mode [hier U und V], Modennummer)
% lambda: Diagonalmatrix mit Eigenwerten/ lambda_2: Vektor mit Eigenwerten
% a:Rekonstruierte Koeffizienten der Moden a(Coefficients of the modes, timesteps)
% Netz: xx,yy


%% Zeitlicher Mittelwert des Geschwindigkeitsfeldes

% Berechne Mittelwert von U_3D und V_3D
U_3D_sum=zeros(X_size,Y_size);
V_3D_sum=zeros(X_size,Y_size);
for i=1:tsteps
    U_3D_sum=U_3D_sum+U_3D(:,:,i);
    V_3D_sum=V_3D_sum+V_3D(:,:,i);
    
end
U_3D_mean=U_3D_sum/tsteps;
V_3D_mean=V_3D_sum/tsteps;



%% REKONSTRUIERE GESCWHINDIGKEITSFELD AUS xx Moden

transpsi=transpose(psi);
u_part_re=zeros(X_size*Y_size*2,500);
disp(['The reconstruction contains ',num2str(sum(lambda_2(modes(1):modes(end)))*100),' % of the energy contained in the fluctuations of the data set'])
%Rekonstruktion
for timestep=1:500
    
    for mode=modes
        u_part_re(:,timestep)=u_part_re(:,timestep)+a(mode,timestep)*psi(:,mode);
    end
U_3D_mean2(:,:,timestep)=U_3D_mean;
V_3D_mean2(:,:,timestep)=V_3D_mean;
end


u_re=reshape(u_part_re(1:X_size*Y_size,:),[X_size,Y_size,500]);%+U_3D_mean2;
v_re=reshape(u_part_re(1+X_size*Y_size:X_size*Y_size*2,:),[X_size,Y_size,500]);%+V_3D_mean2;


%% Berechnung der Wirbelstärke
[x,y]=meshgrid(1:65,1:49);
% u_vort=permute(U_3D_mean2,[2,1,3]);
u_vort=permute(u_re+U_3D_mean2,[2,1,3]);
% u_vort=permute(u_re,[2,1,3]);
x_vort=permute(xx,[2,1]);
y_vort=permute(yy,[2,1]);
% v_vort=permute(V_3D_mean2,[2,1,3]);
v_vort=permute(v_re+V_3D_mean2,[2,1,3]);
% v_vort=permute(v_re,[2,1,3]);
[ux,uy]=gradient(u_vort);
[vx,vy]=gradient(v_vort);
omega_re=vx-uy;
omega_re=permute(omega_re,[2,1,3]);


%% Plotte rekonstruiertes Geschwindigkeitsfeld und das gemessene Geschwindigkeitsfeld

f=figure
set(f,'Position',[10 50 1500 600],'Color','w')
set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');
timestep=122;
subplot(1,2,1)
[p3,p4]=contourf(xx(:,:),yy(:,:),omega_re(:,:,122),15,'LineStyle','none');
% colorbar


hold on
p2=quiver(xx(:,:),yy(:,:),u_re(:,:,timestep),v_re(:,:,timestep),2,'k','AutoScale','off','AutoScaleFactor',3,'MaxHeadSize',0.5);
axis equal

subplot(1,2,2)
[p6,p7]=contourf(xx(:,:),yy(:,:),omega(:,:,122),15,'LineStyle','none');
% colorbar

hold on
p5=quiver(xx(:,:),yy(:,:),U_3D(:,:,timestep),V_3D(:,:,timestep),2,'k','AutoScale','off','AutoScaleFactor',3,'MaxHeadSize',0.5);
axis equal
mkdir('Results')
mkdir('Results/Reconstruct')
for timestep=1:1:800
    set(p4,'ZData',omega_re(:,:,timestep));

%     set(p2,'UData',u_re(:,:,timestep)+U_3D_mean,'VData',v_re(:,:,timestep)+V_3D_mean);
    set(p2,'UData',u_re(:,:,timestep),'VData',v_re(:,:,timestep));
    set(p7,'ZData',omega(:,:,timestep));
%     caxis([-0.022,0.022])
    set(p5,'UData',U_3D(:,:,timestep)-U_3D_mean(:,:),'VData',V_3D(:,:,timestep)-V_3D_mean(:,:));
%     set(p5,'UData',U_3D(:,:,timestep),'VData',V_3D(:,:,timestep));
%      set(p2,'UData',u_re(:,:,timestep),'VData',v_re(:,:,timestep));
    xlabel('x');
    ylabel('y');

    subplot(1,2,1)
    title(['Reconstructed Data; timestep: ',num2str(timestep)]);

      xlabel('x');
    ylabel('y');

    subplot(1,2,2)
    title(['Raw Data; timestep: ',num2str(timestep)]);
        drawnow
    pause(0.0001)
%         print(f,'-dpng',['Results/Reconstruct/Timestep',num2str(1000+timestep),'.png'],'-r100')
    
end