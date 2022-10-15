import pickle

from gridworld import Gridworld

maps = {}
with open('gridworld_maps.pickle', 'rb') as handle:
    maps = pickle.load(handle)

map_size = len(maps[0])

for k in maps:
    m = maps[k]
    g = Gridworld(map_size=map_size - 2, pregenerated_map=m)
    