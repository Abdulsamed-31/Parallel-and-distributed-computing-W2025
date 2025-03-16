# src/database.py

import random
import time
from multiprocessing import Semaphore, current_process  # Import current_process here

class ConnectionPool:
    def __init__(self, num_connections):
        """
        Initialize the ConnectionPool with a list of connections and a semaphore.
        """
        self.connections = [f"Connection-{i}" for i in range(num_connections)]
        self.semaphore = Semaphore(num_connections)

    def get_connection(self):
        """
        Get a connection from the pool, ensuring only a limited number of processes access the pool.
        """
        self.semaphore.acquire()
        connection = self.connections.pop()
        return connection

    def release_connection(self, connection):
        """
        Release a connection back into the pool.
        """
        self.connections.append(connection)
        self.semaphore.release()

def access_database(connection_pool):
    """
    Simulate a process accessing the database.
    """
    # Get the current process name
    process_name = current_process().name
    print(f"Process {process_name}: Waiting for a connection")
    
    connection = connection_pool.get_connection()
    print(f"Process {process_name}: Acquired {connection}")
    
    # Simulate work with a sleep
    time.sleep(random.uniform(0.5, 2))
    
    print(f"Process {process_name}: Releasing {connection}")
    connection_pool.release_connection(connection)
