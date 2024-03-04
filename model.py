import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib.ticker as plticker
import csv


def getArraysFromCSV(pathToCSV):
    points = []
    labels = []

    with open(pathToCSV, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if(row[0] == 'p'):
                points.append([float(row[1]), float(row[2]), float(row[3])])
                labels.append("{}, {}, {}".format(row[1],row[2],row[3]))
            else:
                points.append([float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6])])
                labels.append("{}, {}, {}: {}, {}, {}".format(row[1], row[2], row[3], row[4], row[5], row[6]))
    
    return points, labels

def configurePlot():
    fig = plt.figure()
    plt.subplots_adjust(left=0.001,
                        bottom=0.001, 
                        right=0.97, 
                        top=0.97, 
                        wspace=0.4, 
                        hspace=0.4)
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_xlabel('X', size=17).set_color('red')
    ax.set_ylabel('Y', size=17).set_color('red')
    ax.set_zlabel('Z', size=17).set_color('red')
    plt.title("Points and Vectors")
    # ax.xaxis.set_major_locator(plticker.MultipleLocator(.1))
    # ax.yaxis.set_major_locator(plticker.MultipleLocator(.1))
    # ax.zaxis.set_major_locator(plticker.MultipleLocator(.1))
    return fig, ax

def plotPoints(points, ax):
    for point in points:
        if (len(point) == 3):
            ax.scatter(point[0], point[1], point[2])
        else:
            ax.quiver(point[0], point[1], point[2], point[3], point[4], point[5], length=.2)
    
def annotatePoints(points, labels):
    # global labels_and_points
    labels_and_points = []

    for txt, pointData in zip(labels, points):
        x2, y2, _ = proj3d.proj_transform(pointData[0],pointData[1],pointData[2], ax.get_proj())
        label = plt.annotate(
            txt, xy = (x2, y2), xytext = (-20, 20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=.1'))
        labels_and_points.append((label, pointData))

    return labels_and_points

def update_position(e, labels_and_points, fig):
    for label, pointData in labels_and_points:
        x2, y2, _ = proj3d.proj_transform(pointData[0], pointData[1], pointData[2], ax.get_proj())
        label.xy = x2,y2
        label.update_positions(fig.canvas.renderer)
    fig.canvas.draw()


if __name__ == '__main__':
    fig, ax = configurePlot()
    points, labels = getArraysFromCSV('config.csv')
    plotPoints(points, ax)
    labels_and_points = annotatePoints(points, labels)

    fig.canvas.mpl_connect('motion_notify_event', lambda event: update_position(event, labels_and_points, fig))
    plt.show()