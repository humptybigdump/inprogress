# -----------------------------------------------------------------------
# imports
# -----------------------------------------------------------------------
# 
# # imports for array-handling and plotting
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt

# let's keep our keras backend tensorflow quiet
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
# for testing on CPU
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# keras imports for the dataset and building our neural network
from keras.datasets import mnist
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation
from keras.utils import to_categorical


# -----------------------------------------------------------------------
# load data
# -----------------------------------------------------------------------

def load_data(quiet = True):
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # reshape to 768-component vector with float [0,1] grey level
    X_train  = X_train.reshape(60000, 784)
    X_train  = X_train.astype('float32')
    X_train /= 255
    X_test   = X_test.reshape(10000, 784)
    X_test  = X_test.astype('float32')
    X_test /= 255

    # output lavels are digits [0...9] -> convert to one-hot encoding
    num_classes = 10
    Y_train = to_categorical(y_train, num_classes)
    Y_test  = to_categorical(y_test, num_classes)
    if not quiet : 
        print(f"loaded {len(X_train)} samples of training data, and {len(X_test)} samples of test data")
        print(f"input has shape {X_train.shape}, output has shape {Y_train.shape}")
    return ((X_train, Y_train), (X_test, Y_test))


# -----------------------------------------------------------------------
# train network
# -----------------------------------------------------------------------    

def train(plot_metrics = False):
    (X_train, Y_train), (X_test, Y_test) = load_data()

    # build the network: sequence of layers
    # input: 784 normalized real numbers
    # layer 1: fully connected, 512 neurons, relu activation, 0.2 dropout
    # layer 2: fully connected, 512 neurons, relu activation, 0.2 dropout
    # layer 3: fully connected 10 neurons, softmax activation, output 
    model = Sequential()
    #
    # model.add(Dense(15, input_shape=(784,)))
    # model.add(Activation('relu'))
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    #
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    #
    model.add(Dense(10))
    model.add(Activation('softmax'))

    # compile network to binary code
    model.compile(loss='categorical_crossentropy', metrics = ['accuracy'], optimizer = 'adam')

    # train the model and save metrics in history
    history = model.fit(X_train, Y_train, batch_size=128, epochs=20, verbose=2, validation_data=(X_test, Y_test))

    # save the trained model
    model_name = 'keras_mnist.h5'
    model_path = os.path.join(os.getcwd(), model_name)
    model.save(model_path)
    print(f'Saved trained model at {model_path}')

    # plot training metrics if enabled
    if plot_metrics : 
        fig = plt.figure()
        plt.subplot(2,1,1)
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='lower right')
        plt.subplot(2,1,2)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper right')
        plt.tight_layout()
        fig.show()


# -----------------------------------------------------------------------
# load trained model
# -----------------------------------------------------------------------

def load():
    mnist_model = load_model("keras_mnist.h5")
    return mnist_model


# -----------------------------------------------------------------------
# evaluate trainted model on test data
# -----------------------------------------------------------------------

def evaluate(model) :
    _,(X_test, Y_test) = load_data()
    metrics = model.evaluate(X_test, Y_test, verbose=2)
    print(f"Test loss    : {metrics[0]}")
    print(f"Test accuracy: {metrics[1]}")


# -----------------------------------------------------------------------
# visualize 9 correct, and 9 false predictions
# -----------------------------------------------------------------------

def visualize(model):
    _,(X_test, Y_test) = load_data() 
    predicted = np.argmax(model.predict(X_test), axis=-1)
    correct  = np.argmax(Y_test, axis=1)
    success  = np.nonzero(predicted == correct)[0]
    fail     = np.nonzero(predicted != correct)[0]
    print(f"classified correctly  : {len(success)}")
    print(f"classified incorrectly: {len(fail)}")
    plt.rcParams['figure.figsize'] = (7,14)
    fig = plt.figure()
    # plot 9 correct predicitons
    for i, idx in enumerate(success[:9]):
        plt.subplot(6,3,i+1)
        plt.imshow(X_test[idx].reshape(28,28), cmap='gray', interpolation='none')
        plt.title(f"Pred: {predicted[idx]}, Actual: {correct[idx]}")
        plt.xticks([])
        plt.yticks([])    
    for i, idx in enumerate(fail[:9]):
        plt.subplot(6,3,i+10)
        plt.imshow(X_test[idx].reshape(28,28), cmap='gray', interpolation='none')
        plt.title(f"Pred: {predicted[idx]}, Actual: {correct[idx]}")
        plt.xticks([])
        plt.yticks([])
    fig.show()


# -----------------------------------------------------------------------
# set main() entry point to train()
# -----------------------------------------------------------------------

def main():
    train()

if __name__ == '__main__':
    main()
