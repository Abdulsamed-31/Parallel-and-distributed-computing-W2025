import threading, random, time
from src.display import *
from src.process_temp import *
from src.sensor import *


# Main function to start threads
def main():
    # Initialize display
    initialize_display()

    # Create and start sensor threads
    sensor_threads = []
    for i in range(NUM_SENSORS):
        t = threading.Thread(target=simulate_sensor, args=(i,))
        t.daemon = True
        sensor_threads.append(t)
        t.start()

    # Create and start temperature processing thread
    processing_thread = threading.Thread(target=process_temperatures)
    processing_thread.daemon = True
    processing_thread.start()

    # Create and start display update thread
    display_thread = threading.Thread(target=update_display)
    display_thread.daemon = True
    display_thread.start()

    # Keep the main thread alive to allow daemon threads to run
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
