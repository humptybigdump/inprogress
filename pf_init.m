function particles = pf_init (numParticles, init_s_cov)
% Create initial set of numParticles particles around 0 with random 
% deviation given by the covariance matrix init_s_cov.
% The weight of each particle is 1/numParticles. 
% Each particle should contain in its first column its weight and the 
% other two columns its state.

particles = zeros(numParticles, 3);

% the initial weight of each particle:
particles (:,1) = % ...
% the state of each particle is drawn from a multivariate normal
% distribution with mean (0, 0) ann covariance init_s_cov
particles (:,2:3) = % ...

end
