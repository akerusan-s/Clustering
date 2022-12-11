from main import Dot


def ev_dist(dot1, dot2):
    """ Return Euclidean distance between 2 points """
    return ((dot1.x - dot2.x) ** 2 + (dot1.y - dot2.y) ** 2) ** 0.5


def lu_dist(cluster1, cluster2):
    """ Return Ward's distance between 2 clusters"""
    centre_of_cluster1_x = sum([d.x for d in cluster1.dots]) / len(cluster1)
    centre_of_cluster1_y = sum([d.y for d in cluster1.dots]) / len(cluster1)
    centre_of_cluster1 = Dot(centre_of_cluster1_x, centre_of_cluster1_y)

    centre_of_cluster2_x = sum([d.x for d in cluster2.dots]) / len(cluster2)
    centre_of_cluster2_y = sum([d.y for d in cluster2.dots]) / len(cluster2)
    centre_of_cluster2 = Dot(centre_of_cluster2_x, centre_of_cluster2_y)

    dist_centres = ev_dist(centre_of_cluster1, centre_of_cluster2)

    return len(cluster1) * len(cluster2) * (dist_centres ** 2) / (len(cluster1) + len(cluster2))
