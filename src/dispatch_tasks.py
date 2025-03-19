from src.tasks import power

def dispatch():
    results_objs = [
        power.apply_async((num, 2)) for num in range(1, 1001)
    ]
    results = [
        result.get() for result in results_objs
    ]
    return results
