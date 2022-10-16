import pickle

from gridworld import Gridworld

maps = {}
with open('gridworld_maps.pickle', 'rb') as handle:
    maps = pickle.load(handle)

map_size = len(maps[0])
print("Loaded " + str(len(maps)) + " gridworlds of size " + str(map_size - 2))

successes = [0] * 4
total_expanded_cells = [0] * 4
total_moves_taken = [0] * 4

for k in maps:
    m = maps[k]
    g = Gridworld(map_size=map_size - 2, pregenerated_map=m)

    # Forward A*, ties favor large g values.
    print("Testing forward A*, ties favoring large g values...")
    res = g.repeated_compute_path(reverse=False, large_g_ties=True)
    if res:
        successes[0] += 1
        total_expanded_cells[0] += g.expanded_cells
        total_moves_taken[0] += g.moves_taken
        print("Path found for map " + str(k) + " with "
                                    + str(g.expanded_cells) + " expanded cells and "
                                    + str(g.moves_taken) + " moves made.")
    else:
        print("No path found for map " + str(k) + ".")

    # Forward A*, ties favor small g values.
    print("Testing forward A*, ties favoring small g values...")
    res = g.repeated_compute_path(reverse=False, large_g_ties=False)
    if res:
        successes[1] += 1
        total_expanded_cells[1] += g.expanded_cells
        total_moves_taken[1] += g.moves_taken
        print("Path found for map " + str(k) + " with "
                                    + str(g.expanded_cells) + " expanded cells and "
                                    + str(g.moves_taken) + " moves made.")
    else:
        print("No path found for map " + str(k) + ".")

    # Backward A*, ties favor large g values.
    print("Testing backward A*, ties favoring large g values...")
    res = g.repeated_compute_path(reverse=True, large_g_ties=True)
    if res:
        successes[2] += 1
        total_expanded_cells[2] += g.expanded_cells
        total_moves_taken[2] += g.moves_taken
        print("Path found for map " + str(k) + " with "
                                    + str(g.expanded_cells) + " expanded cells and "
                                    + str(g.moves_taken) + " moves made.")
    else:
        print("No path found for map " + str(k) + ".")

    # Backward A*, ties favor small g values.
    print("Testing backward A*, ties favoring small g values...")
    res = g.repeated_compute_path(reverse=True, large_g_ties=False)
    if res:
        successes[3] += 1
        total_expanded_cells[3] += g.expanded_cells
        total_moves_taken[3] += g.moves_taken
        print("Path found for map " + str(k) + " with "
                                    + str(g.expanded_cells) + " expanded cells and "
                                    + str(g.moves_taken) + " moves made.")
    else:
        print("No path found for map " + str(k) + ".")

print("\nForward A*, ties favor large g values:")
print("\tSuccesses: " + str(successes[0]) + "/" + str(len(maps)))
print("\tAverage expanded cells: " + str(total_expanded_cells[0] / float(successes[0])))
print("\tAverage moves taken: " + str(total_moves_taken[0] / float(successes[0])))

print("\nForward A*, ties favor small g values:")
print("\tSuccesses: " + str(successes[1]) + "/" + str(len(maps)))
print("\tAverage expanded cells: " + str(total_expanded_cells[1] / float(successes[1])))
print("\tAverage moves taken: " + str(total_moves_taken[1] / float(successes[1])))

print("\nBackward A*, ties favor large g values:")
print("\tSuccesses: " + str(successes[2]) + "/" + str(len(maps)))
print("\tAverage expanded cells: " + str(total_expanded_cells[2] / float(successes[2])))
print("\tAverage moves taken: " + str(total_moves_taken[2] / float(successes[2])))

print("\nBackward A*, ties favor small g values:")
print("\tSuccesses: " + str(successes[3]) + "/" + str(len(maps)))
print("\tAverage expanded cells: " + str(total_expanded_cells[3] / float(successes[3])))
print("\tAverage moves taken: " + str(total_moves_taken[3] / float(successes[3])))

    