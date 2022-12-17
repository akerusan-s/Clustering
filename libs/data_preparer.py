import matplotlib.pyplot as plt
from random import random


def get_data(pth):
    """ Return parsing data from the data-set (path to) """
    with open(pth, "r") as file:
        raw_data = file.read().split("\n")
        plot = []
        for i in raw_data:
            st = i.split(",")
            x, y = int(st[4]), int(st[3])  # serum_cholesterol and resting_blood_pressure
            plot.append([x, y, 0])  # x, y and id of cluster
    return plot


def show_plot(plot, clusters=0, name="Results"):
    """ Shows a plot of points labeled with id's of clusters """
    colors = ['black']

    # colors for every individual cluster id
    if clusters != 0:
        colors = [(random(), random(), random()) for _ in range(clusters)]

    fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

    for point in plot:
        ax1.scatter(x=point[0], y=point[1], color=colors[point[2]], s=40)

    ax1.set_title(name)
    # ax1.set_xlabel('serum_cholesterol')
    # ax1.set_ylabel('resting_blood_pressure')
    plt.show()
