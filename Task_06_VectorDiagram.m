% Script for Vector Diagrams for Different Modulation Methods
% Power Electronics
% Written by: Jens Bausch
% Last revision: Simon Frank, 4th July, 2023

% Clear Workspace, Command Window and Figures
clc
clear
close all

% Constants
loops = 100;
gammas = 0:2*pi/(loops-1):2*pi;                 % Angle for one period
scale = 1;                                    % Degree of Mudulation
modulation = "supersine";                   % Modulation types: sine-triangle, supersine, flattop
video = false;                                   % Video recording?

% Check if modulation type is valid
if modulation == "sine-triangle" || modulation == "supersine" || modulation == "flattop"
    valid = true;
else
    valid = false;
    disp("Please enter a valid modulation type.")
end

if valid == true
    
    % Create figure
    f = figure;
    f.Position = [100 100 1200 500];
    set(gcf,'color','w');
    grid on, axis equal
    hold on

    % Variable for Video Recording
    if video == true
        v = VideoWriter(modulation+'.avi','Motion JPEG AVI');
        v.Quality = 100;
        open(v);
    end
    
    % Predefine Arrays for functions over time        
    u_N0_array = zeros(loops,1);
    Ua_array = zeros(loops,1);
    Ub_array = zeros(loops,1);
    Uc_array = zeros(loops,1);

    % Start Vector Diagram Simulation
    for k = 1:loops
        gamma = gammas(k) - pi/2;
        Ua = scale*exp(1i*gamma);
        Ub = scale*exp(1i*gamma -2i*pi/3); 
        Uc = scale*exp(1i*gamma -4i*pi/3);

        % Modulation type -> Calculate Common Mode Voltage
        switch modulation
            
            % Sine-Triangle Modulation
            case "sine-triangle"
                u_N0 = 0;
            case "supersine"
                u_N0 = -(max([real(Ua) real(Ub) real(Uc)]) + min([real(Ua) real(Ub) real(Uc)]))/ 2;
            case "flattop"
                if abs(real(Ua)) > abs(real(Ub)) && abs(real(Ua)) > abs(real(Uc))
                    if real(Ua) > 0
                        u_N0_1 = 1 - real(Ua);
                    else 
                        u_N0_1 = -1 - real(Ua);
                    end
                else
                    u_N0_1 = 0;
                end 
                if abs(real(Ub)) > abs(real(Ua)) && abs(real(Ub)) > abs(real(Uc))
                    if real(Ub) > 0
                        u_N0_2 = 1 - real(Ub);
                    else 
                        u_N0_2 = -1 - real(Ub);
                    end
                else
                    u_N0_2 = 0;
                end 
                if abs(real(Uc)) > abs(real(Ub)) && abs(real(Uc)) > abs(real(Ua))
                    if real(Uc) > 0
                        u_N0_3 = 1 - real(Uc);
                    else 
                        u_N0_3 = -1 - real(Uc);
                    end
                else
                    u_N0_3 = 0;
                end 
                u_N0 = u_N0_1 + u_N0_2 + u_N0_3;
        end

        % Layout: 2 graphs next to each other, first diagram on the left: vector diagram 
        tiledlayout(1, 2)
        ax1 = nexttile;

        % Reference (start of vector) for phase vectors is u_N0
        refStart=u_N0; 

        % 1st arrow: phase a
        arrow=Ua;
        Uuplot=quiver(real(refStart),imag(refStart),real(arrow),imag(arrow), 'Color', [0, 0.4470, 0.7410], 'MaxHeadSize', 0.2/norm(arrow));
        hold on
        % 2nd arrow: phase b   
        arrow=Ub;
        Uvplot=quiver(real(refStart),imag(refStart),real(arrow),imag(arrow), 'Color', [0.8500 0.3250 0.0980], 'MaxHeadSize', 0.2/norm(arrow));
        
        % 3rd arrow: phase c
        arrow=Uc;
        Uwplot=quiver(real(refStart),imag(refStart),real(arrow),imag(arrow), 'Color', [0.700 0.6250 0], 'MaxHeadSize', 0.2/norm(arrow));
        
        % 4th arrow: length phase a
        arrow=Ua;
        UuplotT=quiver(real(refStart),imag(refStart),real(arrow),0, '-.', 'Color', [0 0.4470 0.7410], 'MaxHeadSize', 0.2/norm(real(arrow)));

        % 5th arrow: length phase b
        arrow=Ub;
        UvplotT=quiver(real(refStart),imag(refStart),real(arrow),0, '-.', 'Color', [0.8500 0.3250 0.0980], 'MaxHeadSize', 0.2/norm(real(arrow)));

        % 6th arrow: length phase c
        arrow=Uc;
        UwplotT=quiver(real(refStart),imag(refStart),real(arrow),0, '-.', 'Color', [0.700 0.6250 0], 'MaxHeadSize', 0.2/norm(real(arrow)));
        
        % 7th arrow: common mode voltage
        refStart=0; 
        arrow = u_N0;
        U0plotT=quiver(real(refStart),imag(refStart),real(arrow),0, 'Color', 'k', 'MaxHeadSize', 0.2/norm(real(arrow)));
        
        hold off
        % Draw circle in alpha-beta plane 
        circle(real(u_N0),0,scale);

        % Properties vector diagram
        legend('$\underline{u}_\mathrm{aN}$','$\underline{u}_\mathrm{bN}$','$\underline{u}_\mathrm{cN}$','$\Re(u_\mathrm{a0})$', '$\Re(u_\mathrm{b0})$','$\Re(u_\mathrm{c0})$','$u_\mathrm{N0}$','Interpreter','Latex')
        xlim([-1.5 1.5]);
        ylim([-1.5 1.5]);
        set(gca,'TickLabelInterpreter','latex')
        xlabel('Re($\frac{u}{U_\mathrm{DC}/2}$)','Interpreter','latex');
        ylabel('Im($\frac{u}{U_\mathrm{DC}/2}$)','Interpreter','latex');
        hAutoScale=findobj('-property','AutoScale');                                % switch off the Quivergroup Property AutoScale for all arrows
        set(hAutoScale,'AutoScale','off')
        grid on
        
        % Arrays for functions over time        
        u_N0_array(k) = real(u_N0);
        Ua_array(k) = real(Ua + u_N0);
        Ub_array(k) = real(Ub + u_N0);
        Uc_array(k) = real(Uc + u_N0);

        % Right diagram: waveform over time
        ax2 = nexttile;
        hold on
        % Common mode voltage over time
        plot(gammas(1:k), u_N0_array(1:k), 'Color', 'k');
        % Phase-to-midpoint voltage of phase a over time (u_a0(t))
        plot(gammas(1:k), Ua_array(1:k), 'Color', [0, 0.4470, 0.7410]);
        % Phase-to-midpoint voltage of phase b over time (u_a0(t))
        plot(gammas(1:k), Ub_array(1:k), 'Color', [0.8500 0.3250 0.0980]);
        % Phase-to-midpoint voltage of phase c over time (u_a0(t))
        plot(gammas(1:k), Uc_array(1:k), 'Color', [0.700 0.6250 0]);
        % Phase-to-neutral voltage of phase a over time (u_aN(t))
        plot(gammas(1:k), Ua_array(1:k) - u_N0_array(1:k), 'Color', [0 0 1]);

        % Properties waveform diagram
        hold off
        ylim([-1.5, 1.5]);
        xlim([0 2*pi]);
        set(gca,'XTick',0:pi/4:2*pi)
        set(gca,'XTickLabel',{'0', '$\frac{\pi}{4}$', '$\frac{\pi}{3}$', '$\frac{3\pi}{4}$', '$\pi$', '$\frac{5\pi}{4}$', '$\frac{3\pi}{2}$', '$\frac{7\pi}{4}$', '$2\pi$'}) 
        set(gca,'TickLabelInterpreter','latex')
        legend('$\it{u}_\mathrm{N0}$', '$\it{u}_\mathrm{a0}$','$\it{u}_\mathrm{b0}$','$\it{u}_\mathrm{c0}$','$\it{u}^{*}_\mathrm{aN}$','Interpreter','latex')
        xlabel('$\gamma$ in rad','Interpreter','latex');
        ylabel('$\frac{u}{U_\mathrm{DC}/2}$','Interpreter','latex');
        grid on
        frame = getframe(gcf);

        if video == true
            writeVideo(v,frame);
        end
    end
    
    if video == true
        close(v);
    end
end

% Function for plotting a circle 
function h = circle(x,y,r)
hold on
th = 0:pi/50:2*pi;
xunit = r * cos(th) + x;
yunit = r * sin(th) + y;
h = plot(xunit, yunit, 'Color', [0.5 0.5 0.5]);
hold off
end
