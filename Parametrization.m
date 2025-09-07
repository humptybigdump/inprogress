% Parametrization of the Simulink / PLECS modell for the AC-Bridge loss calculation
% Function is automatically called during Simulink model initialization (initFcn)
% written by: Simon Frank, June 2022
% edited by: Nick Thoenelt, June 2024

close all
clearvars
clc

% change the current folder to the folder of this m-file.
if(~isdeployed)
  cd(fileparts(matlab.desktop.editor.getActiveFilename));
end

folder = fileparts(which(matlab.desktop.editor.getActiveFilename)); 
addpath(genpath(folder));

%__________________________________________________________________________

ref_freq = 60;                              % Frequency of the reference signal
car_freq = 6290;                            % Frequency of the carrier signal
beta_SQ = 2*pi/3;                           % Angle basic frequency modulation
t_lock = 1e-6;                              % Locking time for half-bridge

u_ab_amp = 318;                             % Amplitude of the output voltage u_ab in volt
u_ab_phase = 0;                             % Phase shift of the output voltage u_ab in rad
u_ab_freq = ref_freq*2*pi;                  % Frequency of the output voltage u_ab in rad/s
U_DC = 500;                                 % DC link voltage in volt

L_load = 16.89e-3;                          % Inductance of the load choke in Henry (16.89e-3), change to 33.78e-3 (I_ab = 41.11 A) or 29.25e-3 (I_ab,1 = 50 A) (for basic frequency modulation
I_amp = u_ab_amp/(2*pi*ref_freq*L_load);    % For choke current initial condition (u_ab_amp/(2*pi*ref_freq*L_load), change to zero for basic frequency modulation
R_source = 1e-3;                            % DC source resistance in ohm, necessary to ensure simulation model stability

T_init = 125;                               % Initial Temperature: semiconductors and heat sink element

Clk="Simultaneous";                         % Modulation variant variable: "Simultaneous","Alternating,"SquareWave"

%__________________________________________________________________________

i_vec = linspace(0,3*I_amp,10);
theta_application = 125; % device tempaerature in application in degC
t_sample = 1e-6;

filename_transistor = 'FF75R12RT4_igbt.xml';
file = readstruct(filename_transistor);

e_on_interp_T = XMLtoEon(file);
for j = 1:1:length(i_vec)
    e_on_T(j) = e_on_interp_T(U_DC, i_vec(j), theta_application);
end

e_off_interp_T = XMLtoEoff (file);
for j = 1:1:length(i_vec)
    e_off_T(j) = e_off_interp_T(U_DC, i_vec(j), theta_application);
end

p_cond_interp_T = XMLtoPcond (file);
for j = 1:1:length(i_vec)
    p_cond_T(j) = p_cond_interp_T(U_DC, i_vec(j), theta_application);
end

%__________________________________________________________________________

filename_diode = 'FF75R12RT4_diode.xml';
file = readstruct(filename_diode);

e_off_interp_D = XMLtoEoff (file);
for j = 1:1:length(i_vec)
    e_off_D(j) = e_off_interp_D(-U_DC, i_vec(j), theta_application); %!-1
end

p_cond_interp_D = XMLtoPcond (file);
for j = 1:1:length(i_vec)
    p_cond_D(j) = p_cond_interp_D(U_DC, i_vec(j), theta_application);
end










%__________________________________________________________________________

function [e_on_interp] = XMLtoEon (file)
    % create turn-on loss map
    i_grid = str2num(file.Package.SemiconductorData(1).TurnOnLoss.CurrentAxis(1));
    v_grid = str2num(file.Package.SemiconductorData(1).TurnOnLoss.VoltageAxis(1))';
    theta_grid_reshape = str2num(file.Package.SemiconductorData(1).TurnOnLoss.TemperatureAxis(1));
    theta_grid = reshape(theta_grid_reshape,[1, 1, size(theta_grid_reshape, 2)]);
    % create ngrid for grid points
    i_ngrid = repmat(i_grid,[size(v_grid,1), 1, size(theta_grid, 3)]);
    v_ngrid = repmat(v_grid,[1, size(i_grid,2), size(theta_grid, 3)]);
    theta_ngrid = repmat(theta_grid, [size(v_grid,1), size(i_grid,2), 1]);
    
    for j = 1:1:size(theta_grid,3)
        for i = 1:1:size(v_grid,1)
            e_on_map(i,:,j) = str2num(file.Package.SemiconductorData(1).TurnOnLoss.Energy.Temperature(j).Voltage(i));
        end
    end
    
    e_on_map = e_on_map .* file.Package.SemiconductorData(1).TurnOnLoss.Energy.scaleAttribute;
    
    figure;
    scatter3(i_ngrid(:,:,1), v_ngrid(:,:,1), e_on_map(:,:,1), 'xk');
    xlabel('i_{on} in A');
    ylabel('v_{block} in V');
    zlabel('E_{on} in J');
    hold on
    for j = 1:1:size(theta_grid,3)
        scatter3(i_ngrid(:,:,j), v_ngrid(:,:,j), e_on_map(:,:,j), 'xk');
    end
    
    %__________________________________________________________________________
    
    % interpolate loss map
    e_on_interp = griddedInterpolant(v_ngrid, i_ngrid, theta_ngrid, e_on_map,'makima','linear');
    i_vec = linspace(min(i_grid),max(i_grid),20);
    v_vec = linspace(min(v_grid),max(v_grid),20)';
    theta_vec_reshape = linspace(20,200,10);
    theta_vec = reshape(theta_vec_reshape,[1, 1, size(theta_vec_reshape, 2)]);
    % create ngrid for grid points
    i_ngrid = repmat(i_vec,[size(v_vec,1), 1, size(theta_vec, 3)]);
    v_ngrid = repmat(v_vec,[1, size(i_vec,2), size(theta_vec, 3)]);
    theta_ngrid = repmat(theta_vec, [size(v_vec,1), size(i_vec,2), 1]);
    
    %__________________________________________________________________________
    
    figure;
    surf(i_ngrid(:,:,1), v_ngrid(:,:,1), e_on_interp(v_ngrid(:,:,1), i_ngrid(:,:,1), theta_ngrid(:,:,1)));
    xlabel('i_{on} in A');
    ylabel('v_{block} in V');
    zlabel('E_{on} in J');
    hold on
    for j = 1:1:size(theta_vec,3)
        surf(i_ngrid(:,:,j), v_ngrid(:,:,j), e_on_interp(v_ngrid(:,:,j), i_ngrid(:,:,j), theta_ngrid(:,:,j)));
    end
    hold off
    alpha 0.5
end

%__________________________________________________________________________

function [e_off_interp] = XMLtoEoff (file)
    % create turn-on loss map
    i_grid = str2num(file.Package.SemiconductorData(1).TurnOffLoss.CurrentAxis(1));
    v_grid = str2num(file.Package.SemiconductorData(1).TurnOffLoss.VoltageAxis(1))';
    theta_grid_reshape = str2num(file.Package.SemiconductorData(1).TurnOffLoss.TemperatureAxis(1));
    theta_grid = reshape(theta_grid_reshape,[1, 1, size(theta_grid_reshape, 2)]);
    % create ngrid for grid points
    i_ngrid = repmat(i_grid,[size(v_grid,1), 1, size(theta_grid, 3)]);
    v_ngrid = repmat(v_grid,[1, size(i_grid,2), size(theta_grid, 3)]);
    theta_ngrid = repmat(theta_grid, [size(v_grid,1), size(i_grid,2), 1]);
    
    for j = 1:1:size(theta_grid,3)
        for i = 1:1:size(v_grid,1)
            e_off_map(i,:,j) = str2num(file.Package.SemiconductorData(1).TurnOffLoss.Energy.Temperature(j).Voltage(i));
        end
    end
    
    e_off_map = e_off_map .* file.Package.SemiconductorData(1).TurnOffLoss.Energy.scaleAttribute;
    
    figure;
    scatter3(i_ngrid(:,:,1), v_ngrid(:,:,1), e_off_map(:,:,1), 'xk');
    xlabel('i_{on} in A');
    ylabel('v_{block} in V');
    zlabel('E_{off} in J');
    hold on
    for j = 1:1:size(theta_grid,3)
        scatter3(i_ngrid(:,:,j), v_ngrid(:,:,j), e_off_map(:,:,j), 'xk');
    end
    
    %__________________________________________________________________________
    
    % interpolate loss map
    e_off_interp = griddedInterpolant(v_ngrid, i_ngrid, theta_ngrid, e_off_map,'makima','linear');
    i_vec = linspace(min(i_grid),max(i_grid),20);
    v_vec = linspace(min(v_grid),max(v_grid),20)';
    theta_vec_reshape = linspace(20,200,10);
    theta_vec = reshape(theta_vec_reshape,[1, 1, size(theta_vec_reshape, 2)]);
    % create ngrid for grid points
    i_ngrid = repmat(i_vec,[size(v_vec,1), 1, size(theta_vec, 3)]);
    v_ngrid = repmat(v_vec,[1, size(i_vec,2), size(theta_vec, 3)]);
    theta_ngrid = repmat(theta_vec, [size(v_vec,1), size(i_vec,2), 1]);
    
    %__________________________________________________________________________
    
    figure;
    surf(i_ngrid(:,:,1), v_ngrid(:,:,1), e_off_interp(v_ngrid(:,:,1), i_ngrid(:,:,1), theta_ngrid(:,:,1)));
    xlabel('i_{on} in A');
    ylabel('v_{block} in V');
    zlabel('E_{off} in J');
    hold on
    for j = 1:1:size(theta_vec,3)
        surf(i_ngrid(:,:,j), v_ngrid(:,:,j), e_off_interp(v_ngrid(:,:,j), i_ngrid(:,:,j), theta_ngrid(:,:,j)));
    end
    hold off
    alpha 0.5
end

%__________________________________________________________________________

function [p_cond_interp] = XMLtoPcond (file)
    % create turn-on loss map
    i_grid = str2num(file.Package.SemiconductorData(1).ConductionLoss.CurrentAxis(1));
    v_grid = str2num(file.Package.SemiconductorData(1).TurnOffLoss.VoltageAxis(1))'; % blocking voltages from turn-off data, conduction not dependant from blocking voltage
    theta_grid_reshape = str2num(file.Package.SemiconductorData(1).ConductionLoss.TemperatureAxis(1));
    theta_grid = reshape(theta_grid_reshape,[1, 1, size(theta_grid_reshape, 2)]);
    % create ngrid for grid points
    i_ngrid = repmat(i_grid,[size(v_grid,1), 1, size(theta_grid, 3)]);
    v_ngrid = repmat(v_grid,[1, size(i_grid,2), size(theta_grid, 3)]);
    theta_ngrid = repmat(theta_grid, [size(v_grid,1), size(i_grid,2), 1]);
    
    for j = 1:1:size(theta_grid,3)
        for i = 1:1:size(v_grid,1)
            p_cond_map(i,:,j) = (str2num(file.Package.SemiconductorData(1).ConductionLoss.VoltageDrop.Temperature(j)) .* i_grid);
        end
    end
    
    figure;
    scatter3(i_ngrid(:,:,1)./1000, v_ngrid(:,:,1)./1000, p_cond_map(:,:,1)./1000, 'xk');
    xlabel('\iti\rm_{cond} in kA');
    ylabel('\itv\rm_{block} in kV');
    zlabel('\itP\rm_{cond} in kW');
    hold on
    for j = 1:1:size(theta_grid,3)
        scatter3(i_ngrid(:,:,j)./1000, v_ngrid(:,:,j)./1000, p_cond_map(:,:,j)./1000, 'xk');
    end
    
    %__________________________________________________________________________
    
    % interpolate loss map
    p_cond_interp = griddedInterpolant(v_ngrid, i_ngrid, theta_ngrid, p_cond_map,'makima','linear');
    i_vec = linspace(min(i_grid),max(i_grid),20);
    v_vec = linspace(min(v_grid),max(v_grid),20)';
    theta_vec_reshape = linspace(20,200,10);
    theta_vec = reshape(theta_vec_reshape,[1, 1, size(theta_vec_reshape, 2)]);
    % create ngrid for grid points
    i_ngrid = repmat(i_vec,[size(v_vec,1), 1, size(theta_vec, 3)]);
    v_ngrid = repmat(v_vec,[1, size(i_vec,2), size(theta_vec, 3)]);
    theta_ngrid = repmat(theta_vec, [size(v_vec,1), size(i_vec,2), 1]);
    
    %__________________________________________________________________________
    
    figure;
    surf(i_ngrid(:,:,1)./1000, v_ngrid(:,:,1)./1000, p_cond_interp(v_ngrid(:,:,1), i_ngrid(:,:,1), theta_ngrid(:,:,1))./1000);
    xlabel('\iti\rm_{cond} in kA');
    ylabel('\itv\rm_{DC} in kV');
    zlabel('\itP\rm_{cond} in kW');
    hold on
    for j = 1:1:size(theta_vec,3)
        surf(i_ngrid(:,:,j)./1000, v_ngrid(:,:,j)./1000, p_cond_interp(v_ngrid(:,:,j), i_ngrid(:,:,j), theta_ngrid(:,:,j))./1000);
    end
    % set(gcf, 'Position',  [100, 100, 300, 250])
    hold off
    % alpha 0.5

end
