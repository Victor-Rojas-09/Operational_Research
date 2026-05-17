class DSU:
    # Structure for handling disjoint sets (Union-Find)
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False
def kruskal_mst(num_nodes, edges):

    # Sort edges by weight (Greedy)
    edges.sort()
    
    dsu = DSU(num_nodes)
    mst_edges = []
    total_cost = 0

    for weight, u, v in edges:
        # If connecting u and v does not create a cycle, add the edge.
        if dsu.union(u, v):
            mst_edges.append((u, v, weight))
            total_cost += weight

    return mst_edges, total_cost

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