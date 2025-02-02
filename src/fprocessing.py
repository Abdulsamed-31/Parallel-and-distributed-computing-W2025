import multiprocessing
import time
from functions import *

# Measure the total time for both operations
def fprocessing():
    total_start_time = time.time()

    # Create processes for both functions
    process_1 = multiprocessing.Process(target=join_random_letters)
    process_2 = multiprocessing.Process(target=join_random_letters)
    #process_numbers = multiprocessing.Process(target=add_random_numbers)

    # Start the processes
    process_1.start()
    process_2.start()

    # Wait for all processes to complete
    process_1.join()
    process_2.join()

    total_end_time = time.time()
    print(f"Total time taken(Process): {total_end_time - total_start_time} seconds")
