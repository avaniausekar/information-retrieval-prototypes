# Note this is just a basic version for implementation purposes
def pagerank(graph, damping_factor=0.85, max_iterations=10, tolerance=1e-6):
    nodes = list(graph.keys())
    n = len(nodes)

    # Initializing all nodes with equal probability
    scores = {node: 1.0 / n for node in nodes}

    for iteration in range(max_iterations):
        new_scores = {}

        for node in nodes:
            # Start with base probability (random jump)
            score = (1 - damping_factor) / n

            # Add contributions from incoming links
            for source_node in nodes:
                if node in graph.get(source_node, []):
                    # Handle dangling nodes
                    outgoing_links = len(graph[source_node]) or 1
                    score += damping_factor * \
                        scores[source_node] / outgoing_links

            new_scores[node] = score

        # Check convergence
        if max(abs(new_scores[node] - scores[node]) for node in nodes) < tolerance:
            print(f"Converged after {iteration + 1} iterations")
            break

        scores = new_scores
    return scores


if __name__ == "__main__":

    graph = {
        'A': ['B', 'C'],
        'B': ['C'],
        'C': ['A'],
        'D': ['C']
    }
    scores = pagerank(graph)
    print("PageRank scores:")
    for node, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{node}: {score:.4f}")
