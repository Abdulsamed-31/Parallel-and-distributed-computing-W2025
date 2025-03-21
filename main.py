

import numpy as np
import time
from multiprocessing import Pool, cpu_count, Process
from concurrent.futures import ProcessPoolExecutor
from src.pool import (
    sequential_for_loop,
    multiprocessing_pool_map,
    multiprocessing_pool_apply,
    multiprocessing_pool_apply_async,
    process_pool_executor
)
from src.database import ConnectionPool, access_database

def main():
    random_list = np.random.randint(1, 100, size=10**6)
    print("\n-----Testing different approaches with 10^6 numbers-----")
    sequential_for_loop(random_list)
    multiprocessing_pool_map(random_list)
    multiprocessing_pool_apply(random_list)
    multiprocessing_pool_apply_async(random_list)
    process_pool_executor(random_list)

    random_list_10e7 = np.random.randint(1, 100, size=10**7)
    print("\n-----Testing different approaches with 10^7 numbers-----")
    sequential_for_loop(random_list_10e7)
    multiprocessing_pool_map(random_list_10e7)
    multiprocessing_pool_apply(random_list_10e7)
    multiprocessing_pool_apply_async(random_list_10e7)
    process_pool_executor(random_list_10e7)

    print("\n-----Process Synchronization with Semaphores-----")
    pool = ConnectionPool(num_connections=3)
    processes = [Process(target=access_database, args=(pool,)) for _ in range(10)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()

if __name__ == "__main__":
    main()


