import numpy as np

"""
Class representing one gridworld of a given size.
"""
class Gridworld:
    def __init__(self, map_size=101) -> None:
        self.map_size = map_size + 2  # Size of the square gridworld in # of blocks (must be odd, add 2 for borders).
        self.true_map = [[0] * (self.map_size) for _ in range((self.map_size))]  # 2D array representing the gridworld. 0 = unblocked, 1 = blocked.
        self.discovered_map = [[0] * (self.map_size) for _ in range((self.map_size))]  # Gridworld with all information discovered by agent only.
        self.agent = (1, 1)  # Location of the agent on the map.
        self.target = (self.map_size - 2, self.map_size - 2)  # Location of the target on the map.

    """
    Generate a map with blocked obstacles (1) and unblocked free space (0).
    Borders are denoted as obstacles.
    """
    def generate_map(self, complexity=0.75, density=0.75) -> None:
        # Define the empty maze with extra space for borders.
        # Assume that the dimensions are odd; correct otherwise.
        shape = ((self.map_size // 2) * 2 + 1, (self.map_size // 2) * 2 + 1)

        # Adjust complexity and density to correspond to maze size.
        complexity = int(complexity * (5 * (shape[0] + shape[1])))
        density = int(density * ((shape[0] // 2) * (shape[1] // 2)))

        # Create the maze.
        maze = np.zeros(shape, dtype=bool)

        # Create borders, representing as blocked obstacles.
        maze[0, :] = maze[-1, :] = 1
        maze[:, 0] = maze[:, -1] = 1

        # Create aisles.
        for i in range(density):
            x, y = np.random.randint(0, shape[1] // 2 + 1) * 2, np.random.randint(0, shape[0] // 2 + 1) * 2
            maze[y, x] = 1
            for j in range(complexity):
                neighbors = []
                if x > 1:
                    neighbors.append((y, x - 2))
                if x < shape[1] - 2:
                    neighbors.append((y, x + 2))
                if y > 1:
                    neighbors.append((y - 2, x))
                if y < shape[0] - 2:
                    neighbors.append((y + 2, x))
                if len(neighbors):
                    y_, x_ = neighbors[np.random.randint(0, len(neighbors))]
                    if maze[y_, x_] == 0:
                        maze[y_, x_] = 1
                        maze[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                        x, y = x_, y_

        complete_maze = maze.astype(int)
        self.true_map = complete_maze

    def compute_path(self) -> None:
        pass

    """
    Print the given map.
    """
    def print_map(self) -> None:
        # Top border.
        # print("-", end=" ")
        # for _ in range(self.map_size):
        #     print("-", end=" ")
        # print("-", end="\n")

        # Side borders and map.
        for i in range(self.map_size):
            #print("|", end=" ")
            for j in range(self.map_size):
                # Agent has reached target.
                if self.target == (i, j) and self.agent == (i, j):
                    print("D", end=" ")
                # Target.
                elif self.target == (i, j):
                    print("T", end=" ")
                # Agent.
                elif self.agent == (i, j):
                    print("A", end=" ")
                # Cell is truly unblocked.
                elif self.true_map[i][j] == 0 and self.discovered_map[i][j] == 0:
                    print(" ", end=" ")
                # Cell is truly blocked and has not been discovered as such.
                elif self.true_map[i][j] == 1 and self.discovered_map[i][j] == 0:
                    print("#", end=" ")
                # Cell is truly blocked and has been discovered as such.
                elif self.true_map[i][j] == 1 and self.discovered_map[i][j] == 1:
                    print("X", end=" ")
            print("", end="\n")
            #print("|", end="\n")
        
        # Bottom border.
        # print("-", end=" ")
        # for _ in range(self.map_size):
        #     print("-", end=" ")
        # print("-", end="\n")