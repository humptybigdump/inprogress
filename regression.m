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

% We will incrementally build A and b
A = [ 0 0 ; 0 0 ];
b = [ 0 ; 0 ];

% Implement regression here
for k=1:numT

    A = A + [ 1 k; k k*k];
    b = b + [ measurements(k,1); k*measurements(k,1) ];

    if (k>w) 
        % remove contributions of measurements which have left the sliding
        % window
        A = A - [ 1 k-w; k-w (k-w)*(k-w)];
        b = b - [ measurements(k-w,1); (k-w)*measurements(k-w,1) ];
    end
    
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
