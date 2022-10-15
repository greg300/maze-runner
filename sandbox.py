"""
This file is for testing purposes.
"""
from gridworld import Gridworld

# map_size = 21  # Size of the gridworld in # of blocks (always square).
# map = Gridworld(map_size)  # Gridworld.

map_size = 21
map = Gridworld(map_size)

map.print_map()
map.repeated_compute_path(reverse=False, large_g_ties=True)