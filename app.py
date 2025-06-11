from flask import Flask, request, render_template_string
import heapq
app = Flask(__name__)
# Goal state for the 15 puzzle
goal_state = [1, 2, 3, 4,
              5, 6, 7, 8,
              9, 10, 11, 12,
              13, 14, 15, 0]
# Directions and their inverses
moves = {'UP': -4, 'DOWN': 4, 'LEFT': -1, 'RIGHT': 1}
inverse_move = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
# Manhattan distance heuristic
def manhattan(state):
    distance = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        goal_pos = goal_state.index(val)
        distance += abs(i // 4 - goal_pos // 4) + abs(i % 4 - goal_pos % 4)
    return distance
# Generate neighbors
def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 4)
    for move, delta in moves.items():
        new_index = zero_index + delta
        if move == 'UP' and row == 0: continue
        if move == 'DOWN' and row == 3: continue
        if move == 'LEFT' and col == 0: continue
        if move == 'RIGHT' and col == 3: continue
        new_state = state[:]
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append((new_state, move))
    return neighbors
# A* algorithm
def solve_puzzle(start_state):
    frontier = [(manhattan(start_state), 0, start_state, [])]
    visited = set()
    while frontier:
        _, cost, state, path = heapq.heappop(frontier)
        if state == goal_state:
            return path
        visited.add(tuple(state))
        for neighbor, move in get_neighbors(state):
            if tuple(neighbor) not in visited:
                heapq.heappush(frontier, (cost + 1 + manhattan(neighbor), cost + 1, neighbor, path + [move]))
    return []
# HTML template

html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>15 Puzzle Solver</title>
</head>
<body>
    <h1>15 Puzzle Solver</h1>
    <form method="post">
        <label for="puzzle">Enter 16 numbers (0-15) separated by commas:</label><br>
        <input type="text" id="puzzle" name="puzzle" size="50" required><br><br>
        <input type="submit" value="Solve">
    </form>

    {% if moves %}
        <h2>Moves for blank:</h2>
        <p>{{ moves }}</p>

        <h2>Moves for Neighbors to Blank:</h2>
        <p>{{ inverse }}</p>
    {% endif %}
</body>
</html>
'''

# Controller
@app.route('/', methods=['GET', 'POST'])
def index():
    moves_result = []
    inverse_result = []
    if request.method == 'POST':
        puzzle_input = request.form['puzzle']
        try:
            puzzle = list(map(int, puzzle_input.strip().split(',')))
            if len(puzzle) == 16 and set(puzzle) == set(range(16)):
                moves_result = solve_puzzle(puzzle)
                inverse_result = [inverse_move[m] for m in moves_result]
            else:
                moves_result = ['Invalid input. Please enter all numbers from 0 to 15.']
        except:
            moves_result = ['Invalid input format.']
    return render_template_string(html_template, moves=moves_result, inverse=inverse_result)
# Run with: flask run
