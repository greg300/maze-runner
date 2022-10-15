from gridworld import Gridworld

#mapSize = 101
map_size = 5  # Size of the gridworld in # of blocks (always square).
map = Gridworld(map_size)  # Gridworld.

map.generate_map()
map.uncover()
map.print_map()

res = map.compute_path()
path = map.build_path(res)
print(map.follow_path(path))


