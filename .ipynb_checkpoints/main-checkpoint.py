
from src.fprocessing import fprocessing
from src.fthreading import fthreading

def main():
    # Call fprocessing to run the multiprocessing code
    print("Running fprocessing (Multiprocessing)...")
    fprocessing()

    # Call fthreading to run the threading code
    print("\nRunning fthreading (Threading)...")
    fthreading()

if __name__ == "__main__":
    main()
