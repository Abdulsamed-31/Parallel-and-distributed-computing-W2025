# Simulate sensor readings
def simulate_sensor(sensor_id):
    while True:
        temperature = random.randint(15, 40)  # Random temperature between 15°C and 40°C
        with lock:
            latest_temperatures[sensor_id] = temperature
        with condition:
            condition.notify_all()  # Notify other threads that the temperature has been updated
        time.sleep(1)