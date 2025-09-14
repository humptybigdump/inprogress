import numpy as np
import scipy as sp

class ODEInverseProblem:
    _step_size_fine = 1e-4
    _cov_stabilization_factor = 1e-3
     
    def __init__(self, settings_ode, settings_inverse):
        self._start_time = settings_ode['start-time']
        self._end_time = settings_ode['end-time']
        self._step_size = settings_ode['time-step-size']
        self._initial_solution = settings_ode['initial-condition']
        self._solver = settings_ode['solver']

        self._prior_mean_function = settings_inverse['prior-mean']
        self._prior_var = settings_inverse['prior-variance']
        self._prior_corr_length = settings_inverse['prior-correlation-length']
        self._param_function = settings_inverse['exact-solution']
        self._num_data_points = settings_inverse['num-data-points']
        self._data_noise_var = settings_inverse['data-noise-variance']

        self._time_grid = np.arange(self._start_time,
                                    self._end_time + self._step_size,
                                    self._step_size)
        self._time_grid_fine = np.arange(self._start_time,
                                         self._end_time + self._step_size_fine,
                                         self._step_size_fine)

        self._prior_mean = self._prior_mean_function(self._time_grid)
        self._param_exact_solution = self._param_function(self._time_grid)
        self._param_exact_solution_fine = self._param_function(self._time_grid_fine)
        self._forward_exact_solution = self.solve_forward(self._param_exact_solution)
        self._forward_exact_solution_fine = self.solve_forward(self._param_exact_solution_fine,
                                                               self._step_size_fine,
                                                               self._time_grid_fine)
        
        self._prior_cov_matrix, \
        self._prior_precision_matrix, \
        self._prior_sampling_prefactor = self._initialize_prior()
        self._data_times, self._data_values = self._generate_data()
        self._data_projection_matrix = self._assemble_projection_matrix()
        self._integration_matrix = self._assemble_integration_matrix()

    def evaluate_log_prior(self, parameter_candidate):
        parameter_diff = parameter_candidate - self._prior_mean
        log_probability = - 0.5 * parameter_diff.T \
                                  @ self._integration_matrix \
                                  @ self._prior_precision_matrix \
                                  @ parameter_diff
        
        return log_probability

    def evaluate_log_likelihood(self, parameter_candidate):
        fwd_solution = self.solve_forward(parameter_candidate)
        projected_fwd_solution = self._data_projection_matrix @ fwd_solution
        log_probability = - 0.5 / self._data_noise_var \
                        * np.linalg.norm(projected_fwd_solution - self._data_values) ** 2

        return log_probability
    
    def evaluate_log_posterior(self, parameter_candidate):
        log_probability = self.evaluate_log_prior(parameter_candidate) \
                        + self.evaluate_log_likelihood(parameter_candidate)
        
        return log_probability
    
    def solve_forward(self, param_array, step_size=None, time_grid=None):
        if step_size is None:
            step_size = self._step_size
        if time_grid is None:
            time_grid = self._time_grid

        solution_array = np.zeros(time_grid.shape)
        solution_array[0] = self._initial_solution

        match self._solver:
            case "explicit-euler":
                solution_array = self._solve_explicit_euler(param_array, solution_array, step_size)
            case "implicit-euler":
                solution_array = self._solve_implicit_euler(param_array, solution_array, step_size)
            case _:
                raise NotImplementedError('The specified ODE solver is not implemented.')
            
        return solution_array
    
    def _solve_explicit_euler(self, param_array, solution_array, step_size):
        for i, param in enumerate(param_array[:-1]):
            solution_array[i+1] = solution_array[i] * (1 + step_size * param)

        return solution_array
    
    def _solve_implicit_euler(self, param_array, solution_array, step_size):
        for i, param in enumerate(param_array[1:]):
            solution_array[i+1] = solution_array[i] * 1 / (1 + step_size * param)

        return solution_array
    
    def _generate_data(self):
        rng = np.random.default_rng(42)
        data_time_inds = rng.integers(low=0,
                                      high=self._time_grid_fine.size-2,
                                      size=self._num_data_points)
        data_times = self._time_grid_fine[data_time_inds]
        data_noise_increments = rng.normal(loc=0,
                                           scale=np.sqrt(self._data_noise_var),
                                           size=self._num_data_points)
        data_values = self._forward_exact_solution_fine[data_time_inds] + data_noise_increments
        
        return data_times, data_values
    
    def _assemble_projection_matrix(self):
        lower_inds = np.floor(self._data_times/self._step_size).astype(int)
        interp_param = (self._data_times - self._time_grid[lower_inds]) / self._step_size
        projection_matrix = np.zeros((self._data_times.size, self._time_grid.size))
        for i, j in enumerate(lower_inds):
            projection_matrix[i, j] = 1 - interp_param[i]
            projection_matrix[i, j+1] = interp_param[i]
        projection_matrix = sp.sparse.bsr_array(projection_matrix)
        
        return projection_matrix
    
    def _initialize_prior(self):
        cov_matrix = self._assemble_cov_matrix_squared_exponential()
        precision_matrix = np.linalg.inv(cov_matrix)
        sampling_prefactor = np.linalg.cholesky(cov_matrix)

        return cov_matrix, precision_matrix, sampling_prefactor
    
    def _assemble_integration_matrix(self):
        integration_matrix = np.identity(self._time_grid.size)
        integration_matrix [0, 0] = integration_matrix [-1, -1] = 0.5
        integration_matrix *= self._step_size
        integration_matrix = sp.sparse.bsr_array(integration_matrix)

        return integration_matrix
    
    def _assemble_cov_matrix_squared_exponential(self):
        diff_mat = self._time_grid[:, None] - self._time_grid[None, :]
        cov_matrix = self._cov_stabilization_factor * np.identity(self._time_grid.size) \
                   + self._prior_var * np.exp(- 0.5 / self._prior_corr_length **2
                                              * np.square(diff_mat))
        
        return cov_matrix

    @property
    def grid(self):
        return self._time_grid
    
    @property
    def grid_fine(self):
        return self._time_grid_fine
    
    @property
    def param_exact_solution(self):
        return self._param_exact_solution
    
    @property
    def param_exact_solution_fine(self):
        return self._param_exact_solution_fine
    
    @property
    def forward_exact_solution(self):
        return self._forward_exact_solution

    @property
    def forward_exact_solution_fine(self):
        return self._forward_exact_solution_fine
    
    @property
    def prior_mean(self):
        return self._prior_mean
    
    @property
    def prior_cov(self):
        return self._prior_cov_matrix
    
    @property
    def prior_precision(self):
        return self._prior_precision_matrix
    
    @property
    def prior_sampling_prefactor(self):
        return self._prior_sampling_prefactor
    
    @property
    def data(self):
        return self._data_times, self._data_values
    
    @property
    def data_projection_matrix(self):
        return self._data_projection_matrix