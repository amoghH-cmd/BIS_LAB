import random

stops = {
    "Depot": (0, 0),
    "Stop A": (2, 5),
    "Stop B": (5, 2),
    "Stop C": (7, 8),
    "Stop D": (1, 9),
    "Stop E": (8, 3),
    "Stop F": (6, 6)
}

def distance(stop1, stop2):
    x1, y1 = stops[stop1]
    x2, y2 = stops[stop2]

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def route_distance(route):
    total = 0

    for i in range(len(route) - 1):
        total += distance(route[i], route[i + 1])

    total += distance(route[-1], "Depot")

    return total


def create_population(size):
    population = []

    stops_list = list(stops.keys())
    stops_list.remove("Depot")

    for _ in range(size):
        route = stops_list.copy()
        random.shuffle(route)
        route = ["Depot"] + route
        population.append(route)

    return population


def fitness(route):
    return 1 / route_distance(route)


def selection(population):
    population.sort(key=route_distance)
    return population[:len(population) // 2]


def crossover(parent1, parent2):
    p1 = parent1[1:]
    p2 = parent2[1:]

    size = len(p1)

    start = random.randint(0, size - 2)
    end = random.randint(start + 1, size - 1)

    child = [None] * size

    child[start:end] = p1[start:end]

    remaining = [stop for stop in p2 if stop not in child]

    index = 0

    for i in range(size):
        if child[i] is None:
            child[i] = remaining[index]
            index += 1

    return ["Depot"] + child


def mutation(route, mutation_rate=0.1):
    route = route.copy()

    if random.random() < mutation_rate:
        i = random.randint(1, len(route) - 1)
        j = random.randint(1, len(route) - 1)

        route[i], route[j] = route[j], route[i]

    return route


def genetic_algorithm(
    population_size=100,
    generations=500,
    mutation_rate=0.1
):
    population = create_population(population_size)

    for generation in range(generations):

        selected = selection(population)

        new_population = selected.copy()

        while len(new_population) < population_size:
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)

            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)

            new_population.append(child)

        population = new_population

        if generation % 50 == 0:
            best_route = min(population, key=route_distance)

            print(
                f"Generation {generation}: "
                f"Distance = {route_distance(best_route):.2f}"
            )

    return min(population, key=route_distance)


best_route = genetic_algorithm()

print("OPTIMIZED BUS ROUTE")

print(" -> ".join(best_route) + " -> Depot")

print(
    f"\nTotal Distance: "
    f"{route_distance(best_route):.2f} units"
)