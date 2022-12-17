from libs.metrics import ev_dist


class Cluster:
    def __init__(self, point):
        self.points = [point]

    def __len__(self):
        return len(self.points)

    def add_cluster(self, other):
        """ Merging other cluster to current """
        for point in other.points:
            self.points.append(point)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Edge:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = ev_dist(point1, point2)  # length between 2 points of the edge

    def __eq__(self, other):
        """ Equality of edges is reached by equality of 2 roots connected by these edges """
        if ((self.point1 == other.point1 and self.point2 == other.point2) or
                (self.point1 == other.point2 and self.point2 == other.point1)):
            return True
        return False

    def __repr__(self):
        return f"Edge {self.point1} to {self.point2} with len {round(self.length, 5)}"


class Graph:
    def __init__(self, root):
        self.roots = [root]
        self.edges = []

    def add_root(self, graph_root, root):
        """ Adding a root to the current Graph with the computation of the needed edge """
        graph_root_ind = self.roots.index(graph_root)
        self.roots.append(root)
        self.edges.append(Edge(self.roots[graph_root_ind], root))  # not only adding but connecting to the existing one
