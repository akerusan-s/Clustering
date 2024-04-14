import numpy as np
from tools import dist
import random


class KohonenClustering:

    def __init__(self, k=4):
        self.k = k
        self.centers = [0] * k

    def fit(self, x_data, epochs=10, n=0.1):

        obj_count = x_data.shape[0]
        feat_count = x_data.shape[1]

        # self.centers = np.array([
        #     [0 for i in range(feat_count)] for j in range(obj_count)
        # ])

        random_objs_indexes = np.random.choice(range(0, obj_count), size=(self.k,))
        self.centers = np.array([x_data[i] for i in random_objs_indexes])

        for _ in range(epochs):
            for i in range(obj_count):
                rand_obj = random.choice(x_data)
                print(rand_obj)
                cluster_center_ind = self.predict(rand_obj)
                self.centers[cluster_center_ind] = self.centers[cluster_center_ind] + \
                                                   n * (rand_obj - self.centers[cluster_center_ind])

            q = sum([min([dist(obj, center) for center in self.centers]) for obj in x_data])
            print("Epoch %d: loss %d" % (_ + 1, q))

        return self.centers

    def predict(self, sample):
        return np.argmin([np.linalg.norm(sample - center) for center in self.centers])

    def predict_list(self, samples):
        ans = np.array(
            [self.predict(obj) for obj in samples]
        )
        return ans


class Kmeans:

    def __init__(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass
