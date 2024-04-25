import numpy as np
from tools import dist
import random


class KohonenClustering:

    def __init__(self, k=4):
        self.k = k
        self.centers = [0] * k

        self.best_centers = [0] * k
        self.best_loss = -1
        self.loss = -1

    def fit(self, x_data, ls=0.01):

        obj_count = x_data.shape[0]
        feat_count = x_data.shape[1]

        random_objs_indexes = np.random.choice(range(0, obj_count), size=(self.k,))
        self.centers = np.array([x_data[i] for i in random_objs_indexes])

        q = sum([min([dist(obj, center) for center in self.centers]) for obj in x_data])
        q_prev = -1

        iterations = 1
        while abs(q - q_prev) > 0.1:
            q_prev = q
            n = 1 / iterations

            rand_obj = random.choice(x_data)

            cluster_center_ind = self.predict(rand_obj)
            self.centers[cluster_center_ind] = self.centers[cluster_center_ind] + \
                                               n * (rand_obj - self.centers[cluster_center_ind])

            error = dist(self.centers[cluster_center_ind], rand_obj)
            q = (1 - ls) * q + ls * error
            q = sum([min([dist(obj, center) for center in self.centers]) for obj in x_data])

            iterations += 1

        q = sum([min([dist(obj, center) for center in self.centers]) for obj in x_data])
        self.loss = q

        if (q < self.best_loss) or (self.best_loss == -1):
            self.best_loss = q
            self.best_centers = self.centers[:]

        return self.centers

    def predict(self, sample):
        return np.argmin([np.linalg.norm(sample - center) for center in self.centers])

    def predict_best(self, sample):
        return np.argmin([np.linalg.norm(sample - center) for center in self.best_centers])

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


class Kmeans:

    def __init__(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass
