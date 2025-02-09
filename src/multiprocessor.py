import multiprocessing
import time
import random
import string
from src.tasks import *

# Measure the total time for both operations
def run_multiprocessing():
    total_start_time = time.time()

    # Number of items for each task
    num_items = 10000
    split_size = num_items // 2  # Dividing tasks equally

    # Create processes for both functions, dividing the work
    # Letters (2 processes)
    process_letters1 = multiprocessing.Process(target=join_random_letters, args=(0, split_size))
    process_letters2 = multiprocessing.Process(target=join_random_letters, args=(split_size, num_items))

    # Numbers (2 processes)
    process_numbers1 = multiprocessing.Process(target=add_random_numbers, args=(0, split_size))
    process_numbers2 = multiprocessing.Process(target=add_random_numbers, args=(split_size, num_items))

    # Start the processes
    process_letters1.start()
    process_letters2.start()
    process_numbers1.start()
    process_numbers2.start()

    # Wait for all processes to complete
    process_letters1.join()
    process_letters2.join()
    process_numbers1.join()
    process_numbers2.join()

    total_end_time = time.time()
    print(f"Total time taken (multiprocessing): {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time

