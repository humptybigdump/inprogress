load('data_simple.mat');

% define initial parameters:
numParticles = 500; % number of particles to use
init_s_uncert = 4; % initial state uncertainty
init_s_cov = diag([init_s_uncert^2 init_s_uncert^2]);

% initialization of particles: 
particles = pf_init(numParticles, init_s_cov);

% create a cell in which we will save the history of the particles
particle_sets = cell(numT + 1, 3);
particle_sets{1, 3} = particles;

% this array stores the list of estimated states (excluding the initial state). 
state_history = zeros(numT, 2);

% main loop of particle filter
for t = 1:numT
    particles_predicted = pf_predict(particles, delta_motion(t,:), noise_system);
    particles_updated =   pf_update(particles_predicted, measurements(t,:), noise_meas);
    particles_resampled = pf_resample(particles_updated);
    particles = particles_resampled;
    
    % store the history of the current particle filter iteration
    particle_sets(t+1,:) = {particles_predicted, particles_updated, particles_resampled};    

    % store the estimated state after resampling for error analysis in 'state_history'
    state_history (t,:) = compute_particle_statistics(particles);
end

% analyze the estimation error
mean_error = analyze_state_error(state_history, true_poses);

% simulate the particle filter
simulate_particle_filter(particle_sets, true_poses);
