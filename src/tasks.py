import random
import string

def join_random_letters(start, end):
    letters = [random.choice(string.ascii_letters) for _ in range(start, end)]
    joined_letters = ''.join(letters)
    #print(f"Joined Letters Task Done (from {start} to {end})")

# Function to add random numbers, modified to accept a range
def add_random_numbers(start, end):
    numbers = [random.randint(1, 100) for _ in range(start, end)]
    total_sum = sum(numbers)
    #print(f"Add Numbers Task Done (from {start} to {end})")