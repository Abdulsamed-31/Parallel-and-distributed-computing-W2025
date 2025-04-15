
import argparse
from mpi4py import MPI
from src.A_star import Explorer
from src.maze import create_maze

def explorer_task(maze_type, width, height, visualize):
    maze = create_maze(width, height, maze_type)
    
    # Change the name of the variable to avoid conflict with class name
    explorer_instance = Explorer(maze, visualize=visualize)
    
    time_taken, moves = explorer_instance.solve()

    # Optional: track backtracks if implemented
    backtracks = getattr(explorer_instance, 'backtrack_count', None)

    return (time_taken, len(moves), backtracks)

def compare_results(results):
    print(f"{'Explorer':<10} {'Time (s)':<10} {'Moves':<10} {'Backtracks':<12}")
    best = min(results, key=lambda x: x[0])

    for idx, (time_taken, move_count, backtracks) in enumerate(results, 1):
        backtrack_str = str(backtracks) if backtracks is not None else "N/A"
        print(f"{idx:<10} {time_taken:<10.2f} {move_count:<10} {backtrack_str:<12}")
    
    print("\nBest Time:", f"{best[0]:.2f} seconds with {best[1]} moves")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--explorers", type=int, default=4, help="Number of explorers to run")
    parser.add_argument("--visualize", action="store_true", help="Visualize explorer movement")
    args = parser.parse_args()

    # MPI setup
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    maze_type = "static"
    width, height = 30, 30  # Ignored for static but required by interface
    num_explorers = args.explorers

    # Distribute tasks
    explorers_per_process = num_explorers // size
    remaining = num_explorers % size
    local_tasks = [(maze_type, width, height, args.visualize)] * explorers_per_process
    if rank < remaining:
        local_tasks.append((maze_type, width, height, args.visualize))

    # Run tasks
    local_results = [explorer_task(*task) for task in local_tasks]

    # Gather and compare
    all_results = comm.gather(local_results, root=0)

    if rank == 0:
        flat_results = [res for sublist in all_results for res in sublist]
        compare_results(flat_results)

if __name__ == "__main__":
    main()
