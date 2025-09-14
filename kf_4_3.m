load('data.mat');

% initial state distribution N(init_s, init_s_cov) with high uncertainty:
init_s = [0 0 0 0]';     
init_s_uncert = 100;    
init_s_cov = diag([init_s_uncert^2 init_s_uncert^2 init_s_uncert^2 init_s_uncert^2]);

% this array stores the list of estimated states (excluding the initial state).
state_history = zeros(numT, 4);

% initialize A and H
A = [ 1 0 1 0 ; 0 1 0 1 ; 0 0 1 0 ; 0 0 0 1 ];
H = [ 1 0 0 0 ; 0 1 0 0 ; 0 0 1 0; 0 0 0 1];

% initalize covariance matrices Q and R for the noise terms
uncert_trans_pos = 0.1;
uncert_trans_vel = 0.1;
Q = [ uncert_trans_pos^2 0 0 0 ; 
      0 uncert_trans_pos^2 0 0 ;
      0 0 uncert_trans_vel^2 0 ;
      0 0 0 uncert_trans_vel^2];
uncert_meas_pos = 1.0;
uncert_meas_motion = 1.0;
R = [ uncert_meas_pos^2 0 0 0;
      0 uncert_meas_pos^2 0 0;
      0 0 uncert_meas_motion^2 0;
      0 0 0 uncert_meas_motion^2];

% plotting of positions
figure ('Name', 'Positions');
hold on;
plot(true_poses(:,1), true_poses(:,2), 'r*-');
plot(measurements(:,1), measurements(:,2), 'ks');
xlabel('x position')
ylabel('y position')

state = init_s;
unc = init_s_cov;

% main loop of kalman filter
for t = 1:numT
    % prediction: 
    state_pred = A*state; 
    unc_pred = A*unc*A'+Q;

    % innovation: 
    z = [measurements(t,:) delta_motion(t,:)]'; 
    K = unc_pred*H'*inv(H*unc_pred*H'+R); % Kalman gain
    state = state_pred + K*(z-H*state_pred);
    unc = (eye(4)-K*H)*unc_pred;
    
    % store the estimated state for error analysis in 'state_history'
    state_history(t, :) = state;

    % plot estimated state and covariance after innovation
    plot (state(1), state(2), 'bx');
    error_ellipse(unc(1:2,1:2), state);
    % add relative displacements to plot
    if (t>1)
        plot ([state_history(t-1, 1) state_history(t-1, 1)+delta_motion(t, 1)], ...
              [state_history(t-1, 2) state_history(t-1, 2)+delta_motion(t, 2)], 'k:');
    end

    if (t==1)
        legend('True Position', ...
               'Measurements', ...
               'State Estimate',...
               'Displacement Measurement', ...
               'AutoUpdate','off')
    end
end

axis equal;

mean_squared_error = analyze_state_error(state_history, true_poses)

