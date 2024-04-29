import numpy as np

from sklearn.metrics import silhouette_score

from tools import dist


def cohesion(data, answers, centers):
    # Компактность - критерий внутрикластерного расстояния
    # Чем меньше - тем лучше

    coh = 0
    f = 0

    for i in range(len(data)):
        for j in range(i):
            if answers[i] == answers[j]:
                coh += dist(data[i], data[j])
                f += 1

    coh /= f

    return coh


def separation(data, answers, centers):
    # Отделимость - критерий межкластерного расстояния
    # Чем больше - тем лучше

    sep = 0
    f = 0

    for i in range(len(data)):
        for j in range(i):
            if answers[i] != answers[j]:
                sep += dist(data[i], data[j])
                f += 1

    sep /= f

    return sep


def dunn_index(data, answers, centers):
    # Индекс Данна - межкластерное делить на диаметр (gD41)
    # Больше - лучше

    clusters = [[] for i in range(len(centers))]
    for j in range(len(centers)):
        for i in range(len(data)):
            if answers[i] == j:
                clusters[j].append(data[i])

    clusters_mean = [
        sum(cluster) / len(cluster) for cluster in clusters
    ]

    delt = 0
    for c in clusters:
        for i in range(len(c)):
            for j in range(i):
                delt = max(dist(data[i], data[j]), delt)

    delt4 = 100000000000

    for c_k in range(len(clusters)):
        for c_l in range(c_k):
            delt4 = min(np.linalg.norm(clusters_mean[c_k] - clusters_mean[c_l]),
                        delt4)

    return delt4 / delt


def silhouette(data, answers, centers):
    # Силуэт - схожесть объекта со своими кластером по отношению к другим
    # чем ближе к 1 - тем лучше

    sil = silhouette_score(data, answers)

    return sil


def davies_bouldin_index(data, answers, centers):
    # Индекс Дэвиcа-Болдуина - вычисляет компактность как расстояние
    # от объектов кластера до их центроидов, а отделимость - как расстояние
    # между центроидами (меньше - лучше)

    clusters = [[] for i in range(len(centers))]
    for j in range(len(centers)):
        for i in range(len(data)):
            if answers[i] == j:
                clusters[j].append(data[i])

    clusters_mean = [
        sum(cluster) / len(cluster) for cluster in clusters
    ]

    s = [
        1 / len(clusters[k]) *
        sum([
            np.linalg.norm(
                x - clusters_mean[k]
            )
            for x in clusters[k]
        ]) for k in range(len(centers))
    ]

    db = 1 / len(centers) * sum([
        (max([
            s[k] + s[l]
            /
            np.linalg.norm(
                clusters_mean[k] - clusters_mean[l]
            ) if k != l else 0
            for l, cluster_l in enumerate(clusters)
         ]))
        for k, cluster_k in enumerate(clusters)
    ])

    return db
