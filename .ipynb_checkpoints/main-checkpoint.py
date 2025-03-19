# from mpi4py import MPI
# import time
# import numpy as np
# import pandas as pd
# from src.genetic_algorithms_functions import calculate_fitness, \
#     select_in_tournament, order_crossover, mutate, \
#     generate_unique_population

# start_time = time.time()  # Start execution timer

# # Load the distance matrix
# distance_matrix = pd.read_csv('city_distances.csv').to_numpy()

# # Parameters
# num_nodes = distance_matrix.shape[0]
# population_size = 10000
# num_tournaments = 4  # Number of tournaments to run
# mutation_rate = 0.1
# num_generations = 200
# infeasible_penalty = 1e6  # Penalty for infeasible routes
# stagnation_limit = 5  # Number of generations without improvement before regeneration


# # Generate initial population: each individual is a route starting at node 0
# np.random.seed(42)  # For reproducibility
# population = generate_unique_population(population_size, num_nodes)

# # Initialize variables for tracking stagnation
# best_calculate_fitness = int(1e6)
# stagnation_counter = 0

# # Main GA loop
# for generation in range(num_generations):
#     # Evaluate calculate_fitness
#     calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in population])

#     # Check for stagnation
#     current_best_calculate_fitness = np.min(calculate_fitness_values)
#     if current_best_calculate_fitness < best_calculate_fitness:
#         best_calculate_fitness = current_best_calculate_fitness
#         stagnation_counter = 0
#     else:
#         stagnation_counter += 1

#     # Regenerate population if stagnation limit is reached, keeping the best individual
#     if stagnation_counter >= stagnation_limit:
#         print(f"Regenerating population at generation {generation} due to stagnation")
#         best_individual = population[np.argmin(calculate_fitness_values)]
#         population = generate_unique_population(population_size - 1, num_nodes)
#         population.append(best_individual)
#         stagnation_counter = 0
#         continue  # Skip the rest of the loop for this generation

#     # Selection, crossover, and mutation
#     selected = select_in_tournament(population,
#                                     calculate_fitness_values)
#     offspring = []
#     for i in range(0, len(selected), 2):
#         parent1, parent2 = selected[i], selected[i + 1]
#         route1 = order_crossover(parent1[1:], parent2[1:])
#         offspring.append([0] + route1)
#     mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

#     # Replacement: Replace the individuals that lost in the tournaments with the new offspring
#     for i, idx in enumerate(np.argsort(calculate_fitness_values)[::-1][:len(mutated_offspring)]):
#         population[idx] = mutated_offspring[i]

#     # Ensure population uniqueness
#     unique_population = set(tuple(ind) for ind in population)
#     while len(unique_population) < population_size:
#         individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
#         unique_population.add(tuple(individual))
#     population = [list(individual) for individual in unique_population]

#     # Print best calculate_fitness
#     print(f"Generation {generation}: Best calculate_fitness = {current_best_calculate_fitness}")

# # Update calculate_fitness_values for the final population
# calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in population])

# # Output the best solution
# best_solution = population[np.argmin(calculate_fitness_values)]
# print("Best Solution:", best_solution)
# print("Total Distance:", calculate_fitness(best_solution, distance_matrix))

# end_time = time.time()  # End execution timer
# print(f"Execution Time: {end_time - start_time:.2f} seconds")


# PARALLELIZABLE CODE WITH ADAPTIVE MUTATE AND OX_CROSSOVER

from mpi4py import MPI
import time
import numpy as np
import pandas as pd
from genetic_algorithms_functions import (
    calculate_fitness, select_in_tournament, pmx_crossover,  # Use PMX instead of OX
    adaptive_mutate, generate_unique_population    #Use Adaptive mutate instead of muatete
)

# MPI initialization
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

start_time = time.time()  # Start execution timer

# Load distance matrix (only in rank 0)
if rank == 0:
    distance_matrix = pd.read_csv('city_distances.csv').to_numpy()
else:
    distance_matrix = None

# Broadcast the distance matrix to all processes
distance_matrix = comm.bcast(distance_matrix, root=0)

# Problem Parameters
num_nodes = 20  # Fixed for this problem
population_size = 10000  # Total across all processes
num_tournaments = 6  # Stronger selection pressure
mutation_rate = 0.05  # Start with low mutation rate
num_generations = 200
stagnation_limit = 5
infeasible_penalty = 1e6  # Large penalty for invalid routes

# Generate initial population (only in rank 0)
if rank == 0:
    np.random.seed(42)
    population = generate_unique_population(population_size, num_nodes)
    population_chunks = np.array_split(population, size)  # Split for processes
else:
    population_chunks = None

# Scatter population to processes
sub_population = comm.scatter(population_chunks, root=0)

# Initialize variables
best_fitness = float('inf')
stagnation_counter = 0

# Genetic Algorithm main loop
for generation in range(num_generations):
    # Evaluate fitness for local population
    sub_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in sub_population])

    # Gather fitness values at rank 0
    fitness_values = comm.gather(sub_fitness_values, root=0)

    if rank == 0:
        fitness_values = np.concatenate(fitness_values)  # Merge results
        current_best_fitness = np.min(fitness_values)

        # Adaptive mutation rate adjustment
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            stagnation_counter = 0
            mutation_rate = max(0.05, mutation_rate * 0.9)  # Reduce mutation slightly
        else:
            stagnation_counter += 1
            if stagnation_counter >= 3:
                mutation_rate = min(0.3, mutation_rate * 1.5)  # Increase mutation rate

        # Regenerate if stagnation occurs
        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation")
            best_individual = population[np.argmin(fitness_values)]
            population = generate_unique_population(population_size - 1, num_nodes)
            population.append(best_individual)
            population_chunks = np.array_split(population, size)
            stagnation_counter = 0
    else:
        population_chunks = None

    # Broadcast new population if needed
    sub_population = comm.scatter(population_chunks, root=0)

    # Selection, crossover, and mutation
    selected = select_in_tournament(sub_population, sub_fitness_values, tournament_size=6)  # Stronger selection
    offspring = []
    for i in range(0, len(selected), 2):
        if i + 1 < len(selected):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = pmx_crossover(parent1[1:], parent2[1:])  # Use PMX crossover
            offspring.append([0] + route1)  # Ensure depot is the start

    mutated_offspring = [adaptive_mutate(route, mutation_rate) for route in offspring]

    # Replacement
    for i, idx in enumerate(np.argsort(sub_fitness_values)[::-1][:len(mutated_offspring)]):
        sub_population[idx] = mutated_offspring[i]

    # Ensure uniqueness
    unique_population = set(tuple(ind) for ind in sub_population)
    while len(unique_population) < len(sub_population):
        individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
        unique_population.add(tuple(individual))
    sub_population = [list(individual) for individual in unique_population]

    # Print progress from rank 0
    if rank == 0:
        print(f"Generation {generation}: Best fitness = {current_best_fitness}")

# Gather final population at rank 0
final_population = comm.gather(sub_population, root=0)

# Rank 0 selects the best solution
if rank == 0:
    final_population = [ind for sublist in final_population for ind in sublist]  # Flatten
    final_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in final_population])
    best_idx = np.argmin(final_fitness_values)
    best_solution = final_population[best_idx]

    print("Best Solution:", best_solution)
    print("Total Distance:", -final_fitness_values[best_idx])

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.2f} seconds")
