import random
import network
import mnist_loader
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt


def check(data, sample):
    """
    Check the failed sample from the data set data for details and 
    visualize it. The sample is an element of the (i, y, yy,sc) 
    as reported by network.check()
    """
    network.Network.why(data, sample)
    mnist_loader.visualize( data[sample[0]] )
    
    
def chart(data, succ, fail) : 
    """
    Make a chart of 9 samples from the sample set succ with 
    successfull samples, and from the set fail of failed samples.
    A sample is a 4-tuple (i,y,yy,sc) as returned by network.check()
    and refers to the data set 'data' given as first argument
    """
    if len(succ) < 9 : 
        print(f"ERROR: need at least 9 successful predictions to make a chart (got only {len(succ)})")
    if len(fail) < 9 : 
        print(f"ERROR: need at least 9 wrong predictions to make a chart (got only {len(succ)})")
    plt.rcParams['figure.figsize'] = (7,14)
    fig = plt.figure()
    # plot 9 correct predicitons
    selected = random.sample(succ, 9)
    count = 1
    for sample in selected : 
        plt.subplot(6,3,count)
        plt.imshow(data[sample[0]][0].reshape(28,28), cmap='gray', interpolation='none')
        plt.title(f"Pred: {sample[2]}, Actual: {sample[1]}")
        plt.xticks([])
        plt.yticks([])  
        count += 1
    # plot 9 wrong predicitons
    selected = random.sample(fail, 9)
    for sample in selected : 
        plt.subplot(6,3,count)
        plt.imshow(data[sample[0]][0].reshape(28,28), cmap='gray', interpolation='none')
        plt.title(f"Pred: {sample[2]}, Actual: {sample[1]}")
        plt.xticks([])
        plt.yticks([])  
        count += 1    
    fig.show()    
    
