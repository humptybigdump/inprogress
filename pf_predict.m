function particles_pred = pf_predict(particles, delta_motion, noise_system)
% Initialize array to save the new particles
particles_pred = zeros(size(particles));

% number of particles
num_particles = size(particles, 1);

% keep the weights during prediction
particles_pred(:,1) = % ...
% apply transition model based on delta_motion
particles_pred(:,2:3) = % ...
end

