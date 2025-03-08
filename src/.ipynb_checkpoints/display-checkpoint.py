import threading
import random
import time

# Synchronization primitives
lock = threading.RLock()
condition = threading.Condition(lock)

# Shared resources
latest_temperatures = {}
temperature_averages = {}

# Number of sensors
NUM_SENSORS = 3

# Initialize the display layout with placeholders
def initialize_display():
    print("Current temperatures:")
    print("Latest Temperatures: ", end="")
    for i in range(NUM_SENSORS):
        print(f"Sensor {i}: --°C ", end="")
    print()

    # Display placeholders for sensor averages
    for i in range(NUM_SENSORS):
        print(f"Sensor {i} Average: --°C ", end="")
    print("\n")

# Update the display with the latest temperatures and averages
def update_display():
    while True:
        with condition:
            condition.wait()  # Wait for data to be updated

        display_str = "Current temperatures:\nLatest Temperatures: "
        with lock:
            for i in range(NUM_SENSORS):
                temp = latest_temperatures.get(i, "--")
                display_str += f"Sensor {i}: {temp}°C "

        display_str += "\n"
        with lock:
            for i in range(NUM_SENSORS):
                avg = temperature_averages.get(f'sensor_{i}_average', "--")
                display_str += f"Sensor {i} Average: {avg}°C "

        print("\r" + display_str, end="")  # Update the console output
        time.sleep(1)