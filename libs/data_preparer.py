import matplotlib.pyplot as plt
from random import random, randint


def get_data(pth):
    with open(pth, "r") as file:
        raw_data = file.read().split("\n")
        plot = []
        for i in raw_data:
            st = i.split(",")
            x, y = int(st[4]), int(st[3])
            plot.append([x, y, 0])
    return plot


def get_big_data(pth):
    f = open("data/big_data_prepared.txt", "w")
    with open(pth, "r") as file:
        raw_data = file.read().split("\n")
        plot = []
        for i in raw_data:
            f.write(i + "\n")
            st = i.split(",")
            x, y = int(st[4]), int(st[3])
            plot.append([x, y, 0])
            for j in range(4):
                st[4], st[3] = randint(x-5, x+5), randint(y-5, y+5)
                plot.append([st[4], st[3], 0])
                st[4], st[3] = str(st[4]), str(st[3])
                f.write(",".join(st) + "\n")
    f.close()

    return plot


def show_plot(plot, clusters=0, name="Results"):
    colors = ['black']
    if clusters != 0:
        colors = [(random(), random(), random()) for _ in range(clusters)]

    fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

    for point in plot:
        ax1.scatter(x=point[0], y=point[1], color=colors[point[2]], s=40)

    ax1.set_title(name)
    # ax1.set_xlabel('serum_cholesterol')
    # ax1.set_ylabel('resting_blood_pressure')
    plt.show()
