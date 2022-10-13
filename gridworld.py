"""
Class representing one gridworld of a given size (could be true or discovered).
"""
class Gridworld:
    def __init__(self, map_size) -> None:
        self.map_size = map_size  # Size of the gridworld in # of blocks (always square).
        self.true_map = [[0] * (map_size + 1) for _ in range((map_size + 1))]  # 2D array representing the gridworld. 0 = unblocked, 1 = blocked.
        self.discovered_map = [[0] * (map_size + 1) for _ in range((map_size + 1))]  # Gridworld with all information discovered by agent only.
        self.agent = (1, 1)  # Location of the agent on the map.
        self.target = (map_size, map_size)  # Location of the target on the map.

    """
    Generate a map with blocked obstacles (1) and unblocked free space (0).
    Borders are denoted as obstacles.
    """
    def generate_map(self):
        pass

    def compute_path(self):
        pass

    """
    Print the given map.
    """
    def print_map(self):
        # Top border.
        # print("-", end=" ")
        # for _ in range(self.map_size):
        #     print("-", end=" ")
        # print("-", end="\n")

        # Side borders and map.
        for i in range(self.map_size):
            print("|", end=" ")
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
            print("|", end="\n")
        
        # Bottom border.
        # print("-", end=" ")
        # for _ in range(self.map_size):
        #     print("-", end=" ")
        # print("-", end="\n")