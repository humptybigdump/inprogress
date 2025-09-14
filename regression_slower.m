close all;

load('data.mat');

w = 5;    % the length of the sliding window

est_poses = zeros(numT,1);        % array to store the estimated vehicle position for each point in time
est_velocities = zeros(numT,1);   % array to store the estimated vehicle speed for each point in time

% For each time step we solve a system of linear equations given as
% A * [x0 v]' = b where the matrix A and the vector b are defined as shown
% in the lecture on slide 6.

% start time measurement
tic

% Implement regression here
for k=1:numT

    % Define matrix A
    if k < w
        t_series = 1:k;
        meas = measurements(t_series, 1);
    else
        t_series = k-w+1 : k;
        meas = measurements(t_series, 1);
    end

    % Define matrix A
    a11 = length(t_series);
    a12 = sum(t_series);
    a22 = sum(t_series.^2);
    A = [a11 a12; a12 a22];

    % Define vector b
    b1 = sum(meas);
    b2 = sum(t_series.*meas');
    b = [b1; b2];
    
    % solve A * [x0 v]' = b with respect to [x0 v]
    if (det(A)~=0)
        xv = linsolve(A,b);
        est_poses (k) = xv(1)+xv(2)*k;
        est_velocities (k) = xv(2);
    end
end

% stop time measurement
toc

% visualize results
figure('Name', 'vehicle position'); hold on;
plot(1:numT, true_poses(:,1), 'r*-');
plot(1:numT, measurements(:,1), 'ks');
plot(1:numT, est_poses, 'bx', 'LineWidth', 2);
xlabel('time step')
ylabel('position')
legend ('true position', 'measurement', 'estimated position');

figure('Name', 'vehicle velocity'); hold on;
plot([1 numT], [1 1], 'r-');
plot(1:numT, est_velocities, 'bx', 'LineWidth', 2);
xlabel('time step')
ylabel('velocity')
legend ('true velocity', 'estimated velocity');

squared_mean_error = analyze_residual_error(est_poses, true_poses)
