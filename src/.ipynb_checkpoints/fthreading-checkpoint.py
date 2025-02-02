import threading
import time
from src.functions import *


# Measure the total time for both operations
def fthreading():
    total_start_time = time.time()
    
# Create threads for both functions
    thread_1 = threading.Thread(target=add_random_numbers)
    thread_2 = threading.Thread(target=add_random_numbers)
    #thread_numbers = threading.Thread(target=add_random_numbers)
    
# Start the threads
    thread_1.start()
    thread_2.start()
    
# Wait for all threads to complete
    thread_1.join()
    thread_2.join()
    
    total_end_time = time.time()
    print(f"Total time taken (Threads): {total_end_time - total_start_time} seconds")



