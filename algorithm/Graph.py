# Python program for Dijkstra's single
# source the shortest path algorithm. The program is
# for adjacency matrix representation of the graph
class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def print_solution(self, dist):
        print("Vertex \t Distance from Source")
        for node in range(self.V):
            print(node, "\t\t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in the shortest path tree
    def min_distance(self, dist, spt_set):

        # Initialize minimum distance for next node
        minimum = float('inf')

        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < minimum and spt_set[v] is False:
                minimum = dist[v]
                min_index = v

        return min_index

    # Function that implements Dijkstra's single source the
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        dist = [float('inf')] * self.V
        dist[src] = 0
        spt_set = [False] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.min_distance(dist, spt_set)

            # Put the minimum distance vertex in the
            # shortest path tree
            spt_set[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                        spt_set[v] is False and
                        dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]

        # self.print_solution(dist)
