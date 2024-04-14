from numpy.linalg import norm
from numpy import array
from pandas import read_csv
import matplotlib.pyplot as plt
from random import random


def show(objects, answers, centers):
    colors = ['black']

    if centers:
        colors = [(random(), random(), random()) for _ in range(len(centers))]

    fig, (ax1) = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

    for i, obj in enumerate(objects):
        ax1.scatter(x=obj[0], y=obj[1], color=colors[answers[i]], s=40)

    for i, center in enumerate(centers):
        ax1.scatter(x=center[0], y=center[1], color=colors[i], s=160, edgecolors='black')

    plt.show()


def load_2d_data(pth):
    # data with 2 int features
    with open(pth, "r") as file:
        raw_data = file.read().split("\n")
        data = []
        for i in raw_data:
            st = i.split(",")
            x, y = int(st[4]), int(st[3])  # serum_cholesterol and resting_blood_pressure
            data.append([x, y])
    return array(data)


def load_interests(pth):
    # data with binary features
    df = read_csv(pth)
    return df


def dist(a, b):
    return norm(b - a)
