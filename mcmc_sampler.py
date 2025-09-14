import numpy as np
from tqdm import tqdm

class MCMCSampler:
    
    def __init__(self, BIProblem, proposal, kernel, likelihood_only=False):
        self._parameter_dim = BIProblem.grid.size
        self._rng_samples = np.random.default_rng(seed=42)
        self._rng_kernel = np.random.default_rng(seed=43)
        self._BIProblem = BIProblem
        self._proposal = proposal
        self._kernel = kernel

        if likelihood_only:
            self._evaluate_log_prob = BIProblem.evaluate_log_likelihood
        else:
            self._evaluate_log_prob = BIProblem.evaluate_log_posterior
        
        self._num_samples = None
        self._num_burnin = None
        self._num_batches = None
        self._batch_sizes = None
        self._sample_norm = None
        self._accept_ratio = None
        self._sample_mean = None
        self._sample_var = None

    def sample(self, settings_mcmc):
        self._num_samples = int(settings_mcmc['num-samples'])
        self._num_burnin = int(settings_mcmc['num-burnin'])
        step_size = settings_mcmc['step-size']
        initial_sample = settings_mcmc['initial-sample']
        self._num_batches = settings_mcmc['num-statistics-batches']
        self._batch_sizes = self._determine_batch_sizes()

        self._sample_norm = np.zeros(self._num_samples -self._num_burnin)
        self._accept_ratio = np.zeros(self._num_batches)
        self._sample_mean = np.zeros((self._parameter_dim, self._num_batches))
        self._sample_var = np.zeros((self._parameter_dim, self._num_batches))

        current_sample = initial_sample
        current_log_prob = self._evaluate_log_prob(current_sample)

        for i in tqdm(range(self._num_samples)):
            proposed_sample = self._proposal(self._rng_samples,
                                             self._BIProblem.prior_sampling_prefactor,
                                             current_sample,
                                             step_size)
            proposal_log_prob = self._evaluate_log_prob(proposed_sample)
            next_sample, next_log_prob, is_accepted = self._kernel(self._rng_kernel,
                                                                   current_sample,
                                                                   current_log_prob,
                                                                   proposed_sample,
                                                                   proposal_log_prob)
            if i >= self._num_burnin:
                self._record_values(i, is_accepted, next_sample)

            current_sample = next_sample
            current_log_prob = next_log_prob

        return self._sample_norm, self._accept_ratio, self._sample_mean, self._sample_var
    
    def _record_values(self, iteration, is_accepted, next_sample):
        i = iteration - self._num_burnin

        if i < (self._num_batches-1) * self._batch_sizes[0]:
            batch_size = self._batch_sizes[0]
            current_batch = np.floor(i / batch_size).astype(int)
        else:
            batch_size = self._batch_sizes[1]
            current_batch = self._num_batches - 1

        j = i - current_batch * self._batch_sizes[0]
        
        self._sample_norm[i] = np.linalg.norm(next_sample)
        self._accept_ratio[current_batch] += int(is_accepted) / batch_size
        mean = np.copy(self._sample_mean[:, current_batch])
        var = np.copy(self._sample_var[:, current_batch])
        self._sample_mean[:, current_batch] = (j * mean + next_sample) / (j+1)
        self._sample_var[:, current_batch] = (j * var + (next_sample - mean)**2) / (j+1)

    def _determine_batch_sizes(self):
        num_iterations = self._num_samples-self._num_burnin
        standard_batch_size = np.ceil((num_iterations) / self._num_batches).astype(int)
        last_batch_size = num_iterations - standard_batch_size * (self._num_batches - 1)
        batch_sizes = [standard_batch_size, last_batch_size]

        return batch_sizes