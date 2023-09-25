import random

class Node:
    def __init__(self, state):
        self.state = state

class Problem:
    def __init__(self):
        self.initial_state = self.generate_initial_state()

    def generate_initial_state(self):
        state = []
        for i in range(8):
            state.append(random.randint(0, 7))
        return state

    def calculate_attacking_pairs(self, state):
        attacking_pairs = 0
        for i in range(7):
            for j in range(i + 1, 8):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                    attacking_pairs += 1
        return attacking_pairs

    def get_neighbors(self, state):
        neighbors = []
        for col in range(8):
            for row in range(8):
                if state[col] != row:
                    # Create a new state by changing the row position of one queen in each column
                    neighbor = list(state)
                    neighbor[col] = row
                    neighbors.append(Node(neighbor))
        return neighbors

def hill_climbing_sideways(problem):
    current_node = Node(problem.initial_state)
    states_explored = [current_node]
    sideways_moves = 0

    while True:
        neighbors = problem.get_neighbors(current_node.state)  # Get all neighboring states
        best_neighbor = current_node
        min_attacking_pairs = problem.calculate_attacking_pairs(current_node.state)

        for neighbor in neighbors:
            attacking_pairs = problem.calculate_attacking_pairs(neighbor.state)  # Calculate attacking pairs for each neighbor
            if attacking_pairs < min_attacking_pairs:
                min_attacking_pairs = attacking_pairs
                best_neighbor = neighbor
        # print("Best neighbors: ", best_neighbor.state)

        if min_attacking_pairs == 0:
            return best_neighbor, states_explored

        if best_neighbor == current_node:
            sideways_moves += 1
            if sideways_moves > 100:
                return current_node, states_explored

        current_node = best_neighbor
        states_explored.append(current_node)

problem = Problem()
solution, states_explored = hill_climbing_sideways(problem)

# for state in states_explored:
#     print(state.state)
    
# Find the state with the minimum attacking pairs
optimal_state = min(states_explored, key=lambda x: problem.calculate_attacking_pairs(x.state))

print("Attacking Queens Before: ", problem.calculate_attacking_pairs(problem.initial_state))

print("Optimal State: ")
print(optimal_state.state)
print("Attacking Queens After: ", problem.calculate_attacking_pairs(optimal_state.state))
