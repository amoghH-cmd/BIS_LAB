import numpy as np


distance_matrix = np.array([
    [0,  4,  8,  6,  7],
    [4,  0,  5,  7,  3],
    [8,  5,  0,  4,  6],
    [6,  7,  4,  0,  5],
    [7,  3,  6,  5,  0]
])

NUM_STOPS = len(distance_matrix)



def cost_function(route):


    total_distance = 0

    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]


    total_distance += distance_matrix[route[-1]][route[0]]

    return total_distance




POPULATION = 30
MAX_ITER = 5


w = 0.7
c1 = 1.5
c2 = 1.5



class Particle:

    def __init__(self):


        self.position = np.random.permutation(NUM_STOPS)


        self.velocity = []

        # Personal best
        self.best_position = self.position.copy()
        self.best_fitness = cost_function(self.position)

        self.fitness = self.best_fitness




def create_new_route(current_route, target_route):

    """
    Moves the current route toward the target route.

    A simple swap-based mechanism is used because
    bus routes are permutations rather than continuous values.
    """

    new_route = current_route.copy()

    for i in range(NUM_STOPS):

        if np.random.rand() < 0.5:

            target_value = target_route[i]

            current_index = np.where(new_route == target_value)[0][0]

            # Swap the values
            new_route[i], new_route[current_index] = \
                new_route[current_index], new_route[i]

    return new_route




def particle_swarm_optimization():


    swarm = [Particle() for _ in range(POPULATION)]


    gbest_position = swarm[0].best_position.copy()
    gbest_fitness = swarm[0].best_fitness

    for particle in swarm:

        if particle.best_fitness < gbest_fitness:

            gbest_fitness = particle.best_fitness
            gbest_position = particle.best_position.copy()




    for iteration in range(MAX_ITER):

        for particle in swarm:

            # Move toward personal best
            personal_route = create_new_route(
                particle.position,
                particle.best_position
            )

           
            global_route = create_new_route(
                personal_route,
                gbest_position
            )


            particle.position = global_route


            particle.fitness = cost_function(
                particle.position
            )




            if particle.fitness < particle.best_fitness:

                particle.best_fitness = particle.fitness

                particle.best_position = \
                    particle.position.copy()



            if particle.fitness < gbest_fitness:

                gbest_fitness = particle.fitness

                gbest_position = \
                    particle.position.copy()


        print(
            f"Iteration {iteration + 1}/{MAX_ITER}, "
            f"Best Distance = {gbest_fitness:.2f}"
        )


    return gbest_position, gbest_fitness


#

if __name__ == "__main__":

    best_position, best_fitness = \
        particle_swarm_optimization()

    print("\nOptimal Bus Route Found:")

    print("Route:", best_position)

    print("Total Distance:", best_fitness)
