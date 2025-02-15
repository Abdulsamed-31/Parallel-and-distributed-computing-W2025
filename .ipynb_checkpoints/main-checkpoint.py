import time
from src.thread_parallel_sum import *
from src.multiprocessing_parallel_sum import *
from src.sequential_sum import *

# Function to compute speedup, efficiency, Amdahl's and Gustafson's speedups
def compute_metrics(sequential_time, parallel_time, num_parallel):
    # Speedup
    speedup = sequential_time / parallel_time
    
    # Efficiency
    efficiency = speedup / num_parallel
    
    # Fraction of parallelizable task (let's assume 80% parallelizable)
    p = 0.8
    
    # Amdahl's Law Speedup
    amdahls_speedup = 1 / ((1 - p) + (p / num_parallel))
    
    # Gustafson's Law Speedup
    gustafsons_speedup = num_parallel - (1 - p) * num_parallel
    
    return speedup, efficiency, amdahls_speedup, gustafsons_speedup

def main():
    n = 10**7  # Example: sum of numbers from 1 to 10 million
    num_threads = 4
    num_processes = 4
    
    # Sequential version
    start_time = time.time()
    sequential_total = sequential_sum(n)
    sequential_time = time.time() - start_time
    
    # Parallel (Threading) version
    print("\nThreading parallel")
    parallel_total, parallel_time = parallel_sum(n, num_threads)
    
    # Multiprocessing version
    print("\nMultiprocessing parallel")
    multiprocessing_total, multiprocessing_time = multiprocessing_sum(n, num_processes)
    
    # Compute metrics for each case
    thread_speedup, thread_efficiency, thread_amdahls, thread_gustafsons = compute_metrics(sequential_time, parallel_time, num_threads)
    process_speedup, process_efficiency, process_amdahls, process_gustafsons = compute_metrics(sequential_time, multiprocessing_time, num_processes)

    # Print results for sequential
    print("\n")
    print(f"Sequential sum: {sequential_total}")
    print(f"Parallel sum (Threading): {parallel_total}")
    print(f"Multiprocessing sum: {multiprocessing_total}")
    print(f"Sequential execution time: {sequential_time:.6f} seconds")
    print(f"Parallel execution time (Threading): {parallel_time:.6f} seconds")
    print(f"Multiprocessing execution time: {multiprocessing_time:.6f} seconds")
    
    # Print reesults for Threading
    print("\nThreaded Execution Metrics:")
    print(f"Speedup (Threading): {thread_speedup:.6f}")
    print(f"Efficiency (Threading): {thread_efficiency:.6f}")
    print(f"Amdahl's Law Speedup (Threading): {thread_amdahls:.6f}")
    print(f"Gustafson's Law Speedup (Threading): {thread_gustafsons:.6f}")
    
    # Print results for Multiprocessing
    print("\nMultiprocessing Execution Metrics:")
    print(f"Speedup (Multiprocessing): {process_speedup:.6f}")
    print(f"Efficiency (Multiprocessing): {process_efficiency:.6f}")
    print(f"Amdahl's Law Speedup (Multiprocessing): {process_amdahls:.6f}")
    print(f"Gustafson's Law Speedup (Multiprocessing): {process_gustafsons:.6f}")

if __name__ == "__main__":
    main()
