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
        # colors = [plt.cm.tab10(i / clusters) for i in range(clusters)]
        colors = [(random(), random(), random()) for i in range(clusters)]

    fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

    for dot in plot:
        ax1.scatter(x=dot[0], y=dot[1], color=colors[dot[2]], s=40)

    ax1.set_title('Results')
    # ax1.set_xlabel('serum_cholestoral')
    # ax1.set_ylabel('resting_blood_pressure')
    plt.show()
