from gridworld import Gridworld

#mapSize = 101
map_size = 21  # Size of the gridworld in # of blocks (always square).
map = Gridworld(map_size)  # Gridworld.

#map.generate_map()
#map.uncover()
map.print_map()

map.repeated_compute_path()
#res = map.compute_path()
#path = map.build_path(res)
#print(map.follow_path(path))


