import matplotlib.pyplot as plt
from random import random


def get_data(pth):
    with open(pth, "r") as file:
        raw_data = file.read().split("\n")
        plot = []
        for i in raw_data:
            st = i.split(",")
            x, y = int(st[4]), int(st[3])
            plot.append([x, y, 0])
    return plot


def show_plot(plot, clusters=0):
    colors = ['black']
    if clusters != 0:
        colors = [(random(), random(), random()) for _ in range(clusters)]

    fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

    for point in plot:
        ax1.scatter(x=point[0], y=point[1], color=colors[point[2]], s=40)

    ax1.set_title('Results')
    # ax1.set_xlabel('serum_cholesterol')
    # ax1.set_ylabel('resting_blood_pressure')
    plt.show()
