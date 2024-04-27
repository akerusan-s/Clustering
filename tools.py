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


def dist_squared(a, b):
    return np.dot(b - a, b - a)


def normalize(data):
    data_norm = data.copy().T
    for feat_ind in range(data.shape[1]):
        data_norm[feat_ind] = (data_norm[feat_ind] - np.min(data_norm[feat_ind])) / \
                              (np.max(data_norm[feat_ind]) - np.min(data_norm[feat_ind]))
    return data_norm.T


def choose_farthest_objs(data, n=2):
    dist_matrix = np.array([[dist_squared(x, y) for x in data] for y in data])

    # distances between the object itself
    for i in range(len(data)):
        dist_matrix[i][i] = 1000000000000

    # 2 farthest
    min_obj_ind = np.argmin(dist_matrix)
    row = min_obj_ind // len(data)
    col = min_obj_ind % len(data)

    objs = [row, col]

    for i in range(n - 2):

        # farthest point to the closest already chosen one
        obj_matrix = np.array([min([dist(obj, center) for center in objs]) for obj in data])
        objs.append(np.argmax(obj_matrix))

    return np.array([data[ind] for ind in objs])
