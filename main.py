from data_preparer import *
from helpful_tools import *
from metrics import *


class Cluster:
    def __init__(self, dot):
        self.dots = [dot]

    def __len__(self):
        return len(self.dots)

    def add_cluster(self, other):
        for dot in other.dots:
            self.dots.append(dot)


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Edge:
    def __init__(self, dot1, dot2):
        self.dot1 = dot1
        self.dot2 = dot2
        self.length = ev_dist(dot1, dot2)

    def __eq__(self, other):
        if ((self.dot1 == other.dot1 and self.dot2 == other.dot2) or
                (self.dot1 == other.dot2 and self.dot2 == other.dot1)):
            return True
        return False

    def __repr__(self):
        return f"Edge {self.dot1} to {self.dot2} with len {round(self.length, 5)}"


class Graph:
    def __init__(self, root):
        self.roots = [root]
        self.edges = []

    def add_dot(self, graph_root, root):
        graph_root_ind = self.roots.index(graph_root)
        self.roots.append(root)
        self.edges.append(Edge(self.roots[graph_root_ind], root))


def hierarchical_clustering(data, k=1):
    c = [Cluster(Dot(i[0], i[1])) for i in data]
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
        for dt in c[i].dots:
            clusterized_data.append([dt.x, dt.y, i])

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
                    if edge.dot1 in res[cluster]:
                        res[cluster].append(edge.dot2)
                        flag = False
                    elif edge.dot2 in res[cluster]:
                        res[cluster].append(edge.dot1)
                        flag = False
                if flag:
                    res.append([edge.dot1, edge.dot2])
            else:
                res.append([edge.dot1, edge.dot2])

        for root in gr.roots:
            if root not in linear(res):
                res.append([root])

        return res

    dots = [Dot(i[0], i[1]) for i in data]
    distances = [[ev_dist(i, j) for j in dots] for i in dots]

    dot_start1_ind, dot_start2_ind, distance = find_minimal_from_matrix(distances)
    dot_start1 = dots[dot_start1_ind]
    dot_start2 = dots[dot_start2_ind]

    spanning_tree = Graph(dot_start1)
    spanning_tree.add_dot(dot_start1, dot_start2)

    if dot_start1_ind < dot_start2_ind:
        del dots[dot_start2_ind]
        del dots[dot_start1_ind]
    else:
        del dots[dot_start1_ind]
        del dots[dot_start2_ind]

    while dots:
        nearest_dot = min(spanning_tree.roots, key=lambda x: ev_dist(x, dots[0]))
        spanning_tree.add_dot(nearest_dot, dots[0])
        del dots[0]

    result_clusters = del_n_edges(spanning_tree, k)
    clusterized_data = []
    for i in range(len(result_clusters)):
        for dt in result_clusters[i]:
            clusterized_data.append([dt.x, dt.y, i])

    return clusterized_data, len(result_clusters)


def main():
    data = get_data("data_prepared.txt")
    k = 4
    # dots, clusters_amount = hierarchical_clustering(data, k=k)
    dots, clusters_amount = graph_clustering(data, k=k)
    show_plot(dots, clusters=clusters_amount)


if __name__ == "__main__":
    main()
