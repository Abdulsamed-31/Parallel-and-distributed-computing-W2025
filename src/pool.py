
from multiprocessing import Pool, Process
from concurrent.futures import ProcessPoolExecutor
import time
import random
from .square import square

def sequential_square(random_list):
    """
    #Compute squares of numbers sequentially.
    """
    start_time = time.time()
    result = [square(num) for num in random_list]
    sequential_time = time.time() - start_time
    print(f"Sequential time: {sequential_time:.5f} seconds")
    return result

def multiprocessing_process(random_list):
    """
    Compute squares of numbers using one process for each number.
    """
    start_time = time.time()

    def square_process(num):
        square(num)

    processes = []
    for num in random_list:
        process = Process(target=square_process, args=(num,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    multiprocessing_time = time.time() - start_time
    print(f"Multiprocessing (one process per number) time: {multiprocessing_time:.5f} seconds")

def multiprocessing_pool_map(random_list):
    """
    Compute squares of numbers using Pool with map.
    """
    start_time = time.time()
    with Pool() as pool:
        result = pool.map(square, random_list)
    pool_map_time = time.time() - start_time
    print(f"Multiprocessing pool with map() time: {pool_map_time:.5f} seconds")

def multiprocessing_pool_apply(random_list):
    """
    Compute squares of numbers using Pool with apply.
    """
    start_time = time.time()
    with Pool() as pool:
        result = [pool.apply(square, (num,)) for num in random_list]
    pool_apply_time = time.time() - start_time
    print(f"Multiprocessing pool with apply() time: {pool_apply_time:.5f} seconds")

def process_pool_executor(random_list):
    """
    Compute squares of numbers using ProcessPoolExecutor.
    """
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        result = list(executor.map(square, random_list))
    futures_time = time.time() - start_time
    print(f"ProcessPoolExecutor time: {futures_time:.5f} seconds")
