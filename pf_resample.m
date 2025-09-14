function particles_resampled = pf_resample(particles)
% Initialize array to save the new particles
particles_resampled = zeros(size(particles));

num_particles = size(particles, 1);

% normalize all weights such that the sum up to 1
normalized_weights = % ...

% reset all weights to 1/num_particles
particles_resampled(:,1) = % ...

% draw samples according to normalized weights
% ...

end

