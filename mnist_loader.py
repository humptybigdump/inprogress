#### Libraries
import pickle
import gzip
import numpy as np
import matplotlib.pyplot as plt

# path to MNIST data
data_path = "./mnist.pkl.gz"


def load():
    """Return a tuple containing ``(training_data, validation_data,
    test_data)``, where each data set is a list of samples (x,y).
    In each sample, x is the 784-dimensional vector of floats 
    in the range[0..1], which represents the 28x28 grayscale pixel 
    image, and y is the corresponding label (0,...,9), i.e. the digit 
    rendered in the image x. The training data contains 50,000 samples, 
    while the validation and test data hold 10,000 samples each. 
    Check the length of the returned datasets to see if the import 
    succeeded."""
    with gzip.open(data_path, 'rb') as f:
        tr_d, va_d, te_d = pickle.load(f, encoding="latin1")
        training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
        training_data = [d for d  in zip(training_inputs, tr_d[1])]
        validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
        validation_data = [d for d in zip(validation_inputs, va_d[1])]
        test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
        test_data = [d for d in zip(test_inputs, te_d[1])]
    return (training_data, validation_data, test_data)


# visualize the given data sample(x,y( using matplotlib in ipython.
# > ipython
# > %matplotlib qt
# > from mnist_loader import visualize,load
# > (T,V,X) = load()
# > visualize(T[12])
# > visualize(X[455])
#
def visualize(sample) : 
    """Visualize a sample (x,y) using matplotlib, where x is the pixel img 
       and y the corresponding label."""
    img, val = sample
    pic = np.copy(img)
    pic.resize(28, 28)
    print(f"expected = {val}")
    plt.imshow(pic, cmap = 'gray')
    
