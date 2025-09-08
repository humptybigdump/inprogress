#! /usr/bin/python

import random
import numpy as np


class Network(object):

    def __init__(self, sizes):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network. 
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def vector10(self, j):
        """Return a 10-dimensional unit vector with a 1.0 in the jth
        position and zeroes elsewhere (1-hot).""" 
        e = np.zeros((10, 1))
        e[j] = 1.0
        return e
    
    
    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a


    def SGD(self, training_data, epochs, mini_batch_size, eta,
            validation_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent.  The ``training_data`` is a list of tuples
        ``(x, y)`` representing the training inputs (pixel data) and 
        the desired outputs (digits).  If ``validation_data`` is 
        provided then the network will be evaluated against the 
        validation data after each epoch, and partial progress is 
        printed out. This is slow, but useful for tracking progress"""
        # convert the expected labels to 10-dimensional 1-hot vectors
        # to simplify the error compuation and backpropagation
        tdata = [(x, self.vector10(y)) for (x,y) in training_data]
        if validation_data: 
            n_test = len(validation_data)
        n = len(tdata)
        for j in range(epochs):
            random.shuffle(tdata)
            mini_batches = [tdata[k:k+mini_batch_size] for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if validation_data:
                succ = self.evaluate(validation_data) / n_test
                print(f"Epoch {j}: {succ:.4f}")
            else:
                print("Epoch {j} completed")


    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)`` with the pixel
        data in ``x`` and the expected output (as 10-dimensional one-hot
        vector) in ``y``, and ``eta`` is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]


    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function E_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Here, l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # standard scheme to take advantage of the fact that Python 
        # can use negative indices in lists.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)


    def evaluate(self, dataset):
        """Return the number of trial inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in dataset]
        return sum(int(x == y) for (x, y) in results)


    def check(self, dataset) :
        """Return two lists of 4-tuples (i, y, yy,sc) such that
            i  = index of a sample in dataset on which the network failed
            y  = the expected ouptut (digit)
            yy = the predicted output (digit)
            sc = the 10-component score vector for the sample
           The first list contains the successful samples (with y==yy), 
           the second list the samples that failed (y != yy)
           """
        idx = 0
        succ = []
        fail = []
        while idx < len(dataset) : 
            (x , y) = dataset[idx]
            sc = self.feedforward(x)
            yy = np.argmax(sc)
            sample = (idx, y, yy, sc)
            succ.append(sample) if y == yy else fail.append(sample)
            idx += 1
        return succ, fail
    
    
    @staticmethod
    def why(self, sample) :
        """Pretty prints the detailed findings for a failed sample (as returned in 
           the fail list by check() above"""
        print(f"\ndatat set index : {sample[0]}")
        print(f"expected digit  : {sample[1]}")
        print(f"recognized digit: {sample[2]}")
        print(f"scores per digit: ")
        score = sample[3]
        score /= sum(score)
        for d in range(0, 10): 
            p = score[d][0] * 100
            print(f"  {d} : {p:.4f}%")     
        
        
    def xeval(self, dataset, idx):
        """Return the computed and expected result for item 
           #``idx`` in the given ``dataset``"""
        (x,y) = dataset[idx]
        yy = np.argmax(self.feedforward(x))
        print(f"expcted = {y}, computed = {yy}")
        
        
    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives dE_x / da for the 
           output activations."""
        return (output_activations-y)


#### Neuron activation
def sigmoid(z):
    """The sigmoid neuron activation function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid activation function."""
    return sigmoid(z)*(1-sigmoid(z))
