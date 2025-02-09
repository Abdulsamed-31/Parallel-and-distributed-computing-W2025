import threading
import time
import random
import string
from src.tasks import *

# Measure the total time for both operations
def run_threads():
    total_start_time = time.time()

    # Number of items for each task
    num_items = 10000
    split_size = num_items // 2

    # Create threads for both functions, dividing the work
    # Letters (2 threads)
    thread_letters1 = threading.Thread(target=join_random_letters, args=(0, split_size))
    thread_letters2 = threading.Thread(target=join_random_letters, args=(split_size, num_items))

    # Numbers (2 threads)
    thread_numbers1 = threading.Thread(target=add_random_numbers, args=(0, split_size))
    thread_numbers2 = threading.Thread(target=add_random_numbers, args=(split_size, num_items))

    # Start the threads
    thread_letters1.start()
    thread_letters2.start()
    thread_numbers1.start()
    thread_numbers2.start()

    # Wait for all threads to complete
    thread_letters1.join()
    thread_letters2.join()
    thread_numbers1.join()
    thread_numbers2.join()

    total_end_time = time.time()
    print(f"Total time taken (threading): {total_end_time - total_start_time} seconds")
    return total_end_time - total_start_time