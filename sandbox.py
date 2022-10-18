"""
This file is for testing purposes.
"""
import pickle

from gridworld import Gridworld

maps = {}
with open('gridworld_maps_smaller.pickle', 'rb') as handle:
    maps = pickle.load(handle)

map_size = len(maps[0])
#print("Loaded " + str(len(maps)) + " gridworlds of size " + str(map_size - 2))

map_0 = maps[0]

# Block the agent, resulting in no path.
# map_0[2][1] = 1
# map_0[1][2] = 1

g_0 = Gridworld(map_size=map_size - 2, pregenerated_map=map_0)
g_0.print_map()


# Forward A*, ties favor large g values.
print("\nTesting forward A*, ties favoring large g values...")
res = g_0.repeated_compute_path(reverse=False, large_g_ties=True)
g_0.print_map()
if res:
    print("Path found for map " + str(0) + " with " + str(g_0.expanded_cells) + " expanded cells.")
    print("\tMoves taken: " + str(g_0.moves_taken))
    print("\tMax expanded cells: " + str(g_0.max_expanded))
else:
    print("No path found for map " + str(0) + ".")

# Forward A*, ties favor small g values.
print("\nTesting forward A*, ties favoring small g values...")
res = g_0.repeated_compute_path(reverse=False, large_g_ties=False)
g_0.print_map()
if res:
    print("Path found for map " + str(0) + " with " + str(g_0.expanded_cells) + " expanded cells.")
    print("\tMoves taken: " + str(g_0.moves_taken))
    print("\tMax expanded cells: " + str(g_0.max_expanded))
else:
    print("No path found for map " + str(0) + ".")

# Backward A*, ties favor large g values.
print("\nTesting backward A*, ties favoring large g values...")
res = g_0.repeated_compute_path(reverse=True, large_g_ties=True)
g_0.print_map()
if res:
    print("Path found for map " + str(0) + " with " + str(g_0.expanded_cells) + " expanded cells.")
    print("\tMoves taken: " + str(g_0.moves_taken))
    print("\tMax expanded cells: " + str(g_0.max_expanded))
else:
    print("No path found for map " + str(0) + ".")

# Backward A*, ties favor small g values.
print("\nTesting backward A*, ties favoring small g values...")
res = g_0.repeated_compute_path(reverse=True, large_g_ties=False)
g_0.print_map()
if res:
    print("Path found for map " + str(0) + " with " + str(g_0.expanded_cells) + " expanded cells.")
    print("\tMoves taken: " + str(g_0.moves_taken))
    print("\tMax expanded cells: " + str(g_0.max_expanded))
else:
    print("No path found for map " + str(0) + ".")

# Adaptive A*, ties favor large g values.
print("\nTesting adaptive A*, ties favoring large g values...")
res = g_0.adaptive_repeated_compute_path()
g_0.print_map()
if res:
    print("Path found for map " + str(0) + " with " + str(g_0.expanded_cells) + " expanded cells.")
    print("\tMoves taken: " + str(g_0.moves_taken))
    print("\tMax expanded cells: " + str(g_0.max_expanded))
else:
    print("No path found for map " + str(0) + ".")