import numpy as np
import random

from src.tools import dist_squared, dist, choose_farthest_objs
from sklearn.cluster import KMeans


class KohonenClustering:

    def __init__(self, k=4, init_type=""):
        self.k = k
        self.init_type = init_type

        self.centers = None
        self.loss = -1
        self.iterations = -1
        self.wins = None

        self.best_centers = None
        self.best_loss = -1
        self.best_wins = None

    def fit(self, x_data, ls=0.001):

        obj_count = x_data.shape[0]
        feat_count = x_data.shape[1]

        self.wins = [0 for i in range(self.k)]

        if self.init_type == "farthest":
            self.centers = choose_farthest_objs(x_data, self.k)
        else:
            random_objs_indexes = np.random.choice(range(0, obj_count), size=(self.k,))
            self.centers = np.array([x_data[i] for i in random_objs_indexes])

        q = 1 / 2 * sum([min([dist_squared(obj, center) for center in self.centers]) for obj in x_data])
        q_prev = -1

        iterations = 1
        while abs((q - q_prev) / q_prev) > 0.00001:
            q_prev = q
            n = 1 / iterations

            rand_obj = random.choice(x_data)

            # classic
            cluster_center_ind = self.predict(rand_obj)
            self.centers[cluster_center_ind] = self.centers[cluster_center_ind] + \
                n * (rand_obj - self.centers[cluster_center_ind])

            # soft WTA
            # b = iterations
            #
            # for center_ind in range(self.k):
            #     if center_ind != cluster_center_ind:
            #         self.centers[center_ind] = self.centers[center_ind] + \
            #             n * (rand_obj - self.centers[center_ind]) * \
            #             np.exp(-1 * b * dist_squared(rand_obj,
            #                                          self.centers[center_ind]))

            # conscience WTA
            self.wins[cluster_center_ind] += 1

            error = dist_squared(self.centers[cluster_center_ind], rand_obj)
            q = (1 - ls) * q + ls * error
            iterations += 1

        q = 1 / 2 * sum([min([dist_squared(obj, center) for center in self.centers]) for obj in x_data])
        self.loss = q
        self.iterations = iterations

        if (q < self.best_loss) or (self.best_loss == -1):
            self.best_loss = q
            self.best_centers = self.centers[:]
            self.best_wins = self.wins[:]

        return self.centers

    def predict(self, sample):
        # return np.argmin([dist(sample, self.centers[center_index])
        #                   for center_index in range(self.k)])
        return np.argmin([self.wins[center_index] * dist(sample, self.centers[center_index])
                          for center_index in range(self.k)])

    def predict_best(self, sample):
        # return np.argmin([dist(sample, self.best_centers[center_index])
        #                   for center_index in range(self.k)])
        return np.argmin([self.best_wins[center_index] * dist(sample, self.best_centers[center_index])
                          for center_index in range(self.k)])

    def predict_list(self, samples):
        ans = np.array(
            [self.predict(obj) for obj in samples]
        )
        return ans

    def predict_list_best(self, samples):
        ans = np.array(
            [self.predict_best(obj) for obj in samples]
        )
        return ans

    def fit_predict(self, data):
        self.fit(data)
        ans = self.predict_list(data)
        return ans


class Kmeans:

    def __init__(self, k):
        self.k = k

        self.best_centers = None
        self.best_loss = -1
        self.loss = -1

        self.clf = KMeans(n_clusters=k, init="random", n_init=1)
        self.centers = None

    def fit(self, data):
        self.clf.fit(data)
        self.centers = self.clf.cluster_centers_
        self.loss = 1 / 2 * self.clf.inertia_

        if (self.loss < self.best_loss) or (self.best_loss == -1):
            self.best_centers = self.centers[:]
            self.best_loss = self.loss

    def predict(self, obj):
        return self.clf.predict(obj)

    def fit_predict(self, data):
        ans = self.clf.fit_predict(data)
        self.centers = self.clf.cluster_centers_
        self.loss = 1 / 2 * self.clf.inertia_

        if (self.loss < self.best_loss) or (self.best_loss == -1):
            self.best_centers = self.centers[:]
            self.best_loss = self.loss

        return ans
