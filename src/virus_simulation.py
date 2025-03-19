import numpy as np

def simulate_virus_spread(population, spread_chance, vaccination_rate):
    """Simulate virus spread for one time step."""
    new_population = population.copy()
    for i in range(len(population)):
        if population[i] == 1:
            # If the individual is infected, attempt to spread the virus
            for j in range(len(population)):
                if population[j] == 0 and np.random.random() < spread_chance * (1 - vaccination_rate):
                    new_population[j] = 1
    return new_population
