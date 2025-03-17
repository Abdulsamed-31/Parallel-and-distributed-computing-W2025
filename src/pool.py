from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor
import time
import random
from .square import square

def sequential_square(random_list):
    """
    Compute squares of numbers sequentially.
    """
    start_time = time.time()
    result = [square(num) for num in random_list]
    sequential_time = time.time() - start_time
    print(f"\n[sequential]\n")
    print(f"Sequential time: {sequential_time:.5f} seconds")
    return result

def multiprocessing_process(random_list):
    """
    Compute squares of numbers using a fixed-size multiprocessing pool with chunking.
    """
    start_time = time.time()
    
    # Number of processes limited to the number of CPU cores (adjustable)
    pool_size = min(cpu_count(), 8)  # Limit the pool size to 8 processes for optimal performance

    # Use Pool with chunking for efficient task distribution
    chunk_size = len(random_list) // pool_size  # Dynamically calculate chunk size
    with Pool(pool_size) as pool:
        result = pool.map(square, random_list)

    multiprocessing_time = time.time() - start_time
    print(f"\n[Multiprocessing]\n")
    print(f"(fixed-size pool) time: {multiprocessing_time:.5f} seconds")

def multiprocessing_pool_map(random_list):
    """
    Compute squares of numbers using Pool with map() and a fixed pool size.
    """
    start_time = time.time()
    
    # Limit number of processes based on available CPU cores
    pool_size = min(cpu_count(), 8)  # You can adjust this value
    with Pool(pool_size) as pool:
        result = pool.map(square, random_list)

    pool_map_time = time.time() - start_time
    print(f"pool with map() time: {pool_map_time:.5f} seconds")

def multiprocessing_pool_apply(random_list):
    """
    Compute squares of numbers using Pool with apply().
    """
    start_time = time.time()
    
    pool_size = min(cpu_count(), 8)  # Limiting pool size
    with Pool(pool_size) as pool:
        result = [pool.apply(square, (num,)) for num in random_list]

    pool_apply_time = time.time() - start_time
    print(f"pool with apply() time: {pool_apply_time:.5f} seconds")


def multiprocessing_pool_apply_async(random_list):
    """
    Compute squares of numbers using Pool with apply_async() to speed up task execution.
    """
    start_time = time.time()
    
    pool_size = 8  # Number of processes in the pool
    with Pool(pool_size) as pool:
        results = []
        
        # Use apply_async to run tasks asynchronously
        for num in random_list:
            result = pool.apply_async(square, (num,))
            results.append(result)
        
        # Wait for all tasks to complete and get the result
        result_values = [result.get() for result in results]
    
    pool_apply_async_time = time.time() - start_time
    print(f"pool with apply_async() time: {pool_apply_async_time:.5f} seconds")


def process_pool_executor(random_list):
    """
    Compute squares of numbers using ProcessPoolExecutor.
    """
    start_time = time.time()
    
    # Use a fixed-size pool based on system's available CPU cores
    with ProcessPoolExecutor(max_workers=min(cpu_count(), 8)) as executor:
        result = list(executor.map(square, random_list))

    futures_time = time.time() - start_time
    print(f"ProcessPoolExecutor time: {futures_time:.5f} seconds\n")
