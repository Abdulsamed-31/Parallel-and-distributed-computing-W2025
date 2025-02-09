import time
from src.tasks import *
from src.threads import run_threads
from src.multiprocessor import run_multiprocessing
from src.tasks import *

# Measure sequential execution
def run_sequential():
    total_start_time = time.time()
    
    num_items = 10000
    
    # Sequential execution of the functions
    join_random_letters(0, num_items)
    add_random_numbers(0, num_items)
    
    total_end_time = time.time()
    return total_end_time - total_start_time

def performance_analysis():
    # Run sequential case to get baseline time
    seq_time = run_sequential()
    print(f"Sequential execution time: {seq_time} seconds")
    
    # Run threading case
    threading_time = run_threads()

    # Run multiprocessing case
    multiprocessing_time = run_multiprocessing()

    # Calculate speedups
    speedup_threads = seq_time / threading_time
    speedup_multiprocessing = seq_time / multiprocessing_time
    
    # Calculate efficiency
    num_threads = 4  # Two threads for each function
    num_processes = 4  # Two processes for each function
    
    efficiency_threads = speedup_threads / num_threads
    efficiency_multiprocessing = speedup_multiprocessing / num_processes
    
    # Assume P (parallelizable portion) to be around 0.95 (assuming 95% of the task is parallelizable)
    P = 0.95

    # Amdahl's Law for speedup (assuming 4 workers, 4 threads or processes)
    amdahl_speedup_threads = 1 / ((1 - P) + (P / num_threads))
    amdahl_speedup_multiprocessing = 1 / ((1 - P) + (P / num_processes))
    
    # Gustafson's Law for speedup (assuming N workers)
    gustafson_speedup_threads = num_threads - ((1 - P) * num_threads)
    gustafson_speedup_multiprocessing = num_processes - ((1 - P) * num_processes)

    # Print results
    print("\nPerformance Analysis:")
    print(f"Speedup (Threads): {speedup_threads}")
    print(f"Speedup (Multiprocessing): {speedup_multiprocessing}")
    
    print(f"Efficiency (Threads): {efficiency_threads}")
    print(f"Efficiency (Multiprocessing): {efficiency_multiprocessing}")
    
    print(f"Amdahl's Speedup (Threads): {amdahl_speedup_threads}")
    print(f"Amdahl's Speedup (Multiprocessing): {amdahl_speedup_multiprocessing}")
    
    print(f"Gustafson's Speedup (Threads): {gustafson_speedup_threads}")
    print(f"Gustafson's Speedup (Multiprocessing): {gustafson_speedup_multiprocessing}")

# Run the performance analysis
performance_analysis()