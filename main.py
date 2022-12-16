from libs.data_preparer import *
from libs.matrix_tools import *
from libs.metrics import *
from libs.models import *
from math import exp, pi
from random import choice


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


def em_clustering(data, k):

    def p(kk, x):
        res = (1 / (2 * pi * o[kk][0] * o[kk][1])) *\
              exp((-1 / 2) * (((x.x - u[kk][0]) / o[kk][0]) ** 2 +
                              ((x.y - u[kk][1]) / o[kk][1]) ** 2))
        return res

    points = [Point(i[0], i[1]) for i in data]

    l = 3

    M = len(points)
    Y = k

    w = [1/Y for _ in range(Y)]
    u = [[points[0].x, points[0].y] for _ in range(Y)]

    o = [[0] * 2 for _ in range(Y)]
    for i in range(Y):
        o[i][0] = (1 / (M * Y)) * sum([(points[_].x - u[i][0]) ** 2 for _ in range(M)])
        o[i][1] = (1 / (M * Y)) * sum([(points[_].y - u[i][1]) ** 2 for _ in range(M)])

    g = [[0] * Y for _ in range(M)]
    for i in range(l):
        for y in range(Y):
            for j, point in enumerate(points):
                p_kx = w[y] * p(y, point) / sum([w[_] * p(_, point) for _ in range(Y)])
                g[j][y] = p_kx
        print(*g, sep="\n")

        for y in range(Y):
            w[y] = (1 / M) * sum([g[_][y] for _ in range(M)])

        for y in range(Y):
            u[y][0] = (1 / (M * w[y])) * sum([g[_][y] * points[_].x for _ in range(M)])
            u[y][1] = (1 / (M * w[y])) * sum([g[_][y] * points[_].y for _ in range(M)])

        for y in range(Y):
            o[y][0] = (1 / (M * w[y])) * sum([g[_][y] * (points[_].x - u[y][0]) ** 2 for _ in range(M)])
            o[y][1] = (1 / (M * w[y])) * sum([g[_][y] * (points[_].y - u[y][1]) ** 2 for _ in range(M)])

    clusterized_data = []
    for i in range(M):
        max_v = -1
        max_v_ind = -1
        for j in range(Y):
            if g[i][j] > max_v:
                max_v = g[i][j]
                max_v_ind = j
        clusterized_data.append([points[i].x, points[i].y, max_v_ind])

    return clusterized_data, Y


def k_means_clustering(data, k):

    points = [[i[0], i[1], 0] for i in data]
    u = [choice(points)[:2] for _ in range(k)]

    prev_points = []
    while prev_points != points:
        u_points = [[[], []] for _ in range(k)]
        for point in points:
            distances = [ev_dist_coord(j[0], j[1], point[0], point[1]) for j in u]
            min_dist = min(distances)
            for j, d in enumerate(distances):
                if d == min_dist:
                    point[2] = j
                    u_points[j][0] += [point[0]]
                    u_points[j][1] += [point[1]]
                    break
        for j in range(len(u)):
            if u_points[j][1] and u_points[j][0]:
                u[j] = [sum(u_points[j][0]) / len(u_points[j][0]),
                        sum(u_points[j][1]) / len(u_points[j][1])]
        prev_points = points

    return points, k


def forel_clustering(data, k=1):
    eps = 0.01
    r = 20
    points = [Point(i[0], i[1]) for i in data]
    clusters = []

    while points:
        distances = [[ev_dist(i, j) for i in points] for j in points]
        avers = []
        for i in distances:
            aver = sum(i)
            avers.append(aver)

        x0 = points[avers.index(min(avers))]

        x0_prev = Point(-10, -10)

        while ev_dist(x0, x0_prev) > eps:
            c = Cluster(x0)
            for p in points:
                if 0 < ev_dist(x0, p) <= r:
                    c.points += [p]
            x0_new_x = sum([i.x for i in c.points]) / len(c)
            x0_new_y = sum([i.y for i in c.points]) / len(c)
            x0_new = Point(x0_new_x, x0_new_y)

            x0_prev = x0
            x0 = x0_new
        if len(c) != 1:
            print(c.points)
            del c.points[c.points.index(x0_prev)]

        for p in c.points:
            del points[points.index(p)]

        clusters.append(c)

    clusterized_data = []
    for i, c in enumerate(clusters):

        for p in c.points:
            clusterized_data.append([p.x, p.y, i])

    return clusterized_data, len(clusters)


def main():
    data = get_big_data("data/data_prepared.txt")
    k = 3
    # points, clusters_amount = hierarchical_clustering(data, k=k)
    # points, clusters_amount = graph_clustering(data, k=k)
    # points, clusters_amount = em_clustering(data, k=k)
    # points, clusters_amount = k_means_clustering(data, k=k)
    points, clusters_amount = forel_clustering(data, k=k)
    show_plot(points, clusters=clusters_amount)


if __name__ == "__main__":
    main()
