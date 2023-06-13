# A* Maze Runner
## CS 520 - Introduction to Artificial Intelligence

A console-based gridworld generator and solver. A* and adaptive A* are separately used and evaluated as algorithms to solve a given gridworld.

## Implementation Details

Implementation was completed in Python, using Python 3.9.12 on an Intel 2019 MacBook Pro running macOS Monterey.
	    
$gridworld.py$ contains the primary algorithms and helper functions associated with all A* search operations. It contains the Gridworld class which, among other bookkeeping variables, contains `true_map` and `discovered_map` 2D arrays to keep track of the state of the gridworld.

Note that the `print_map()` helper function can be called on any gridworld to visualize the map at any state. Undiscovered blocks are marked with a `#`; discovered blocks are marked with an `X`; the agent and target are marked with `A` and `T`, respectively, and `D` is displayed when the agent meets the target.

`gridworld_generator.py` runs a maze generation algorithm to generate a series of mazes and save them to a .pickle file.
Algorithm: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search

`main.py` contains the primary testing infrastructure that was used to generate the results in the report. `sample_run.txt` provides the output from one sample run of this program.

`sandbox.py` provides a one-at-a-time testing ground for mazes and may be used to test the effects of different variations on performance.

## Usage

Use `python3 main.py` to run simulations on 50 pre-generated gridworlds.

Use `python3 gridworld_generator.py` to generate new gridworlds; modify variables within this file to change the size and number of gridworlds to generate.
