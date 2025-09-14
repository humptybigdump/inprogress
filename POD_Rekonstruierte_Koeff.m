clear;
mkdir('Results')
%% Settings
Coefficients_2D=true; %Plotte Koeffizienten von mehreren Moden


Lissajou=true; % Plotte Koeffizienten von 2 verschiedenen Moden über die Zeit
ComparedModes=[1,2]; % Moden die gegenübergestellt werden sollen

FFT_a=false; % Frequenzinhaltsanalyse von Koeffizienten a_i;
FFT_a_modes=[3,4]; % Koeffizienten der Moden für die eine FFT gemacht werden soll

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



%% Plotte Koeffizienten der Moden
if Coefficients_2D
    f=figure;
    set(f,'Position',[10 50 1500 500],'Color','w')
    set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');
    
    
    hold on
    a2=plot([1:length(a(2,:))],a(2,:),'Color',[173+20,14+20,6+20]/255,'LineWidth',1);
    a1=plot([1:length(a(1,:))],a(1,:),'Color',[0.0,0.0,0.8],'LineWidth',1);
    
    
    legend('rec. coefficient a^{LES}_2(t)','rec. coefficient a^{LES}_1(t)')
    xlab=xlabel('time step $[-]$');
    set(xlab,'Interpreter','Latex');
    ylab=ylabel('$a^{LES}_j$ $[\frac{\mathrm{m}}{\mathrm{s}}]$');
    set(ylab,'Interpreter','Latex');
    
    
    set(findall(gcf,'type','text'),'fontName','Times New Roman','fontSize',15)
    set(findall(gcf,'type','axes'),'fontName','Times New Roman','fontSize',15)
    
    
    
end
%% Lissajou Figure
if Lissajou
    f=figure;
    set(f,'Position',[10 50 1500 1500],'Color','w')
    set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');
    
    plot3(1:length(a(2,:)),a(ComparedModes(1),:),a(ComparedModes(2),:),'o-','MarkerEdgeColor',[1,0.5,0],'MarkerFaceColor',[1,0.7,0.3],'Color',[1,0.5,0])
    hold on
    axis equal
    
    daspect([140,1,1])
    
    xlab=xlabel('$a^{LES}_2$ $[\frac{\mathrm{m}}{\mathrm{s}}]$');
    set(xlab,'Interpreter','Latex');
    ylab=ylabel('$a^{LES}_3$ $[\frac{\mathrm{m}}{\mathrm{s}}]$');
    set(ylab,'Interpreter','Latex');
    set(findall(gcf,'type','text'),'fontName','Times New Roman','fontSize',15)
    set(findall(gcf,'type','axes'),'fontName','Times New Roman','fontSize',15)
    set(findall(gcf,'type','legend'),'fontName','Times New Roman','fontSize',15)
    
end
%% FFT von der Koeffizienten a_i
if FFT_a
    f=figure;
    
    set(f,'Position',[10 50 500 450],'Color','w')
    set(f, 'PaperUnits', 'inches', 'PaperPosition', [0.2, 0.2, 18, 3.00],'PaperPositionMode','auto');
    
    hold on
    colorthemes=[0.0,0.0,0.8;[173+20,14+20,6+20]/255;0.0,0.95,0.0;1.0,0.95,0.0;0.0,0.95,1.0;1.0,0.95,1.0]
    % order=[1,3,2]
    for i=FFT_a_modes %M
        b=a(i,:);
        c=fft(b(:))/length(b);
        
        Fs=11;
        
        f=linspace(0,1,length(b)/2+1)*Fs/2;
        plot(f(2:length(b)/2+1),abs(c(2:length(b)/2+1)),'Color',colorthemes(i,:),'LineWidth',1.2);
        
        
    end
    
    box on
    set(gca, 'yscale', 'log');
    set(gca, 'xscale', 'log');
    xlab=xlabel('$\omega^* [-]$');
    set(xlab,'Interpreter','Latex');
    ylab=ylabel('$A^{LES}_j(\omega^*)$ $[\frac{\mathrm{m}}{\mathrm{s}}]$');
    set(ylab,'Interpreter','Latex');
    % set(gca,'XTick',[10^-1,1,10^1,10^2],'YTick',[10^-6,10^-3,1]);
    % set(gca,'XLim',[10^-1,300],'YLim',[10^-6,10^0]);
    set(findall(gcf,'type','text'),'fontName','Times New Roman','fontSize',20)
    set(findall(gcf,'type','axes'),'fontName','Times New Roman','fontSize',20)
end

