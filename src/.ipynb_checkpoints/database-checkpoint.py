
import time
import random
from multiprocessing import Semaphore

class ConnectionPool:
    def __init__(self, num_connections=3):
        self.semaphore = Semaphore(num_connections)
        self.connections = [f"Connection-{i}" for i in range(num_connections)]

    def get_connection(self):
        self.semaphore.acquire()
        return self.connections.pop()

    def release_connection(self, connection):
        self.connections.append(connection)
        self.semaphore.release()

def access_database(pool):
    connection = pool.get_connection()
    print(f"Process {connection} acquired a connection.")
    time.sleep(random.uniform(0.5, 2))  # Simulate work
    pool.release_connection(connection)
    print(f"Process {connection} released the connection.")

