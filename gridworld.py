from cmath import inf
from random import randint
from typing import List
import numpy as np
from heapq import heapify, heappop, heappush

"""
Class representing one gridworld of a given size.
"""
class Gridworld:
    def __init__(self, map_size=101, pregenerated_map=None, complexity=0.75, density=0.75) -> None:
        self.map_size = map_size + 2  # Size of the square gridworld in # of blocks (must be odd, add 2 for borders).
        self.true_map = [[0] * (self.map_size) for _ in range((self.map_size))]  # 2D array representing the gridworld. 0 = unblocked, 1 = blocked.
        self.discovered_map = [[]]  # Gridworld with all information discovered by agent only.
        self.g_vals = [[]]  # g values for all cells.
        self.search_vals = [[]]  # search values for all cells.
        self.agent = (0, 0)  # Location of the agent on the map.
        self.target = (0, 0)  # Location of the target on the map.
        self.expanded_cells = 0  # Number of expanded cells (cells added to closed list).
        self.moves_taken = 0  # Number of moves made by the agent.

        if pregenerated_map is None:
            self.generate_map(complexity, density)  # Generate a new true map.
        else:
            self.true_map = pregenerated_map
            #print(self.true_map)
        self.reset_map()  # Reset the map to its default state.

    """
    Resets the agent and the target to their default positions.
    Clears all g & search values and wipes the discovered map.
    """
    def reset_map(self) -> None:
        self.agent = (1, 1)
        self.target = (self.map_size - 2, self.map_size - 2)
        self.discovered_map = [[0] * (self.map_size) for _ in range((self.map_size))]
        self.g_vals = [[0] * (self.map_size) for _ in range((self.map_size))]
        self.search_vals = [[0] * (self.map_size) for _ in range((self.map_size))]
        self.expanded_cells = 0 
        self.moves_taken = 0
        self.uncover()  # Uncover the neighboring states to agent's starting position.

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
        for _ in range(density):
            x, y = np.random.randint(0, shape[1] // 2 + 1) * 2, np.random.randint(0, shape[0] // 2 + 1) * 2
            maze[y, x] = 1
            for _ in range(complexity):
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
    def h(self, s, s_goal) -> int:
        a = s
        b = s_goal
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
    def f(self, s, s_goal) -> int:
        return self.g(s) + self.h(s, s_goal)
    
    """
    Normal A* to find the shortest path, based on agent's knowledge of the gridworld.
    Returns True if a path is found, False otherwise.
    """
    def compute_path(self, s_start, s_goal, open_list, closed_list, tree, counter, g_max, large_g_ties=True) -> bool:
        #while self.g(s_goal) > self.g(open_list[0][2]) + self.h(open_list[0][2], s_goal):
        #print(counter)
        while len(open_list) > 0:
            # if not self.g(s_goal) > self.g(open_list[0][2]) + self.h(open_list[0][2], s_goal):
            #     return False

            # Identify a state s with the smallest f-value in the open list.
            s = heappop(open_list)[2]

            # If s is the goal state, A* is finished.
            if s == s_goal:
                return True
            # Add s to the closed list.
            closed_list.add(s)
            self.expanded_cells += 1

            # Try all possible actions from s to get successor states.
            succ_states = self.create_action_states(s)
            for succ in succ_states:
                # Skip states already in closed list.
                if succ in closed_list:
                    continue
                
                if self.search_vals[succ[0]][succ[1]] < counter:
                    self.g_vals[succ[0]][succ[1]] = inf
                    self.search_vals[succ[0]][succ[1]] = counter

                if self.g(succ) > self.g(s):
                    # Sets g value of successor state to g value of s plus action cost (1).
                    self.g_vals[succ[0]][succ[1]] = self.g_vals[s[0]][s[1]] + 1
                    # Set tree-pointer of successor state to point to state s.
                    tree.append((succ, s))
                
                    i = self.is_in_open_list(s, open_list)

                    # Insert successor state into open list (if it is not already there).
                    if i is None:
                        priority = 0
                        tie_breaker = 0
                        if large_g_ties:
                            priority = g_max * self.f(succ, s_goal) - self.g(succ)
                            tie_breaker = randint(0, 100)
                        else:
                            priority = self.f(succ, s_goal) + self.g(succ)
                        heappush(open_list, (priority, tie_breaker, succ))
                    else:
                        # Remove state from open list and add it back with new f value.
                        # (Really, we just change its priority and re-heapify.)
                        priority = 0
                        tie_breaker = 0
                        if large_g_ties:
                            priority = g_max * self.f(succ, s_goal) - self.g(succ)
                            tie_breaker = randint(0, 100)
                        else:
                            priority = self.f(succ, s_goal) + self.g(succ)
                        open_list[i] = (priority, tie_breaker, succ)
                        heapify(open_list)

        return False
    
    """
    Repeated A* to find the shorest path from agent to target.
    Continuously calls A* (compute_path) until agent reaches target
    or when no path is found.
    Before searching, resets discovered map and all g & search values.
    Returns True if a path is found, False otherwise.
    """
    def repeated_compute_path(self, reverse=False, large_g_ties=True) -> bool:
        # Initialize search counter to 0.
        counter = 0
        # Initialize search(s) and g(s) to 0 for all states.
        self.reset_map()

        s_start = self.agent  # Starting state is location of agent.
        s_goal = self.target  # Goal state is location of target.

        # If testing Backward A*, swap start and goal.
        if reverse:
            s_start = self.target
            s_goal = self.agent

        while s_start != s_goal:
            # Increment search counter.
            counter += 1

            # Set g(s_start) = 0.
            self.g_vals[s_start[0]][s_start[1]] = 0 
            # Set search(s_start) = counter.
            self.search_vals[s_start[0]][s_start[1]] = counter

            # Set g(s_goal) = infinity.
            self.g_vals[s_goal[0]][s_goal[1]] = inf
            # Set search(s_goal) = counter.
            self.search_vals[s_goal[0]][s_goal[1]] = counter

            # Create an open list, represented as a binary heap.
            open_list = []

            # Create a closed list, represented as a set.
            closed_list = set()

            # Create a tree-pointer for identifying shortest path after A*.
            # First item in tuple points to second item.
            tree = []
        
            # Tie breaking:
            g_max = self.map_size ** 2
            priority = 0
            if large_g_ties:
                # Largest g-value of any generated cell.
                # Favors cells with larger g-values.
                priority = g_max * self.f(s_start, s_goal) - self.g(s_start)
            else:
                # Smallest g-value of any generated cell.
                # Favors cells with smaller g-values.
                priority = self.f(s_start, s_goal) + self.g(s_start)

            # Second tie breaking: random.

            # Insert s_start into open list.
            heappush(open_list, (priority, 0, s_start))  # (f, tie_breaker, s)

            # Normal A*.
            path_found = self.compute_path(s_start, s_goal, open_list, closed_list, tree, counter, g_max, large_g_ties)
            #print(len(open_list))
            #print(len(closed_list))
        
            #print(tree)
            # If open list is empty, no path exists to the target.
            if len(open_list) == 0 and not path_found:
                #print("Target cannot be reached; no path found.")
                return False
            
            # Follow tree-pointers from s_goal to s_start and move agent on this path
            # from s_start to s_goal until s_goal is reached or path is blocked.
            path = self.build_path(tree, s_start, s_goal, reverse)
            # If path was followed successfully, target is reached.
            if self.follow_path(path):
                #print("Target reached!")
                #print("Expanded " + str(self.expanded_cells) + " cells.")
                return True
            #print(self.agent)
            # Otherwise, set s_start to agent's state.
            if reverse:
                s_goal = self.agent
            else:
                s_start = self.agent

    """
    Returns whether a state s is in the open list.
    If yes, returns the index of s.
    If no, returns None.
    """
    def is_in_open_list(self, s, open_list) -> int:
        for i in range(len(open_list)):
            if open_list[i][2] == s:
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
        if s[1] > 0:  # Ensure not touching top border.
            if self.discovered_map[s[0]][s[1] - 1] == 0:
                new_states.append((s[0], s[1] - 1))
        # Try south.
        if s[1] < self.map_size - 1:  # Ensure not touching bottom border.
            if self.discovered_map[s[0]][s[1] + 1] == 0:
                new_states.append((s[0], s[1] + 1))
        # Try east.
        if s[0] < self.map_size - 1:  # Ensure not touching right border.
            if self.discovered_map[s[0] + 1][s[1]] == 0:
                new_states.append((s[0] + 1, s[1]))
        # Try west.
        if s[0] > 0:  # Ensure not touching left border.
            if self.discovered_map[s[0] - 1][s[1]] == 0:
                new_states.append((s[0] - 1, s[1]))

        return new_states

    """
    Reveals the true contents of any cells to the
    north, south, east, and west of the agent's current location.
    """
    def uncover(self) -> None:
        # North.
        self.discovered_map[self.agent[0]][self.agent[1] - 1] = self.true_map[self.agent[0]][self.agent[1] - 1]
        # South.
        self.discovered_map[self.agent[0]][self.agent[1] + 1] = self.true_map[self.agent[0]][self.agent[1] + 1]
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
            self.moves_taken += 1
            self.uncover()
            return True
        else:
            return False
    
    """
    Given a tree from A*, creates a full path
    from agent's location to the end of the path.
    """
    def build_path(self, tree, s_start, s_goal, reverse=False) -> List:
        path = []
        goal = s_goal  # Start of path is the target.
        path.append(goal)
        # if not reverse:
        #     tree = tree[: : -1]
        for t in tree[: : -1]:
            # First item in tuple (successor state) points to second item (previous state).
            succ = t[0]
            prev = t[1]

            # Check if this is a path into the current goal.
            if succ == goal:
                # Add previous state to path. 
                #if prev != s_start:  # if prev is not the start.
                path.append(prev)
                # Update goal with previous state.
                goal = prev

        #print(path)
        if reverse:
            return path
        else:
            return path[: : -1]

    """
    Given a created path, attempts to advance along this path
    until the target is reached or a block is encountered.
    Uncovers knowledge of blocked cells along the way.
    Returns False if unsuccessful, True otherwise. 
    """
    def follow_path(self, path) -> bool:
        for next in path[1 :]:
            if not self.advance(next):
                #self.print_map()
                return False
        
        #self.print_map()
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
