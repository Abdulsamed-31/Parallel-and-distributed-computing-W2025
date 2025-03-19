
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

--------Identifying Parts for Parallelization--------

In the Genetic Algorithm (GA), the most computationally expensive operations are:

Fitness Evaluation (calculate_fitness) → Each individual in the population is evaluated, which is independent of others. (Ideal for parallelization!)

Selection (select_in_tournament) → Can be run in parallel for multiple tournaments.

Crossover & Mutation (order_crossover, mutate) → Independent operations that can be computed simultaneously.

Population Update → Individuals are updated independently, which allows parallel processing.

Why these choices?

These operations involve large-scale repetitive computations that don’t depend on sequential execution.

--------Outcome of Sequential and Parallelization--------

Sequential Outcome:

    Regenerating population at generation 199 due to stagnation
    Best Solution: [0, 12, 7, 15, 18, 31, 28, 5, 3, 6, 9, 23, 22, 20, 1, 2, 10, 25, 13, 29, 11, 30, 8, 21, 4, 19, 14, 26, 17, 27, 16, 24]
    Total Distance: -1800547.0
    Execution Time: 24.40 seconds

Parallelized Outcome:

    🔹 Best Solution: [0, 5, 1, 19, 16, 14, 7, 12, 3, 11, 15, 17, 4, 2, 10, 6, 13, 18, 9, 8]
    Total Distance: 1100670.0
    Execution Time: 20.18 seconds

    