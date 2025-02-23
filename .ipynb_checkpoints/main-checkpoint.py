import random
import time
import threading

# Global shared data
latest_temperatures = {}
temperature_averages = {}

# Lock for synchronizing access to shared data
lock = threading.RLock()
condition = threading.Condition(lock)

def main():
    initialize_display()

    # Create and start threads for simulate_sensor
    for i in range(3):  # Assuming 3 sensors
        threading.Thread(target=simulate_sensor, args=(i,), daemon=True).start()

    # Create and start the processing thread
    threading.Thread(target=process_temperatures, daemon=True).start()

    # Create and start the display update thread
    threading.Thread(target=update_display, daemon=True).start()

    # Keep the main thread running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()