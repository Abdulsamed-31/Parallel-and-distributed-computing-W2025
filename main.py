from mpi4py import MPI
import numpy as np
import time
from src.square import calculate_squares
from mpi4py import MPI
import numpy as np
import time
from src.virus_simulation import simulate_virus_spread


def squareMain():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Define n (number up to which we want to calculate squares)
    n = 100  # Example value
    start_time = time.time()

    # Split the work among the processes
    numbers_per_process = n // size
    start = rank * numbers_per_process + 1
    end = start + numbers_per_process - 1

    if rank == size - 1:
        end = n  # Last process handles the remaining numbers

    # Calculate squares for the assigned range
    squares = calculate_squares(start, end)

    # Gather all results at root (rank 0)
    all_squares = comm.gather(squares, root=0)

    if rank == 0:
        # Flatten the list of squares
        all_squares = np.concatenate(all_squares)
        print(f"Total number of squares: {len(all_squares)}")
        print(f"Last square: {all_squares[-1]}")
        print(f"Time taken: {time.time() - start_time} seconds")

def virusMain():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Define parameters
    population_size = 100
    spread_chance = 0.3
    vaccination_rate = np.random.uniform(0.1, 0.5)
    
    # Initialize population
    population = np.zeros(population_size)
    if rank == 0:
        infected_indices = np.random.choice(population_size, int(0.1 * population_size), replace=False)
        population[infected_indices] = 1

    # Simulate virus spread for 10 time steps
    for _ in range(10):
        population = simulate_virus_spread(population, spread_chance, vaccination_rate)

        if rank != 0:
            comm.send(population, dest=0)
        else:
            for i in range(1, size):
                received_data = comm.recv(source=i)
                population += received_data  # Combine results

    # Calculate and print infection rate
    total_infected = np.sum(population)
    infection_rate = total_infected / population_size
    print(f"Process {rank} Infection Rate: {infection_rate:.2f}")

if __name__ == "__main__":
    squareMain()
    virusMain()
