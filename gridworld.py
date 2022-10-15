from cmath import inf
from random import randint
from typing import List
import numpy as np
from heapq import heapify, heappop, heappush

"""
Class representing one gridworld of a given size.
"""
class Gridworld:
    def __init__(self, map_size=101) -> None:
        self.map_size = map_size + 2  # Size of the square gridworld in # of blocks (must be odd, add 2 for borders).
        self.true_map = [[0] * (self.map_size) for _ in range((self.map_size))]  # 2D array representing the gridworld. 0 = unblocked, 1 = blocked.
        self.discovered_map = [[0] * (self.map_size) for _ in range((self.map_size))]  # Gridworld with all information discovered by agent only.
        self.g_vals = [[0] * (self.map_size) for _ in range((self.map_size))]  # g values for all cells.
        self.agent = (1, 1)  # Location of the agent on the map.
        self.target = (self.map_size - 2, self.map_size - 2)  # Location of the target on the map.

    """
    Resets the agent and the target to their default positions.
    """
    def reset_map(self) -> None:
        self.agent = (1, 1)
        self.target = (self.map_size - 2, self.map_size - 2)
        self.g_vals = [[0] * (self.map_size) for _ in range((self.map_size))]

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

    """
    h(n), a heuristic function for A*.
    Manhattan distance is used as the heuristic.
    Given two points a, b, returns the Manhattan distance between them.
    """
    def h(self, s) -> int:
        a = s
        b = self.target
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    """
    g(n), the path cost from start node to node n for A*.
    """
    def g(self, s) -> int:
        return self.g_vals[s[0]][s[1]]

    """
    f(n), the evaluation function for A*.
    f(n) = g(n) + h(n).
    """
    def f(self, s) -> int:
        return self.g(s) + self.h(s)
    
    """
    Normal A* to find the shortest path, based on agent's knowledge of the gridworld.
    """
    def compute_path(self) -> List:
        s_start = self.agent  # Starting state is location of agent.
        s_goal = self.target  # Goal state is location of target.

        # Zero out all g values.
        self.g_vals = [[0] * (self.map_size) for _ in range((self.map_size))]

        # Set g(s_goal) = infinity.
        self.g_vals[s_goal[0]][s_goal[1]] = inf
        # Set g(s_start) = 0.
        self.g_vals[s_start[0]][s_start[1]] = 0 

        # Tie breaking: largest g-value of any generated cell.
        # Favors cells with larger g-values.
        # Second tie breaking: random.
        g_max = self.map_size ** 2

        # Create an open list, represented as a binary heap.
        open_list = []
        # Insert s_start into open list.
        priority = g_max * self.f(s_start) - self.g(s_start)
        heappush(open_list, (priority, 0, s_start))  # (f, rand_tie_break, s)

        # Create a closed list.
        closed_list = set()

        # Create a tree-pointer for identifying shortest path after A*.
        # First item in tuple points to second item.
        tree = []
        while len(open_list) > 0:
            # Identify a state s with the smallest f-value in the open list.
            s = heappop(open_list)[2]

            # If s is the goal state, A* is finished.
            if s == s_goal:
                return tree
            # Add s to the closed list.
            closed_list.add(s)

            # Try all possible actions from s to get successor states.
            succ_states = self.create_action_states(s)
            for succ in succ_states:
                self.g_vals[succ[0]][succ[1]] = inf

                # Skip states already in closed list.
                if succ in closed_list:
                    continue
                if self.g(succ) > self.g(s):
                    # Sets g value of successor state to g value of s plus action cost (1).
                    self.g_vals[succ[0]][succ[1]] = self.g_vals[s[0]][s[1]] + 1
                    # Set tree-pointer of successor state to point to state s.
                    tree.append((succ, s))
                
                    i = self.is_in_open_list(s, open_list)

                    # Insert successor state into open list (if it is not already there).
                    if i is None:
                        priority = g_max * self.f(succ) - self.g(succ)
                        rand_tie_breaker = randint(0, 1000)
                        heappush(open_list, (priority, rand_tie_breaker, succ))
                    else:
                        # Remove state from open list and add it back with new f value.
                        # (Really, we just change its priority and re-heapify.)
                        priority = g_max * self.f(succ) - self.g(succ)
                        rand_tie_breaker = randint(0, 1000)
                        open_list[i] = (priority, rand_tie_breaker, succ)
                        heapify(open_list)

        return None
    
    """
    Returns whether a state s is in the open list.
    If yes, returns the index of s.
    If no, returns None.
    """
    def is_in_open_list(self, s, open_list) -> int:
        for i in range(len(open_list)):
            if open_list[i][1] == s:
                return i

        return None

    """
    Generate a list of new states to explore from current state s,
    given the four available actions: N, S, E, W.
    Takes into account blocks / borders.
    """
    def create_action_states(self, s) -> List:
        new_states = []
        # Try north.
        if self.discovered_map[s[0]][s[1] + 1] == 0:
            new_states.append((s[0], s[1] + 1))
            #self.g_vals[s[0]][s[1] + 1] = self.g_vals[s[0]][s[1]] + 1
        # Try south.
        if self.discovered_map[s[0]][s[1] - 1] == 0:
            new_states.append((s[0], s[1] - 1))
            #self.g_vals[s[0]][s[1] - 1] = self.g_vals[s[0]][s[1]] + 1
        # Try east.
        if self.discovered_map[s[0] + 1][s[1]] == 0:
            new_states.append((s[0] + 1, s[1]))
            #self.g_vals[s[0] + 1][s[1]] = self.g_vals[s[0]][s[1]] + 1
        # Try west.
        if self.discovered_map[s[0] - 1][s[1]] == 0:
            new_states.append((s[0] - 1, s[1]))
            #self.g_vals[s[0] - 1][s[1]] = self.g_vals[s[0]][s[1]] + 1

        return new_states

    """
    Reveals the true contents of any cells to the
    north, south, east, and west of the agent's current location.
    """
    def uncover(self) -> None:
        # North.
        self.discovered_map[self.agent[0]][self.agent[1] + 1] = self.true_map[self.agent[0]][self.agent[1] + 1]
        # South.
        self.discovered_map[self.agent[0]][self.agent[1] - 1] = self.true_map[self.agent[0]][self.agent[1] - 1]
        # East.
        self.discovered_map[self.agent[0] + 1][self.agent[1]] = self.true_map[self.agent[0] + 1][self.agent[1]]
        # West.
        self.discovered_map[self.agent[0] - 1][self.agent[1]] = self.true_map[self.agent[0] - 1][self.agent[1]]

    """
    Attempts to move the agent's location from its current cell
    to the cell indicated by the given next state.
    Returns False if unsuccessful, True otherwise.
    """
    def advance(self, next) -> bool:
        if self.true_map[next[0]][next[1]] == 0:
            self.agent = next
            self.uncover()
            return True
        else:
            return False
    
    """
    Given a tree from A*, creates a full path
    from agent's location to the end of the path.
    """
    def build_path(self, tree) -> List:
        path = []
        goal = self.target  # Start of reverse path is the target.
        path.append(goal)
        for t in tree[: : -1]:
            # First item in tuple (successor state) points to second item (previous state).
            succ = t[0]
            prev = t[1]

            # Check if this is a path into the current goal.
            if succ == goal:
                # Add previous state to path, if prev is not the agent.
                if prev != self.agent:
                    path.append(prev)
                # Update goal with previous state.
                goal = prev
                #print("Added to path:", prev)
        print(path)
        return reversed(path)

    """
    Given a created path, attempts to advance along this path
    until the target is reached or a block is encountered.
    Uncovers knowledge of blocked cells along the way.
    Returns False if unsuccessful, True otherwise. 
    """
    def follow_path(self, path) -> bool:
        for next in path:
            if not self.advance(next):
                self.print_map()
                return False
        
        self.print_map()
        return True

    """
    Prints the given map.
    """
    def print_map(self) -> None:
        for i in range(self.map_size):
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
