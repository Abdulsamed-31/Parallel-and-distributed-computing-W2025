## Parallelized Genetic Algorithm for Route Optimization


## AUTHOR: 

    OUSSAMA ABDULSAMED MEDEBBER
    
### STUDENT ID: 

    60102334

## EXECUTION CODE:

multiple process, multiple machines

    mpirun -np 2 --hostfile machines.txt python3 main.py  
    
multiple process, same machine

    mpiexec -n 4 python main.py   


                                                             --------Description of trial code--------

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


                                                    --------Identifying Parts for Parallelization-------
                                                    -

In the Genetic Algorithm (GA), the most computationally expensive operations are:

    Fitness Evaluation (calculate_fitness) → Each individual in the population is evaluated, which is independent of others. (Ideal for parallelization!)

    Selection (select_in_tournament) → Can be run in parallel for multiple tournaments.

    Crossover & Mutation (order_crossover, mutate) → Independent operations that can be computed simultaneously.

    Population Update → Individuals are updated independently, which allows parallel processing.

Why these choices?

    These operations involve large-scale repetitive computations that don’t depend on sequential execution.
    

                                                                    --------OUTCOMES--------

Sequential Outcome:

    Generation 198: Best calculate_fitness = 1187.0
    Best Solution: [0, 25, 20, 30, 29, 31, 19, 28, 11, 9, 24, 27, 3, 14, 10, 12, 18, 23, 7, 22, 5, 4, 13, 15, 2, 8, 17, 1, 6, 26, 21, 16]
    
    Total Distance: -1187.0
    Execution Time: 23.50 seconds

Parallelized + hypertuning Outcome:

    Generation 198: Best fitness = 678.0
    Best Solution: [0, 16, 4, 13, 8, 2, 6, 12, 10, 11, 19, 3, 14, 17, 9, 7, 1, 5, 18, 15]
    
    Total Distance: -707.0
    Execution Time: 6.03 seconds

Running on different machines:

    Generation 199: Best fitness = 627.0
    Best Solution: [np.int64(0), np.int64(10), np.int64(3), np.int64(4), np.int64(7), np.int64(19), np.int64(9), np.int64(11), np.int64(12), np.int64(13), np.int64(18), np.int64(15), np.int64(2), np.int64(14), np.int64(8), np.int64(6), np.int64(16), np.int64(1), np.int64(17), np.int64(5)]
    
    Total Distance: -680.0
    Execution Time: 6.47 seconds

Running with multiple cars (4).

    Generation 199: Best fitness = 247.0
    Best Solution: [[0, np.int64(16), np.int64(11), np.int64(15), np.int64(6), np.int64(4)], [0, np.int64(7), np.int64(12), np.int64(8), np.int64(14), np.int64(10)], [0, np.int64(18), np.int64(2), np.int64(9), np.int64(5), np.int64(13)], [0, np.int64(1), np.int64(17), np.int64(19), np.int64(3)]]
    
    Total Distance: -247.0
    Execution Time: 35.03 seconds

Running with multiple cars (4) on different machines.

    Generation 199: Best fitness = 257.0
    Best Solution: [[0, np.int64(7), np.int64(8), np.int64(6), np.int64(12), np.int64(1), np.int64(9), np.int64(5)], [0, np.int64(4), np.int64(18), np.int64(19), np.int64(11), np.int64(15), np.int64(13)], [0, np.int64(3), np.int64(16), np.int64(2), np.int64(14), np.int64(10), np.int64(17)]]
    
    Total Distance: -257.0
    Execution Time: 39.13 seconds


    

                                                                    --------Algorithm Enhancement--------
                                                                    
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

    

                                                                    --------Adding more cars--------
                                                                    
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





    




    