def ev_dist(point1, point2):
    """ Return Euclidean distance between 2 points """
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5


def lu_dist(cluster1, cluster2):
    """ Return Ward's distance between 2 clusters"""
    centre_of_cluster1_x = sum([d.x for d in cluster1.points]) / len(cluster1)
    centre_of_cluster1_y = sum([d.y for d in cluster1.points]) / len(cluster1)

    centre_of_cluster2_x = sum([d.x for d in cluster2.points]) / len(cluster2)
    centre_of_cluster2_y = sum([d.y for d in cluster2.points]) / len(cluster2)

    dist_centres = ev_dist_coord(centre_of_cluster1_x, centre_of_cluster1_y,
                                 centre_of_cluster2_x, centre_of_cluster2_y)

    return len(cluster1) * len(cluster2) * (dist_centres ** 2) / (len(cluster1) + len(cluster2))


def ev_dist_coord(x1, y1, x2, y2):
    """ Return Euclidean distance between 2 points viewed as coordinates """
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
