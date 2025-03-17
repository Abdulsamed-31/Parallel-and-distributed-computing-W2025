

import random
from src.pool import (
    sequential_square,
    multiprocessing_process,
    multiprocessing_pool_map,
    multiprocessing_pool_apply_async,
    multiprocessing_pool_apply,
    process_pool_executor
)

from multiprocessing import Process
from src.database import ConnectionPool, access_database

def main_square_program():
    """
    Main function to run the square computation program with different methods.
    """
    # Create a random list of 10^6 numbers
    random_list = [random.randint(1, 100) for _ in range(10**6)]

    # Test sequential approach
    sequential_square(random_list)

    # Test multiprocessing (one process per number)
    multiprocessing_process(random_list)

    # Test multiprocessing pool with map()
    multiprocessing_pool_map(random_list)

    # Test multiprocessing pool with apply()
    multiprocessing_pool_apply_async(random_list)

    # Test multiprocessing pool with apply()
    multiprocessing_pool_apply(random_list)

    # Test ProcessPoolExecutor
    process_pool_executor(random_list)

def main_database_simulation():
    """
    Main function to run the database connection pool simulation.
    """
    # Create a connection pool with 3 connections
    pool = ConnectionPool(num_connections=3)

    # Create 10 processes to simulate database access
    processes = []
    for i in range(10):  # Create 10 processes
        process = Process(target=access_database, args=(pool,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    print("\n-----Square Program with 10^6 numbers-----")
    main_square_program()

    print("\n-----Square Program with 10^7 numbers-----")
    random_list_10e7 = [random.randint(1, 100) for _ in range(10**7)]
    main_square_program()

    print("\n-----Process Synchronization with Semaphores-----")
    main_database_simulation()


