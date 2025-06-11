# 15-Puzzle-Game Solver

## Executive Summary
This is a 2-D 4-by-4 puzzle solver.

### A* search algorithm with the Manhattan distance heuristic
The A* is a pathfinding and graph traversal algorithm. 
It finds the shortest path from a start node to a goal node using a combination of:
- Actual cost from the start node to the current node (g(n))
- Estimated cost from the current node to the goal (h(n))
The total cost function is:
f(n)=g(n)+h(n)
The Manhattan distance is used as the heuristic function h(n). 
It calculates the total number of moves each tile is away from its goal position (goal_row, goal_column).
- **Assumption:** Only vertical and horizontal moves are allowed.

For any tile with value v at position **(i, j)**:
Manhattan distance is:
**h(n) = |i−goal_row| + |j−goal_column|**
- The total heuristic is the sum of these distances for all tiles (excluding the blank).
### How A* Solves the 15-Puzzle
1.	Start with the initial puzzle configuration.
2.	Generate neighbors by moving the blank tile (0) up, down, left, or right.
3.	For each neighbor:
 - Compute g(n) = number of moves so far.
 - Compute h(n) = Manhattan distance.
 - Compute f(n) = g(n) + h(n).
4.	Choose the neighbor with the lowest f(n) and repeat.
5.	Stop when the goal state is reached.

### CAUTION !
A* Search on 15-Puzzle Can Be Computationally Expensive
1.	The 15-puzzle has over 10 trillion possible states.
2.	A* with Manhattan distance is a good heuristic, but for complex or deeply scrambled puzzles, the search space becomes huge.
My current implementation has the following limitations:
- It does not use a priority queue with state deduplication efficiently.
- It does not limit search depth or time, so it can run indefinitely on hard puzzles.
