import numpy as np

def calculate_squares(start, end):
    """Calculate the squares of numbers from start to end (inclusive)."""
    return np.array([i ** 2 for i in range(start, end + 1)])
