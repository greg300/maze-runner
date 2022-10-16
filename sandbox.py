"""
This file is for testing purposes.
"""
import pickle

from gridworld import Gridworld

# map_size = 21  # Size of the gridworld in # of blocks (always square).
# map = Gridworld(map_size)  # Gridworld.

# map.print_map()
# map.repeated_compute_path(reverse=False, large_g_ties=True)


maps = {}
with open('gridworld_maps.pickle', 'rb') as handle:
    maps = pickle.load(handle)

map_size = len(maps[0])
print("Loaded " + str(len(maps)) + " gridworlds of size " + str(map_size - 2))

map_0 = maps[0]
# Block the agent, resulting in no path.
# map_0[2][1] = 1
# map_0[1][2] = 1
g_0 = Gridworld(map_size=map_size - 2, pregenerated_map=map_0)
#g_0.print_map()


# # Forward A*, ties favor large g values.
# print("Testing forward A*, ties favoring large g values...")
# res = g_0.repeated_compute_path(reverse=False, large_g_ties=True)
# if res:
#     print("Path found for map " + str(0) + " with " + str(g_0.expanded_cells) + " expanded cells.")
#     print("\tMoves taken: " + str(g_0.moves_taken))
# else:
#     print("No path found for map " + str(0) + ".")

# # Forward A*, ties favor small g values.
# print("Testing forward A*, ties favoring small g values...")
# res = g_0.repeated_compute_path(reverse=False, large_g_ties=False)
# if res:
#     print("Path found for map " + str(0) + " with " + str(g_0.expanded_cells) + " expanded cells.")
#     print("\tMoves taken: " + str(g_0.moves_taken))
# else:
#     print("No path found for map " + str(0) + ".")

# Backward A*, ties favor large g values.
print("Testing backward A*, ties favoring large g values...")
res = g_0.repeated_compute_path(reverse=True, large_g_ties=True)
if res:
    print("Path found for map " + str(0) + " with " + str(g_0.expanded_cells) + " expanded cells.")
    print("\tMoves taken: " + str(g_0.moves_taken))
else:
    print("No path found for map " + str(0) + ".")