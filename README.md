# Parallelized Genetic Algorithm for Route Optimization


### AUTHOR: 

    OUSSAMA ABDULSAMED MEDEBBER
    
### STUDENT ID: 

    60102334

## EXECUTION CODE:

multiple process, multiple machines

    mpirun -np 2 --hostfile machines.txt python3 main.py  
    scp -r main.py city_distances_extended.csv src student@10.102.0.218:/home/student/Parallel-and-distributed-computing-W2025
    
multiple process, same machine

    mpiexec -n 4 python main.py   

## Description of trial code

Load Distance Matrix

    Reads a CSV file (city_distances.csv) containing the distances between cities.


Initialize Parameters

    Defines the number of cities, population size, number of generations, mutation rate, and stagnation limit.


Generate Initial Population

    Creates a unique population of routes, each starting at city 0 and randomly visiting all other cities.

Main Genetic Algorithm Loop (Runs for a fixed number of generations)

    Evaluate Fitness: Calculates the total travel distance for each route.
    Check for Stagnation: If no improvement occurs for stagnation_limit generations, the population is regenerated.
    Selection: Uses Tournament Selection to pick the best routes.
    Crossover: Applies Order Crossover (OX) to generate new routes.
    Mutation: Introduces small random changes to maintain genetic diversity.
    Replacement: Replaces weaker individuals in the population with new offspring.
    Ensure Uniqueness: Removes duplicate routes.

Output the Best Solution

    Identifies and prints the shortest route and its total distance.

Measure Execution Time

    Uses the time module to track how long the algorithm takes to run.


## Identifying Parts for Parallelization
                                                    

In the Genetic Algorithm (GA), the most computationally expensive operations are:

    Fitness Evaluation (calculate_fitness) → Each individual in the population is evaluated, which is independent of others. (Ideal for parallelization!)

    Selection (select_in_tournament) → Can be run in parallel for multiple tournaments.

    Crossover & Mutation (order_crossover, mutate) → Independent operations that can be computed simultaneously.

    Population Update → Individuals are updated independently, which allows parallel processing.

Why these choices?

    These operations involve large-scale repetitive computations that don’t depend on sequential execution.
    

## OUTCOMES
                                                                    

Sequential Outcome:

    Generation 198: Best calculate_fitness = 1187.0
    Best Solution: [0, 25, 20, 30, 29, 31, 19, 28, 11, 9, 24, 27, 3, 14, 10, 12, 18, 23, 7, 22, 5, 4, 13, 15, 2, 8, 17, 1, 6, 26, 21, 16]
    
    Total Distance: 1187.0
    Execution Time: 23.50 seconds

Parallelized + hypertuning Outcome:

    Generation 198: Best fitness = 678.0
    Best Solution: [0, 16, 4, 13, 8, 2, 6, 12, 10, 11, 19, 3, 14, 17, 9, 7, 1, 5, 18, 15]
    
    Total Distance: 707.0
    Execution Time: 6.03 seconds

Running on different machines:

    Generation 199: Best fitness = 627.0
    Best Solution: [np.int64(0), np.int64(10), np.int64(3), np.int64(4), np.int64(7), np.int64(19), np.int64(9), np.int64(11), np.int64(12), np.int64(13), np.int64(18), np.int64(15), np.int64(2), np.int64(14), np.int64(8), np.int64(6), np.int64(16), np.int64(1), np.int64(17), np.int64(5)]
    
    Total Distance: 680.0
    Execution Time: 6.47 seconds

Running with multiple cars (4).

    Generation 199: Best fitness = 247.0
    Best Solution: [[0, np.int64(16), np.int64(11), np.int64(15), np.int64(6), np.int64(4)], [0, np.int64(7), np.int64(12), np.int64(8), np.int64(14), np.int64(10)], [0, np.int64(18), np.int64(2), np.int64(9), np.int64(5), np.int64(13)], [0, np.int64(1), np.int64(17), np.int64(19), np.int64(3)]]
    
    Total Distance: 247.0
    Execution Time: 35.03 seconds

Running with multiple cars (4) on different machines multiple process.

    Generation 199: Best fitness = 257.0
    Best Solution: [[0, np.int64(7), np.int64(8), np.int64(6), np.int64(12), np.int64(1), np.int64(9), np.int64(5)], [0, np.int64(4), np.int64(18), np.int64(19), np.int64(11), np.int64(15), np.int64(13)], [0, np.int64(3), np.int64(16), np.int64(2), np.int64(14), np.int64(10), np.int64(17)]]
    
    Total Distance: 257.0
    Execution Time: 39.13 seconds

Running with multiple cars (4) on different machines single process.

    Generation 199: Best fitness = 205.0
    Best Solution: [[0, np.int64(16), np.int64(2), np.int64(6), np.int64(12), np.int64(18)], [0, np.int64(5), np.int64(13), np.int64(15), np.int64(8), np.int64(7)], [0, np.int64(9), np.int64(11), np.int64(4), np.int64(19), np.int64(17)], [0, np.int64(10), np.int64(3), np.int64(14), np.int64(1)]]
    
    Total Distance: 205.0
    Execution Time: 45.45 seconds



## Algorithm Enhancement
                                                                    
updated Functions:

calculate_fitness(route,distance_matrix)    ---->    calc_fitness_multiple_cars(route, distance_matrix, num_cars)

    Distributes deliveries among multiple vehicles.
    Supports multiple vehicles, leading to shorter individual routes.
    Balances workload to prevent a single car from handling all deliveries.

order_crossover(parent1, parent2)      ---->    pmx_crossover(parent1, parent2)

    Uses Partially Mapped Crossover (PMX), which preserves absolute positions.
    Ensures valid offspring without additional corrections.
    PMX ensures better gene inheritance, making it more effective for multi-car solutions.
    Eliminates post-processing steps, improving execution speed
    
mutate(route,mutation_rate = 0.1)      ---->    adaptive_mutate(route, mutation_rate, diversity_factor=0.2)

    Adjusts mutation rate based on population diversity.
    If improvement occurs, mutation decreases (to refine solutions).
    If stagnation occurs, mutation increases (to introduce diversity).
    Ensures mutation rate does not drop too low, maintaining exploration.
    Avoids getting stuck in local optima by adjusting mutation probability.
    Provides faster convergence with fewer unnecessary mutations

generate_unique_population(population_size, num_nodes)     ---->    generate_unique_population_multiple_cars(population_size, num_nodes, num_cars)
    
    Generates routes for multiple cars.
    Splits locations evenly across cars.
    Ensures each car has a unique, valid route.
    Uses tuple-based uniqueness to prevent duplicate solutions.
    Supports multiple vehicles, leading to shorter routes and better load balancing.

main function:

Parallelization:

    -Enhanced Code: Uses MPI for parallel execution across multiple machines.
    -Original Code: Runs sequentially on a single machine.

Multi-Car vs. Single-Car:

    -Enhanced Code: Supports multiple cars (4 cars) using calc_fitness_multiple_cars().
    -Original Code: Uses only one car for the entire route.

Crossover & Mutation:
    
    -Enhanced Code: Uses PMX crossover (better for route optimization) and adaptive mutation.
    -Original Code: Uses Order Crossover (OX) and fixed mutation rate.

Population Handling:
    
    -Enhanced Code: Generates multi-car routes (generate_unique_population_multiple_cars()).
    -Original Code: Creates single-car routes (generate_unique_population()).

Performance & Scalability:
    
    -Enhanced Code: Scales better with large problems, reduces execution time via parallelism.
    -Original Code: Slower but simpler, suitable for small-scale problems.

Overall: 

    The first Enahnced code is faster, more scalable, and optimized for multi-vehicle routing in a parallel environment,
    while the original is simpler and single-threaded for basic TSP problems.

    

## Adding more cars
                                                                    
 To modify the Genetic Algorithm (GA) for multiple cars, we need to:

    -Assign deliveries to multiple vehicles instead of just one.
    -Ensure each car has its own route while collectively minimizing total distance.
    -Balance the workload between cars to avoid one doing all the work.
    -Modify crossover and mutation to work with multiple vehicle paths.

    Total Distance: -257.0
    Execution Time: 39.13 seconds

    
 updated Functions:

    calculate_fitness_multiple_cars
    Generate_unique_popluation_multiple_cars


## PARALLELIZABLE CODE WITH ADAPTIVE MUTATE AND PMX_CROSSOVER (ONE CAR)
    
    from mpi4py import MPI
    import time
    import numpy as np
    import pandas as pd
    from src.genetic_algorithms_functions import (
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
        distance_matrix = pd.read_csv('city_distances_extended.csv').to_numpy()
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
        print("Total Distance:", final_fitness_values[best_idx])
    
        end_time = time.time()
        print(f"Execution Time: {end_time - start_time:.2f} seconds")
    
    
    
        




    