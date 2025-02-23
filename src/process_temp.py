def process_temperatures():
    while True:
        with lock:
            total = sum(latest_temperatures.values())
            count = len(latest_temperatures)
            if count > 0:
                average = total / count
                for i in range(count):
                    temperature_averages[f"sensor_{i}_average"] = average
        with condition:
            condition.notify_all()  # Notify the display thread to update
        time.sleep(1)