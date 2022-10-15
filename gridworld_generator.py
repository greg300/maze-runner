import pickle
from typing import Dict

from gridworld import Gridworld

def generate_true_maps(num_maps, map_size, complexity=0.75, density=0.75) -> Dict:
    maps = {}
    for i in range(num_maps):
        g = Gridworld(map_size, complexity=complexity, density=density)
        maps[i] = g.true_map

    return maps

num_maps = 50
map_size = 101

maps = generate_true_maps(num_maps, map_size) 

# Save all the data.
with open("gridworld_maps.pickle", "wb") as handle:
    pickle._dump(maps, handle, protocol=pickle.HIGHEST_PROTOCOL)




