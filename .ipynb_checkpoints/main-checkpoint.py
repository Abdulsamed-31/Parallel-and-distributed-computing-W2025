from src.fprocessing import *
from src.fthreading import *
from src.functions import *


def main():
    print("Starting multiprocessing...")
    fprocessing()  # This will run the multiprocessing version

    print("\nStarting threading...")
    fthreading()  # This will run the threading version

if __name__ == "__main__":
    main()
