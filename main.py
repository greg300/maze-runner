from gridworld import Gridworld

#mapSize = 101
map_size = 5  # Size of the gridworld in # of blocks (always square).
map = Gridworld(map_size)  # Gridworld.

map.generate_map()
map.print_map()


