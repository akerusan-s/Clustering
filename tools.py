import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt
from random import random


def show(objects, answers, centers):
    colors = ['black']

    if len(centers):
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
    return np.array(data, dtype="f")


def load_interests(pth):
    # data with binary features
    df = read_csv(pth)

    title_mapping = {"P": 0, "C": 1, "R": 2, "I": 3}
    df['group'] = df['group'].map(title_mapping)

    return df


def drop_missing_columns(datafr, threshold):
    nan_info = datafr.isna().sum()

    res = datafr.copy()
    for i in nan_info.index:
        if nan_info[i] > threshold:
            res.drop(columns=i, inplace=True)

    return res


def dist(a, b):
    return np.linalg.norm(b - a)


def normalize(data):
    data_norm = data.copy().T
    for feat_ind in range(data.shape[1]):
        data_norm[feat_ind] = (data_norm[feat_ind] - np.min(data_norm[feat_ind])) / \
                              (np.max(data_norm[feat_ind]) - np.min(data_norm[feat_ind]))
    return data_norm.T
