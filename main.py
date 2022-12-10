from data_preparer import show_plot, get_data
from helpful_tools import print_matrix, find_minimal_from_matrix


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


def hierarchical_clustering(data):

    def ev_dist(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def lu_dist(c1, c2):
        centre_of_c1_x = sum([d.x for d in c1.dots]) / len(c1)
        centre_of_c1_y = sum([d.y for d in c1.dots]) / len(c1)

        centre_of_c2_x = sum([d.x for d in c2.dots]) / len(c2)
        centre_of_c2_y = sum([d.y for d in c2.dots]) / len(c2)

        dist_centres = ev_dist(centre_of_c1_x, centre_of_c1_y, centre_of_c2_x, centre_of_c2_y)

        return len(c1) * len(c2) * (dist_centres ** 2) / (len(c1) + len(c2))

    c = [Cluster(Dot(i[0], i[1])) for i in data]
    ln = len(c)

    distances = [[lu_dist(i, j) for j in c] for i in c]

    for t in range(2, ln + 1 - 3):

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


def main():
    data = get_data("data_prepared.txt")
    dots, clusters_amount = hierarchical_clustering(data)
    show_plot(dots, clusters=clusters_amount)


if __name__ == "__main__":
    main()
