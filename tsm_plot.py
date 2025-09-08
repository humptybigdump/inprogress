import operator
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def plot(points, path: list):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.plot(x, y, 'co')

    count = len(path)
    for _ in range(1, count):
        i = path[_ - 1]
        j = path[_]
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)
    ie = path[count-1]
    ia = path[0]
    # plt.arrow(x[ie], y[ie], x[ia] - x[ie], y[ia] - y[ie], color='r', length_includes_head=True)
    plt.xlim(0, 1)
    plt.ylim(0, 1) 
    
    plt.show(block=True)
