from libs.data_preparer import *
from libs.helpful_tools import *
from libs.metrics import *
from libs.models import *


def hierarchical_clustering(data, k=1):
    c = [Cluster(Point(i[0], i[1])) for i in data]
    ln = len(c)

    distances = [[lu_dist(i, j) for j in c] for i in c]

    for t in range(2, ln + 1 - k):

        u_ind, v_ind, min_dist = find_minimal_from_matrix(distances)
        u = c[u_ind]
        v = c[v_ind]
        u.add_cluster(v)

        for i in range(len(c)):
            del distances[i][v_ind]
        del distances[v_ind]
        del c[c.index(v)]

        w = c.index(u)
        for s in range(len(distances[w])):
            if s != w:
                distances[w][s] = lu_dist(c[w], c[s])
        for s in range(len(distances)):
            if s != w:
                distances[s][w] = lu_dist(c[w], c[s])

    clusterized_data = []
    for i in range(len(c)):
        for pt in c[i].points:
            clusterized_data.append([pt.x, pt.y, i])

    return clusterized_data, len(c)


def graph_clustering(data, k=1):

    def del_n_edges(graph, n):
        k_edges = sorted(graph.edges, key=lambda x: x.length)[-n:]
        gr = graph
        res = []

        for edge in k_edges:
            del gr.edges[gr.edges.index(edge)]

        for edge in gr.edges:
            if res:
                flag = True
                for cluster in range(len(res)):
                    if edge.point1 in res[cluster]:
                        res[cluster].append(edge.point2)
                        flag = False
                    elif edge.point2 in res[cluster]:
                        res[cluster].append(edge.point1)
                        flag = False
                if flag:
                    res.append([edge.point1, edge.point2])
            else:
                res.append([edge.point1, edge.point2])

        for root in gr.roots:
            if root not in linear(res):
                res.append([root])

        return res

    points = [Point(i[0], i[1]) for i in data]
    distances = [[ev_dist(i, j) for j in points] for i in points]

    point_start1_ind, point_start2_ind, distance = find_minimal_from_matrix(distances)
    point_start1 = points[point_start1_ind]
    point_start2 = points[point_start2_ind]

    spanning_tree = Graph(point_start1)
    spanning_tree.add_root(point_start1, point_start2)

    if point_start1_ind < point_start2_ind:
        del points[point_start2_ind]
        del points[point_start1_ind]
    else:
        del points[point_start1_ind]
        del points[point_start2_ind]

    while points:
        nearest_point = min(spanning_tree.roots, key=lambda x: ev_dist(x, points[0]))
        spanning_tree.add_root(nearest_point, points[0])
        del points[0]

    result_clusters = del_n_edges(spanning_tree, k)
    clusterized_data = []
    for i in range(len(result_clusters)):
        for dt in result_clusters[i]:
            clusterized_data.append([dt.x, dt.y, i])

    return clusterized_data, len(result_clusters)


def main():
    data = get_data("data/data_prepared.txt")
    k = 4
    # points, clusters_amount = hierarchical_clustering(data, k=k)
    points, clusters_amount = graph_clustering(data, k=k)
    show_plot(points, clusters=clusters_amount)


if __name__ == "__main__":
    main()
