import numpy as np

class SingleNeuronLeaky:

    def __init__(self, n_inputs: int, leak_rate: float,  seed: int = 42):
        np.random.seed(seed)
        self.x = 0
        self.theta = 0
        self.leak = leak_rate
        self.u = np.zeros([n_inputs, 1])
        self.w = np.random.uniform(low=-1, high=1, size=[1, n_inputs])

    def activate(self, input_vector):
        self.x = self.leak*np.dot(self.w, input_vector) + (1-self.leak)*self.theta
        self.theta = np.tanh(self.x)

    def step(self, input_vector):
        self.activate(input_vector)
        return self.theta