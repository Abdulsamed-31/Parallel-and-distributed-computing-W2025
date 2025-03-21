from mpi4py import MPI
import time
import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import (
    calc_fitness_multiple_cars, select_in_tournament, pmx_crossover,  
    adaptive_mutate, generate_unique_population_multiple_cars
)

# MPI Setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

start_time = time.time()

# Load distance matrix (only rank 0 does this)
if rank == 0:
    distance_matrix = pd.read_csv('city_distances_extended.csv').to_numpy()
else:
    distance_matrix = None

# Asynchronously broadcast the distance matrix
distance_matrix = comm.bcast(distance_matrix, root=0)

# Problem Parameters
num_nodes = 20  # Number of locations (excluding depot)
num_cars = 4  # Number of cars
population_size = 5000  # Total across all processes
num_tournaments = 6  
mutation_rate = 0.05  
num_generations = 200  
stagnation_limit = 5  

# Generate initial population (only in rank 0)
if rank == 0:
    np.random.seed(42)
    population = np.array(generate_unique_population_multiple_cars(population_size, num_nodes, num_cars), dtype=object)
    population_chunks = np.array_split(population, size)
else:
    population_chunks = None

# Non-blocking scatter for better efficiency
sub_population = np.empty(len(population_chunks[0]) if rank == 0 else 0, dtype=object)
comm.Scatter(population_chunks, sub_population, root=0)

# Initialize tracking variables
best_fitness = float('inf')
stagnation_counter = 0

# Multi-Car Genetic Algorithm
for generation in range(num_generations):
    # Vectorized fitness calculation
    sub_fitness_values = np.array([calc_fitness_multiple_cars(route, distance_matrix, num_cars) for route in sub_population])

    # Asynchronous gather of fitness values
    fitness_values = None
    if rank == 0:
        fitness_values = np.empty(population_size, dtype=float)
    comm.Gather(sub_fitness_values, fitness_values, root=0)

    if rank == 0:
        current_best_fitness = np.min(fitness_values)

        # Adaptive mutation rate
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            stagnation_counter = 0
            mutation_rate = max(0.02, mutation_rate * 0.9)  
        else:
            stagnation_counter += 1
            if stagnation_counter >= 3:
                mutation_rate = min(0.3, mutation_rate * 1.5)  

        # Improved stagnation handling
        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating at generation {generation} due to stagnation")
            best_individual = population[np.argmin(fitness_values)]
            population = np.array(generate_unique_population_multiple_cars(population_size - 1, num_nodes, num_cars), dtype=object)
            population = np.append(population, [best_individual])
            population_chunks = np.array_split(population, size)
            stagnation_counter = 0
    
    # Non-blocking scatter for updated population
    sub_population = np.empty(len(population_chunks[0]) if rank == 0 else 0, dtype=object)
    comm.Scatter(population_chunks, sub_population, root=0)

    # Batch processing for selection, crossover, and mutation
    selected = select_in_tournament(sub_population, sub_fitness_values, tournament_size=6)
    offspring = [pmx_crossover(selected[i], selected[i + 1]) for i in range(0, len(selected) - 1, 2)]
    mutated_offspring = np.array([adaptive_mutate(route, mutation_rate) for route in offspring], dtype=object)

    # Replacement using vectorized numpy operations
    worst_indices = np.argsort(sub_fitness_values)[-len(mutated_offspring):]
    sub_population[worst_indices] = mutated_offspring

    # Print progress from rank 0
    if rank == 0:
        print(f"Generation {generation}: Best fitness = {current_best_fitness}")

# Gather final population
final_population = None
if rank == 0:
    final_population = np.empty((population_size,), dtype=object)
comm.Gather(sub_population, final_population, root=0)

if rank == 0:
    final_fitness_values = np.array([calc_fitness_multiple_cars(route, distance_matrix, num_cars) for route in final_population])
    best_idx = np.argmin(final_fitness_values)
    best_solution = final_population[best_idx]

    print("Best Solution:", best_solution)
    print("Total Distance:", -final_fitness_values[best_idx])

    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.2f} seconds")



# #Multiple Cars:

# from mpi4py import MPI
# import time
# import numpy as np
# import pandas as pd
# from src.genetic_algorithms_functions import (
#     calc_fitness_multiple_cars, select_in_tournament, pmx_crossover,  
#     adaptive_mutate, generate_unique_population_multiple_cars
# )

# # MPI Setup
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()

# start_time = time.time()

# # Load distance matrix (only rank 0 does this)
# if rank == 0:
#     distance_matrix = pd.read_csv('city_distances_extended.csv').to_numpy()
# else:
#     distance_matrix = None

# # Broadcast the distance matrix to all processes
# distance_matrix = comm.bcast(distance_matrix, root=0)

# # Problem Parameters
# num_nodes = 20  # Number of locations (excluding depot)
# num_cars = 4  # Number of cars
# population_size = 5000  # Total across all processes
# num_tournaments = 6  
# mutation_rate = 0.05  
# num_generations = 200  
# stagnation_limit = 5  
# max_distance_threshold = 400  # Ensure total distance is below this

# # Generate initial population (only in rank 0)
# if rank == 0:
#     np.random.seed(42)
#     population = generate_unique_population_multiple_cars(population_size, num_nodes, num_cars)   #generate unique population with multiple cars
#     # Ensure population is a list before splitting
#     population_chunks = [population[i::size] for i in range(size)]   # Divide population for MPI
# else:
#     population_chunks = None

# # Scatter population to processes
# sub_population = comm.scatter(population_chunks, root=0)

# # Initialize tracking variables
# best_fitness = float('inf')
# stagnation_counter = 0

# # Multi-Car Genetic Algorithm
# for generation in range(num_generations):
#     # Evaluate fitness for each sub-population
#     sub_fitness_values = np.array([calc_fitness_multiple_cars(route, distance_matrix, num_cars) for route in sub_population])  #calculate fitness for multiple cars

#     # Gather fitness values at rank 0
#     fitness_values = comm.gather(sub_fitness_values, root=0)

#     if rank == 0:
#         fitness_values = np.concatenate(fitness_values)  
#         current_best_fitness = np.min(fitness_values)

#         # Adaptive mutation rate
#         if current_best_fitness < best_fitness:
#             best_fitness = current_best_fitness
#             stagnation_counter = 0
#             mutation_rate = max(0.02, mutation_rate * 0.9)  
#         else:
#             stagnation_counter += 1
#             if stagnation_counter >= 3:
#                 mutation_rate = min(0.3, mutation_rate * 1.5)  

#         # Regenerate population if stagnation occurs
#         if stagnation_counter >= stagnation_limit:
#             print(f"Regenerating at generation {generation} due to stagnation")
#             best_individual = population[np.argmin(fitness_values)]
#             population = generate_unique_population_multiple_cars(population_size - 1, num_nodes, num_cars) #generating unique population with multiple cars
#             population.append(best_individual)
#             population_chunks = [population[i::size] for i in range(size)]   # Ensure population is a list before splitting

#             stagnation_counter = 0
#     else:
#         population_chunks = None

#     # Broadcast updated population
#     sub_population = comm.scatter(population_chunks, root=0)

#     # Selection, crossover, and mutation
#     selected = select_in_tournament(sub_population, sub_fitness_values, tournament_size=6)
#     offspring = []
#     for i in range(0, len(selected), 2):
#         if i + 1 < len(selected):
#             parent1, parent2 = selected[i], selected[i + 1]
#             route1 = pmx_crossover(parent1, parent2)  
#             offspring.append(route1)

#     mutated_offspring = [adaptive_mutate(route, mutation_rate) for route in offspring]

#     # Replacement
#     for i, idx in enumerate(np.argsort(sub_fitness_values)[::-1][:len(mutated_offspring)]):
#         sub_population[idx] = mutated_offspring[i]

#     # Print progress from rank 0
#     if rank == 0:
#         print(f"Generation {generation}: Best fitness = {current_best_fitness}")

# # Gather final population
# final_population = comm.gather(sub_population, root=0)

# if rank == 0:
#     final_population = [ind for sublist in final_population for ind in sublist]
#     final_fitness_values = np.array([calc_fitness_multiple_cars(route, distance_matrix, num_cars) for route in final_population])  #calculate fitness for multiple cars
#     best_idx = np.argmin(final_fitness_values)
#     best_solution = final_population[best_idx]

#     print("Best Solution:", best_solution)
#     print("Total Distance:", -final_fitness_values[best_idx])

#     end_time = time.time()
#     print(f"Execution Time: {end_time - start_time:.2f} seconds")


#PARALLELIZABLE CODE WITH ADAPTIVE MUTATE AND OX_CROSSOVER

# from mpi4py import MPI
# import time
# import numpy as np
# import pandas as pd
# from src.genetic_algorithms_functions import (
#     calculate_fitness, select_in_tournament, pmx_crossover,  # Use PMX instead of OX
#     adaptive_mutate, generate_unique_population    #Use Adaptive mutate instead of muatete
# )

# # MPI initialization
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()

# start_time = time.time()  # Start execution timer

# # Load distance matrix (only in rank 0)
# if rank == 0:
#     distance_matrix = pd.read_csv('city_distances_extended.csv').to_numpy()
# else:
#     distance_matrix = None

# # Broadcast the distance matrix to all processes
# distance_matrix = comm.bcast(distance_matrix, root=0)

# # Problem Parameters
# num_nodes = 20  # Fixed for this problem
# population_size = 10000  # Total across all processes
# num_tournaments = 6  # Stronger selection pressure
# mutation_rate = 0.05  # Start with low mutation rate
# num_generations = 200
# stagnation_limit = 5
# infeasible_penalty = 1e6  # Large penalty for invalid routes

# # Generate initial population (only in rank 0)
# if rank == 0:
#     np.random.seed(42)
#     population = generate_unique_population(population_size, num_nodes)
#     population_chunks = np.array_split(population, size)  # Split for processes
# else:
#     population_chunks = None

# # Scatter population to processes
# sub_population = comm.scatter(population_chunks, root=0)

# # Initialize variables
# best_fitness = float('inf')
# stagnation_counter = 0

# # Genetic Algorithm main loop
# for generation in range(num_generations):
#     # Evaluate fitness for local population
#     sub_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in sub_population])

#     # Gather fitness values at rank 0
#     fitness_values = comm.gather(sub_fitness_values, root=0)

#     if rank == 0:
#         fitness_values = np.concatenate(fitness_values)  # Merge results
#         current_best_fitness = np.min(fitness_values)

#         # Adaptive mutation rate adjustment
#         if current_best_fitness < best_fitness:
#             best_fitness = current_best_fitness
#             stagnation_counter = 0
#             mutation_rate = max(0.05, mutation_rate * 0.9)  # Reduce mutation slightly
#         else:
#             stagnation_counter += 1
#             if stagnation_counter >= 3:
#                 mutation_rate = min(0.3, mutation_rate * 1.5)  # Increase mutation rate

#         # Regenerate if stagnation occurs
#         if stagnation_counter >= stagnation_limit:
#             print(f"Regenerating population at generation {generation} due to stagnation")
#             best_individual = population[np.argmin(fitness_values)]
#             population = generate_unique_population(population_size - 1, num_nodes)
#             population.append(best_individual)
#             population_chunks = np.array_split(population, size)
#             stagnation_counter = 0
#     else:
#         population_chunks = None

#     # Broadcast new population if needed
#     sub_population = comm.scatter(population_chunks, root=0)

#     # Selection, crossover, and mutation
#     selected = select_in_tournament(sub_population, sub_fitness_values, tournament_size=6)  # Stronger selection
#     offspring = []
#     for i in range(0, len(selected), 2):
#         if i + 1 < len(selected):
#             parent1, parent2 = selected[i], selected[i + 1]
#             route1 = pmx_crossover(parent1[1:], parent2[1:])  # Use PMX crossover
#             offspring.append([0] + route1)  # Ensure depot is the start

#     mutated_offspring = [adaptive_mutate(route, mutation_rate) for route in offspring]

#     # Replacement
#     for i, idx in enumerate(np.argsort(sub_fitness_values)[::-1][:len(mutated_offspring)]):
#         sub_population[idx] = mutated_offspring[i]

#     # Ensure uniqueness
#     unique_population = set(tuple(ind) for ind in sub_population)
#     while len(unique_population) < len(sub_population):
#         individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
#         unique_population.add(tuple(individual))
#     sub_population = [list(individual) for individual in unique_population]

#     # Print progress from rank 0
#     if rank == 0:
#         print(f"Generation {generation}: Best fitness = {current_best_fitness}")

# # Gather final population at rank 0
# final_population = comm.gather(sub_population, root=0)

# # Rank 0 selects the best solution
# if rank == 0:
#     final_population = [ind for sublist in final_population for ind in sublist]  # Flatten
#     final_fitness_values = np.array([calculate_fitness(route, distance_matrix) for route in final_population])
#     best_idx = np.argmin(final_fitness_values)
#     best_solution = final_population[best_idx]

#     print("Best Solution:", best_solution)
#     print("Total Distance:", -final_fitness_values[best_idx])

#     end_time = time.time()
#     print(f"Execution Time: {end_time - start_time:.2f} seconds")



