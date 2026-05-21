class DisjointSet:
    """
    Union-Find / Disjoint Set structure.

    Keeps track of connected components in a graph.
    Useful for Kruskal's algorithm to avoid cycles.
    """

    def __init__(self, size):
        # Each node starts as its own leader
        self.leader = list(range(size))

    def get_leader(self, node):
        """Finds the representative (leader) of a set."""

        if self.leader[node] != node:
            self.leader[node] = self.get_leader(self.leader[node])

        return self.leader[node]

    def connect_groups(self, node_a, node_b):
        """Merges two groups if they are different."""

        leader_a = self.get_leader(node_a)
        leader_b = self.get_leader(node_b)

        if leader_a == leader_b:
            return False

        self.leader[leader_a] = leader_b
        return True


def kruskal_mst(total_nodes, connections):
    """
    Kruskal's Minimum Spanning Tree algorithm.
    """

    # Sort edges from cheapest to most expensive
    connections.sort()

    groups = DisjointSet(total_nodes)

    selected_edges = []
    minimum_cost = 0

    for cost, start, end in connections:

        # Add edge only if it doesn't create a cycle
        if groups.connect_groups(start, end):
            selected_edges.append((start, end, cost))
            minimum_cost += cost

    return selected_edges, minimum_cost


if __name__ == "__main__":
    graph_edges = [
        (10, 0, 1),
        (6, 0, 2),
        (5, 0, 3),
        (15, 1, 3),
        (4, 2, 3)
    ]
    mst, cost = kruskal_mst(4, graph_edges)
    print(f"Aristas en el MST: {mst}")
    print(f"Costo mínimo total: {cost}")