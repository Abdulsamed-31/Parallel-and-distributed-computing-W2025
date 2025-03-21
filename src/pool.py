
import numpy as np
import time
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor
import numba

# JIT-compiled function for fast parallel execution of squaring operations
@numba.njit(fastmath=True, parallel=True)
def parallel_square_array(arr):
    """
    Compute the square of each element in the given NumPy array.
    Uses Numba for JIT compilation and parallel execution.
    
    Parameters:
        arr (numpy.ndarray): Input array of numbers.
    
    Returns:
        numpy.ndarray: Squared values of the input array.
    """
    return arr * arr  # Vectorized NumPy operation (faster than loops)

def sequential_for_loop(random_list):
    """
    Compute squares sequentially using Numba-optimized function.
    
    Parameters:
        random_list (numpy.ndarray): Array of numbers to be squared.
    
    Returns:
        numpy.ndarray: Squared values of the input array.
    """
    start_time = time.time()
    result = parallel_square_array(random_list)  # Optimized vectorized function
    print(f"Sequential for loop time: {time.time() - start_time:.5f} seconds")
    return result

def multiprocessing_pool_map(random_list):
    """
    Compute squares in parallel using multiprocessing Pool with map().
    
    Parameters:
        random_list (numpy.ndarray): Array of numbers to be squared.
    
    Returns:
        numpy.ndarray: Squared values of the input array.
    """
    start_time = time.time()
    pool_size = min(cpu_count(), 8)  # Use up to 8 CPU cores to balance performance
    chunk_size = len(random_list) // (2 * pool_size)  # Optimize workload distribution

    with Pool(pool_size) as pool:
        # Split the array into chunks and process them in parallel
        result = pool.map(parallel_square_array, np.array_split(random_list, pool_size), chunksize=chunk_size)

    print(f"Multiprocessing pool map() time: {time.time() - start_time:.5f} seconds")
    return np.concatenate(result)  # Merge the results back into a single array

def multiprocessing_pool_apply(random_list):
    """
    Compute squares in parallel using multiprocessing Pool with apply().
    This version is much slower than starmap() because it runs one task at a time.
    
    Parameters:
        random_list (numpy.ndarray): Array of numbers to be squared.
    
    Returns:
        numpy.ndarray: Squared values of the input array.
    """
    start_time = time.time()
    pool_size = min(cpu_count(), 8)  # Limit the number of parallel processes
    
    with Pool(pool_size) as pool:
        # Using apply(), which runs one task at a time (VERY SLOW)
        result = [pool.apply(parallel_square_array, (chunk,)) for chunk in np.array_split(random_list, pool_size)]
    
    print(f"Multiprocessing pool apply() time: {time.time() - start_time:.5f} seconds")
    return np.concatenate(result)  # Merge chunks back into a single array


def multiprocessing_pool_apply_async(random_list):
    """
    Compute squares in parallel using multiprocessing Pool with apply_async().
    
    Parameters:
        random_list (numpy.ndarray): Array of numbers to be squared.
    
    Returns:
        numpy.ndarray: Squared values of the input array.
    """
    start_time = time.time()
    pool_size = min(cpu_count(), 8)  # Use up to 8 CPU cores

    with Pool(pool_size) as pool:
        # Apply async processing for each chunk and retrieve results efficiently
        results = [pool.apply_async(parallel_square_array, (chunk,)) for chunk in np.array_split(random_list, pool_size)]
        result_values = [res.get() for res in results]  # Collect results as processes complete

    print(f"Multiprocessing pool apply_async() (optimized) time: {time.time() - start_time:.5f} seconds")
    return np.concatenate(result_values)  # Merge results into a single array

def process_pool_executor(random_list):
    """
    Compute squares using ProcessPoolExecutor for parallel processing.
    
    Parameters:
        random_list (numpy.ndarray): Array of numbers to be squared.
    
    Returns:
        numpy.ndarray: Squared values of the input array.
    """
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        # Efficiently distribute workload using map()
        result = list(executor.map(parallel_square_array, np.array_split(random_list, cpu_count())))

    print(f"ProcessPoolExecutor time: {time.time() - start_time:.5f} seconds")
    return np.concatenate(result)  # Merge results back into a single array

