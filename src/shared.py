# Synchronization primitives
lock = threading.RLock()
condition = threading.Condition(lock)

# Shared resources
latest_temperatures = {}
temperature_averages = {}