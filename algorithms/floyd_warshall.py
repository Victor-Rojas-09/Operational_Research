def floyd_warshall(number_of_nodes, weighted_edges):
    """
    Floyd-Warshall Algorithm:

    Computes the shortest path between EVERY pair of nodes
    in a weighted graph.
    """

    # STEP 1: Create distance matrix

    # Infinity
    INFINITY = float("inf")

    shortest_distance = [
        [INFINITY] * number_of_nodes
        for _ in range(number_of_nodes)
    ]

    # STEP 2: Distance from a node to itself is 0
    for node in range(number_of_nodes):
        shortest_distance[node][node] = 0

    # STEP 3: Fill matrix with direct edge weights
    for source, destination, weight in weighted_edges:
        shortest_distance[source][destination] = weight

    # STEP 4: Floyd-Warshall logic
    for intermediate_node in range(number_of_nodes):

        for source_node in range(number_of_nodes):

            for destination_node in range(number_of_nodes):

                # Current known distance
                current_distance = (
                    shortest_distance[source_node][destination_node]
                )

                # Possible shorter route using the intermediate node
                new_possible_distance = (
                    shortest_distance[source_node][intermediate_node]
                    +
                    shortest_distance[intermediate_node][destination_node]
                )

                # keep the shortest option
                if new_possible_distance < current_distance:

                    shortest_distance[source_node][destination_node] = (
                        new_possible_distance
                    )

    # STEP 5: Detect negative cycles
    for node in range(number_of_nodes):

        if shortest_distance[node][node] < 0:
            raise ValueError("Graph contains a negative cycle")

    # Return shortest distance
    return shortest_distance


# ------------------------------------------------------
# Example Usage
# ------------------------------------------------------

graph_edges = [
    (0, 1, 3),
    (0, 2, 8),
    (1, 2, 2),
    (1, 3, 5),
    (2, 3, 1),
    (3, 0, 2)
]

distance_matrix = floyd_warshall(
    number_of_nodes=4,
    weighted_edges=graph_edges
)

print("Shortest Distance Matrix:\n")

for row in distance_matrix:
    print(row)