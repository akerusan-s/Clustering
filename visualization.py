import seaborn as sns

import matplotlib.pyplot as plt


def show_chart(dataframe, clusters, objects, features):
    # dataframe - pandas.DataFrame with columns
    # 'Index' - criteria
    # 'Value' - numeric
    # 'Method' - method of clustering

    sns.barplot(
        x='Index',
        y='Value',
        data=dataframe,
        hue='Method',
    )

    plt.title("Clustering Results\n" 
              f"(clusters={clusters}, "
              f"objects={objects}, "
              f"features={features})")

    plt.show()
