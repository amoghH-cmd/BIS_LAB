import random

# Network: router -> {neighbor: link_cost}
network = {
    'A': {'B': 2, 'C': 4},
    'B': {'A': 2, 'C': 1, 'D': 7},
    'C': {'A': 4, 'B': 1, 'D': 3, 'E': 5},
    'D': {'B': 7, 'C': 3, 'E': 2, 'F': 4},
    'E': {'C': 5, 'D': 2, 'F': 1},
    'F': {'D': 4, 'E': 1}
}

source, destination = 'A', 'F'
m, iterations = 20, 100
alpha, beta, rho, Q = 1.0, 2.0, 0.5, 100
initial_pheromone = 0.1

# Initialize pheromone and heuristic
pheromone = {
    u: {v: initial_pheromone for v in network[u]}
    for u in network
}
heuristic = {
    u: {v: 1 / cost for v, cost in network[u].items()}
    for u in network
}

best_path, best_cost = None, float('inf')

for _ in range(iterations):
    all_paths = []

    # Each ant searches for a route
    for _ in range(m):
        path = [source]
        visited = {source}
        current = source
        cost = 0

        while current != destination:
            candidates = [
                v for v in network[current] if v not in visited
            ]

            if not candidates:
                break

            weights = [
                pheromone[current][v] ** alpha *
                heuristic[current][v] ** beta
                for v in candidates
            ]

            next_node = random.choices(
                candidates, weights=weights, k=1
            )[0]

            cost += network[current][next_node]
            path.append(next_node)
            visited.add(next_node)
            current = next_node

        # Keep only routes that reach the destination
        if current == destination:
            all_paths.append((path.copy(), cost))

            if cost < best_cost:
                best_path, best_cost = path.copy(), cost

    # Evaporate pheromones
    for u in network:
        for v in network[u]:
            pheromone[u][v] *= (1 - rho)

    # Deposit pheromones on successful routes
    for path, cost in all_paths:
        deposit = Q / cost

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            pheromone[u][v] += deposit
            pheromone[v][u] += deposit

# Display result
if best_path:
    print("Best Packet Route:", " -> ".join(best_path))
    print("Minimum Network Cost:", best_cost)
else:
    print("No route found. Check network connectivity.")