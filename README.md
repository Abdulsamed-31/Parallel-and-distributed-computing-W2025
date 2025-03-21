# Assignment 1 - Multiprocessing                                               

### Name

    Oussama Medebber

### Student ID

    60102334

## OUTPUT

# Square Program with 10^6 numbers

## sequential

    Sequential time: 0.05349 seconds

## Multiprocessing

    (fixed-size pool) time: 0.07797 seconds
    pool with map() time: 0.07919 seconds
    pool with apply_async() time: 54.51268 seconds
    pool with apply() time: 173.33328 seconds
    ProcessPoolExecutor time: 104.74520 seconds


# Square Program with 10^7 numbers

### sequential

    Sequential time: 0.04317 seconds

### Multiprocessing

    (fixed-size pool) time: 0.17218 seconds
    pool with map() time: 0.16744 seconds
    pool with apply_async() time: 54.94505 seconds
    
    pool with apply() time: 173.40405 seconds
    ProcessPoolExecutor time: 111.78266 seconds


### Process Synchronization with Semaphores

    Process-65: Waiting for a connection
    Process-65: Acquired Connection-2
    Process-66: Waiting for a connection
    Process-66: Acquired Connection-2
    Process-67: Waiting for a connection
    Process-67: Acquired Connection-2
    Process-68: Waiting for a connection
    Process-69: Waiting for a connection
    Process-70: Waiting for a connection
    Process-71: Waiting for a connection
    Process-72: Waiting for a connection
    Process-73: Waiting for a connection
    Process-74: Waiting for a connection
    Process-66: Releasing Connection-2
    Process-68: Acquired Connection-2
    Process-67: Releasing Connection-2
    Process-69: Acquired Connection-2
    Process-65: Releasing Connection-2
    Process-70: Acquired Connection-2
    Process-68: Releasing Connection-2
    Process-71: Acquired Connection-2
    Process-69: Releasing Connection-2
    Process-72: Acquired Connection-2
    Process-70: Releasing Connection-2
    Process-73: Acquired Connection-2
    Process-71: Releasing Connection-2
    Process-74: Acquired Connection-2
    Process-73: Releasing Connection-2
    Process-72: Releasing Connection-2
    Process-74: Releasing Connection-2


