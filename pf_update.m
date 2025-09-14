function particles_upd = pf_update(particles, measurement, noise_meas)
% Initialize array to save the new particles
particles_upd = zeros(size(particles));

num_particles = size(particles, 1);

% the state variables are kept
particles_upd(:,2:3) = % ...

% update the weights based on the likelihood of the given observation
for i = 1:num_particles 
particles_upd(i,1) = % ...
end
end

