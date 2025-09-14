% Clear variables and figures
clear all; close all; clc;

% Double Pendulum Parameters
m1 = 1; % Mass of the first pendulum bob (kg)
m2 = 1; % Mass of the second pendulum bob (kg)
l1 = 1; % Length of the first rod (m)
l2 = 1; % Length of the second rod (m)
g = 9.81; % Acceleration due to gravity (m/s^2)
k1 = 0; % Damping coefficient for theta1
k2 = 0.0; % Damping coefficient for theta2

% Initial Conditions [theta1, dtheta1, theta2, dtheta2]
theta1_0 = pi; % Initial angle of first pendulum (rad)
theta2_0 = theta1_0; % Initial angle of second pendulum (rad)
dtheta1_0 = 0; % Initial angular velocity of first pendulum (rad/s)
dtheta2_0 = 0.01; % Initial angular velocity of second pendulum (rad/s)
initial_conditions = [theta1_0; dtheta1_0; theta2_0; dtheta2_0];

% Time Span
tspan = [0, 20]; % Simulation time (s)

% ODE Solver Options (Stricter Tolerances)
options = odeset('RelTol', 1e-10, 'AbsTol', 1e-12);

% Solve the Original and Linearized Equations
[t, Y] = ode45(@(t, y) double_pendulum_ode(t, y, m1, m2, l1, l2, g, k1, k2), tspan, initial_conditions, options);
[t_lin, Y_lin] = ode45(@(t, y) linearized_double_pendulum_ode(t, y, m1, m2, l1, l2, g, k1, k2), tspan, initial_conditions, options);

% Evaluate at Equidistant Time Points
t_fine = linspace(tspan(1), tspan(2), 1000);
Y_fine = interp1(t, Y, t_fine);
Y_lin_fine = interp1(t_lin, Y_lin, t_fine);

% Extract Positions
theta1 = Y_fine(:, 1); theta2 = Y_fine(:, 3);
theta1_lin = Y_lin_fine(:, 1); theta2_lin = Y_lin_fine(:, 3);

% Original System Positions
x1 = l1 * sin(theta1); y1 = -l1 * cos(theta1);
x2 = x1 + l2 * sin(theta2); y2 = y1 - l2 * cos(theta2);

% Linearized System Positions
x1_lin = l1 * sin(theta1_lin); y1_lin = -l1 * cos(theta1_lin);
x2_lin = x1_lin + l2 * sin(theta2_lin); y2_lin = y1_lin - l2 * cos(theta2_lin);

% Add video writer setup
video_filename = 'double_pendulum_animation_counter_phase_flatter.mp4';
video_writer = VideoWriter(video_filename, 'MPEG-4');
video_writer.FrameRate = 30; % Set frame rate
open(video_writer);

% Animation Setup
figure('Color', 'w','Position',[100 100 950 400]);
axis equal;
axes1 = subplot(1, 2, 1); hold on; grid on;
title('Original Double Pendulum');
xlabel('X Position (m)'); ylabel('Y Position (m)');
axis([-l1-l2-0.5, l1+l2+0.5, -l1-l2-0.5, l1+l2+0.5]);

axes2 = subplot(1, 2, 2); hold on; grid on;
title('Linearized Double Pendulum');
xlabel('X Position (m)'); ylabel('Y Position (m)');
axis([-l1-l2-0.5, l1+l2+0.5, -l1-l2-0.5, l1+l2+0.5]);

% Initial Plots
[rod1, rod2, bob1, bob2] = plot_pendulum(axes1, x1(1), y1(1), x2(1), y2(1));
[rod1_lin, rod2_lin, bob1_lin, bob2_lin] = plot_pendulum(axes2, x1_lin(1), y1_lin(1), x2_lin(1), y2_lin(1));

% Animate and Save Frames
for i = 1:length(t_fine)
    % Update original pendulum
    update_pendulum(rod1, rod2, bob1, bob2, x1(i), y1(i), x2(i), y2(i));
    
    % Update linearized pendulum
    update_pendulum(rod1_lin, rod2_lin, bob1_lin, bob2_lin, x1_lin(i), y1_lin(i), x2_lin(i), y2_lin(i));
    
    drawnow;
    
    % Capture frame and write to video
    frame = getframe(gcf);
    writeVideo(video_writer, frame);
end

% Close the video writer
close(video_writer);

disp(['Animation saved as ', video_filename]);

% Functions
function dydt = double_pendulum_ode(~, y, m1, m2, l1, l2, g, k1, k2)
    % Nonlinear dynamics
    theta1 = y(1); dtheta1 = y(2);
    theta2 = y(3); dtheta2 = y(4);
    delta_theta = theta1 - theta2;
    delta_dtheta = dtheta2 - dtheta1;

    M = [(m1 + m2) * l1, m2 * l2 * cos(delta_theta); 
         m2 * l1 * cos(delta_theta), m2 * l2];
    b = [-m2 * l2 * dtheta2^2 * sin(delta_theta) - (m1 + m2) * g * sin(theta1) - k1 * dtheta1; 
          m2 * l1 * dtheta1^2 * sin(delta_theta) - m2 * g * sin(theta2) - k2 * delta_dtheta];
    ddtheta = M \ b;

    dydt = [dtheta1; ddtheta(1); dtheta2; ddtheta(2)];
end

function dydt = linearized_double_pendulum_ode(~, y, m1, m2, l1, l2, g, k1, k2)
    % Linearized dynamics
    theta1 = y(1); dtheta1 = y(2);
    theta2 = y(3); dtheta2 = y(4);

    M = [(m1 + m2) * l1, m2 * l2; 
         m2 * l1, m2 * l2];
    b = [-(m1 + m2) * g * theta1 - k1 * dtheta1; 
         -m2 * g * theta2 - k2 * (dtheta2 - dtheta1)];
    ddtheta = M \ b;

    dydt = [dtheta1; ddtheta(1); dtheta2; ddtheta(2)];
end

function [rod1, rod2, bob1, bob2] = plot_pendulum(ax, x1, y1, x2, y2)
    % Helper to plot initial pendulum
    rod1 = line(ax, [0, x1], [0, y1], 'Color', 'b', 'LineWidth', 2);
    rod2 = line(ax, [x1, x2], [y1, y2], 'Color', 'r', 'LineWidth', 2);
    bob1 = plot(ax, x1, y1, 'bo', 'MarkerSize', 10, 'MarkerFaceColor', 'b');
    bob2 = plot(ax, x2, y2, 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
end

function update_pendulum(rod1, rod2, bob1, bob2, x1, y1, x2, y2)
    % Helper to update pendulum positions
    set(rod1, 'XData', [0, x1], 'YData', [0, y1]);
    set(rod2, 'XData', [x1, x2], 'YData', [y1, y2]);
    set(bob1, 'XData', x1, 'YData', y1);
    set(bob2, 'XData', x2, 'YData', y2);
end
