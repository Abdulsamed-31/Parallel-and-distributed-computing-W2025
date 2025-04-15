import time
import pygame
import heapq
from typing import Tuple, List, Optional, Deque
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        self.maze = maze
        self.x, self.y = maze.start_pos
        self.direction = (1, 0)  # Start facing right
        self.moves = []
        self.start_time = None
        self.end_time = None
        self.visualize = visualize
        self.move_history = deque(maxlen=3)  # Keep track of last 3 moves
        self.backtracking = False
        self.backtrack_path = []
        self.backtrack_count = 0  # Count number of backtrack operations
        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - Automated Solving")
            self.clock = pygame.time.Clock()

    def heuristic(self, pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
        """Calculate Manhattan distance heuristic."""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def a_star(self) -> List[Tuple[int, int]]:
        """A* search algorithm to find the shortest path."""
        start = (self.x, self.y)
        goal = self.maze.end_pos
        open_list = []
        closed_list = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        heapq.heappush(open_list, (f_score[start], start))
        
        while open_list:
            _, current = heapq.heappop(open_list)
            if current == goal:
                # Reconstruct the path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # Return reversed path to go from start to goal

            closed_list.add(current)

            # Explore neighbors
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < self.maze.width and 0 <= neighbor[1] < self.maze.height:
                    if self.maze.grid[neighbor[1]][neighbor[0]] == 1 or neighbor in closed_list:
                        continue
                    tentative_g_score = g_score.get(current, float('inf')) + 1  # Assume cost 1 for each move
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))
        
        return []  # Return empty if no path found

    def move_to(self, path: List[Tuple[int, int]]):
        """Move the explorer along the given path."""
        for (target_x, target_y) in path:
            self.x, self.y = target_x, target_y
            self.moves.append((self.x, self.y))
            if self.visualize:
                self.draw_state()

    def draw_state(self):
        """Draw the current state of the maze and explorer."""
        self.screen.fill(WHITE)
        
        # Draw maze
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                   (x * CELL_SIZE, y * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE))
        
        # Draw start and end points
        pygame.draw.rect(self.screen, (0, 255, 0),
                        (self.maze.start_pos[0] * CELL_SIZE,
                         self.maze.start_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (self.maze.end_pos[0] * CELL_SIZE,
                         self.maze.end_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        # Draw explorer
        pygame.draw.rect(self.screen, BLUE,
                        (self.x * CELL_SIZE, self.y * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        pygame.display.flip()
        self.clock.tick(30)  # Control visualization speed

    def print_statistics(self, time_taken: float):
        print("\nMaze Exploration Statistics:")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("\n")

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        """
        Solve the maze using A* search.
        Returns the time taken and the list of moves made.
        """
        self.start_time = time.time()

        # Use A* to find the shortest path
        path = self.a_star()

        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        
        if path:
            self.move_to(path)
        
        if self.visualize:
            # Show final state for a few seconds
            pygame.time.wait(2000)
            pygame.quit()

        # Print detailed statistics
        self.print_statistics(time_taken)
        
        return time_taken, self.moves
