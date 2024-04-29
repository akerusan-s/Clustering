from sklearn.metrics import silhouette_score

from tools import load_interests, drop_missing_columns, normalize
from models import *

data = load_interests("kaggle_Interests_group.csv")

data = drop_missing_columns(data, 1000)
data.drop(columns=["group"], inplace=True)
data.drop(columns=["grand_tot_interests"], inplace=True)
data.fillna(0, inplace=True)

data_norm = normalize(data.values)

range_n_clusters = [i for i in range(2, 8)]

for i, n_clusters in enumerate(range_n_clusters):

    clusterer = KohonenClustering(k=n_clusters)

    for j in range(10):
        clusterer.fit(data_norm)

    cluster_labels = clusterer.predict_list_best(data_norm)

    silhouette_avg = silhouette_score(data_norm, cluster_labels)
    print(
        "For n_clusters =",
        n_clusters,
        "The average silhouette_score is :",
        silhouette_avg,
    )
