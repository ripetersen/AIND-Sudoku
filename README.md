# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The code loops over all "two-valued boxes", loops over the units that contain those boxes, loops over the peers in those units.  
   If a peer is found with the same value as the box then the two values are removed from the other peers in that unit.  The
   `reduce_puzzle` method is updated to call the `naked_twin` method thereby enforcing that constraint.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Additional units are added.   These units contain the boxes along the two diagonals. `unitlist` includes the two addtional units
   and the maps `units` and `peers` are built the same way as before and therefore include the boxes from the two new units.  
   The constraint methods: `eleminate`, `only_choice` and `naked_twin` apply the constraints to any unit we construct and 
   therefore work to apply the constraints to the additional units without change.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
