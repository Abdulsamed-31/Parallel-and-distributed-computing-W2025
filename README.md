# Assignment 1 - Multiprocessing                                               

### Name

    Oussama Abdulsamed Medebber

### Student ID

    60102334

### Execution code

    python main.py

## OUTPUT
### Testing different approaches with 10^6 numbers

    Sequential for loop time: 0.85314 seconds
    Multiprocessing pool map() time: 0.59416 seconds
    Multiprocessing pool apply() time: 0.10825 seconds
    Multiprocessing pool apply_async() (optimized) time: 0.09515 seconds
    ProcessPoolExecutor time: 0.09082 seconds

#### Testing different approaches with 10^7 numbers

    Sequential for loop time: 0.01729 seconds
    Multiprocessing pool map() time: 0.69216 seconds
    Multiprocessing pool apply() time: 0.49592 seconds
    Multiprocessing pool apply_async() (optimized) time: 0.34410 seconds
    ProcessPoolExecutor time: 0.31492 seconds

### Process Synchronization with Semaphores

    Process Connection-2 acquired a connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 released the connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 released the connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 released the connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 released the connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 released the connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 released the connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 released the connection.
    Process Connection-2 acquired a connection.
    Process Connection-2 released the connection.
    Process Connection-2 released the connection.
    Process Connection-2 released the connection.

## Performance & Optimization

Execution time is fast due to NumPy vectorization and Numba JIT compilation.
instead of using standard Python loops, which are significantly slower.

## Multiprocessing Efficiency

Data processed in chunks (np.array_split), reducing overhead.
instead of sending individual numbers to processes, causing excessive inter-process communication.

## apply() Optimization

Optimizing apply() with starmap(), which is far more efficient for bulk processing.
starmap() is like map(), but supports multiple arguments → Efficient batch processing in parallel.

## Parallel Execution

parallelizes entire arrays with Numba (parallel_square_array).
Instead of parallelizes individual operations, causing inefficiencies.

## Better Process Distribution

optimal chunking (len(array) // (2 * pool_size)) for better load balancing.
This way we can avoid inefficiencies.

Conclusion
Due to Numba JIT, NumPy vectorization, optimized multiprocessing, and chunking strategies, The code is significantly faster

## What is Numba JIT:

Numba JIT (Just-In-Time Compilation) is a technique that compiles Python functions into highly optimized code. 
This significantly speeds up numerical computations, especially when working with loops and arrays.

Benefits of Numba JIT
Faster execution (up to 100x speedup for loops)
Parallel execution (@numba.njit(parallel=True)) enables multi-threading
Optimized CPU usage (fastmath=True for faster floating-point operations)
Works with NumPy arrays, making operations extremely efficient

## what is Numpy Vectorization:

NumPy vectorization refers to performing operations on entire arrays at once, rather than using Python loops. 
Vectorized operations are much faster because they leverage efficient C-based implementations.

Benefits of NumPy Vectorization
Avoids slow Python loops (operations happen in C, not Python)
Uses SIMD (Single Instruction, Multiple Data) optimizations
Makes code cleaner and easier to read

### What happens if more processes try to access the pool than there are available connections?

When more processes try to access the ConnectionPool than there are available connections, the extra processes are forced to wait until a connection becomes available.

The semaphore ensures that only a limited number of processes can access the pool at a time.
Waiting processes remain blocked until another process releases a connection.
Once a process releases a connection, one of the waiting processes acquires it and continues execution.
This prevents overloading the system by ensuring that only a fixed number of connections are used at any given time.

Example Scenario:
If the connection pool has 3 connections but 10 processes try to access it, only 3 processes will proceed while the remaining 7 will wait. As soon as a process releases a connection, the next waiting process takes it

### How does the semaphore prevent race conditions and ensure safe access to the connections?

A semaphore is a synchronization mechanism that controls access to shared resources by limiting the number of simultaneous accesses.

The semaphore count is set to the number of available connections (e.g., Semaphore(3) for 3 connections).
When a process wants a connection, it calls acquire() on the semaphore.
If a connection is available, the semaphore count decreases, and the process continues.
If no connections are available, the process is blocked (put on hold) until another process calls release() and frees up a connection.
This prevents multiple processes from accessing the same connection at the same time, avoiding data corruption or unexpected behavior
