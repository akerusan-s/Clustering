import pandas as pd

from tools import *
from models import KohonenClustering, Kmeans
from metrics import *
from visualization import show_chart


# 2d data

# data = normalize(load_2d_data("2d_data.txt"))
# print(data)
#
# khn = KohonenClustering(k=4)
#
# for tet in range(0, 10):
#     khn.fit(data)
#
# ans = khn.predict_list_best(data)
# show(data, ans, khn.best_centers)


# interests data
data = load_interests("kaggle_Interests_group.csv")

data = drop_missing_columns(data, 1000)                     # del features with 6000 Nulls
data.drop(columns=["group"], inplace=True)                  # categorical
data.drop(columns=["grand_tot_interests"], inplace=True)    # linear-depend
data.fillna(0, inplace=True)                                # Null fill by 0


print("Первые пять объектов (примеры):")
print(data.head())

data_norm = normalize(data.values)                  # basic normalization

np.random.shuffle(data_norm)                        # shuffle the dataset
data_norm = data_norm[:len(data_norm) // 2, :]      # use the half of dataset

print("Размер данных (объекты, признаки)")
print(data_norm.shape)

training_count = 10                                 # retraining quantity
K = 3                                               # clusters amount

print()
print("Результаты, %d запусков" % (training_count,), end="\n\n")

# K-means Clustering
print("Кластеризация K-means")

kms = Kmeans(k=K)

kms.fit(data_norm)
print("Loss: %.3f" % (kms.loss,))
# print("Min Loss: %.3f" % (kms.best_loss,))

# Kohonen Clustering
print("Кластеризация сетью Кохонена")

khn = KohonenClustering(k=K)

for i in range(training_count):
    khn.fit(data_norm)
    print("Loss: %.3f" % (khn.loss,))

print("Min Loss: %.3f" % (khn.best_loss,))

########

# Criteria of clustering
print("\nПрименение критериев оценки качества")

X = data_norm

# K-means
kms_Y = kms.fit_predict(X)
kms_centers = kms.best_centers

# Kohonen
khn_Y = khn.predict_list_best(X)
khn_centers = khn.best_centers

########

# Davies-Bouldin
# K-means
db_kms = davies_bouldin_index(
    X,
    kms_Y,
    kms_centers
)
# Kohonen
db_khn = davies_bouldin_index(
    X,
    khn_Y,
    khn_centers
)

print("Критерий Дэвиса-Болдуина (меньше - лучше):")
print("K-means: %.3f     Кохонен: %.3f" % (db_kms, db_khn))

# Silhouette
# K-means
sil_kms = silhouette(
    X,
    kms_Y,
    kms_centers
)
# Kohonen
sil_khn = silhouette(
    X,
    khn_Y,
    khn_centers
)

print("Силуэт (ближе к 1 - лучше):")
print("K-means: %.3f     Кохонен: %.3f" % (sil_kms, sil_khn))

# Dunn Index
# K-means
dn_kms = dunn_index(
    X,
    kms_Y,
    kms_centers
)
# Kohonen
dn_khn = dunn_index(
    X,
    khn_Y,
    khn_centers
)

print("Индекс Данна (больше - лучше):")
print("K-means: %.3f     Кохонен: %.3f" % (dn_kms, dn_khn))

# Cohesion
# K-means
coh_kms = cohesion(
    X,
    kms_Y,
    kms_centers
)
# Kohonen
coh_khn = cohesion(
    X,
    khn_Y,
    khn_centers
)

print("Компактность (меньше - лучше):")
print("K-means: %.3f     Кохонен: %.3f" % (coh_kms, coh_khn))

# Separation
# K-means
sep_kms = separation(
    X,
    kms_Y,
    kms_centers
)
# Kohonen
sep_khn = separation(
    X,
    khn_Y,
    khn_centers
)

print("Отделимость (больше - лучше):")
print("K-means: %.3f     Кохонен: %.3f" % (sep_kms, sep_khn))

##############

# Visualization of statistics

statistic = pd.DataFrame(
    data={
        "Value": [dn_kms, sep_kms, sil_kms, coh_kms,
                  db_kms, dn_khn, sep_khn, sil_khn,
                  coh_khn, db_khn],
        "Method": [
            "K-means",
            "K-means",
            "K-means",
            "K-means",
            "K-means",
            "Kohonen Net",
            "Kohonen Net",
            "Kohonen Net",
            "Kohonen Net",
            "Kohonen Net",
        ],
        "Index": [
            "Dunn Index\n (to max)",
            "Separation\n (to max)",
            "Silhouette\n (to max)",
            "Cohesion\n (to min)",
            "Davies-Bouldin\n (to min)",
            "Dunn Index\n (to max)",
            "Separation\n (to max)",
            "Silhouette\n (to max)",
            "Cohesion\n (to min)",
            "Davies-Bouldin\n (to min)",
        ]
    }
)

print("\nДанные в виде таблицы\n")
print(statistic)

# Bar Chart
show_chart(statistic,
           clusters=K,
           objects=data_norm.shape[0],
           features=data_norm.shape[1])
