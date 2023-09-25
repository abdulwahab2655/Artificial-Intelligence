from queue import PriorityQueue
import math

#TASK-1

with open('problems.txt', 'r') as file:
    lines = file.readlines()
    
num_problems = int(lines[0].strip())

arrlist = []
for line in lines[1:]:
    problem = line.strip().split()
    problem = [int(num) for num in problem] # Convert the strings to integers
    arrlist.append(problem) 

def convert2D(arr, r, c):  
    matrix = []
    count = 0
    for i in range(r):
        col = []
        for j in range(c):
            col.append(arr[count])
            count += 1
        matrix.append(col)
    return matrix

matrix_2D = []
for i in range(num_problems):     
    square_root = int(math.sqrt(len(arrlist[i])))
    matrix_2D.append(convert2D(arrlist[i], square_root, square_root))

def getInvCount(arr,N):
	arr1=[]
	for y in arr:
		for x in y:
			arr1.append(x)
	arr=arr1
	inv_count = 0
	for i in range(N * N - 1):
		for j in range(i + 1,N * N):
			# count pairs(arr[i], arr[j]) such that
			# i < j and arr[i] > arr[j]
			if (arr[j] and arr[i] and arr[i] > arr[j]):
				inv_count+=1
    
	return inv_count


# find Position of blank from bottom
def findXPosition(puzzle,N):
	# start from bottom-right corner of matrix
	for i in range(N - 1,-1,-1):
		for j in range(N - 1,-1,-1):
			if (puzzle[i][j] == 0):
				return N - i


# This function returns true if given
# instance of N*N - 1 puzzle is solvable

def isSolvable(puzzle,N):
	# Count inversions in given puzzle
	invCount = getInvCount(puzzle,N)

	# If grid is odd, return true if inversion
	# count is even.
	if (N % 2):
		return not(invCount % 2)

	else: # grid is even
		pos = findXPosition(puzzle,N)
		if (pos % 2):
			return not(invCount % 2)
		else:
			return invCount % 2


#TASK-2


class Problem:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def goal_test(self, state):
        return state == self.goal_state


# uncomment the heuristic if u want to use this


# # Misplaced Heuristic
# def calculate_heuristic(state, goal_state): 
#     misplaced = 0
#     n = len(state)
#     for i in range(n):
#         for j in range(n):
#             if state[i][j] != goal_state[i][j]:
#                 misplaced += 1
#     return misplaced

# Manhattan Distance Heuristic
def calculate_heuristic(state, goal_state):  
    distance = 0
    n = len(state)
    for i in range(n):
        for j in range(n):
            value = state[i][j]
            if value != 0:
                goal_position = find_goal_position(goal_state, value)
                distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
    return distance

def find_goal_position(goal_state, value):
    n = len(goal_state)
    for i in range(n):
        for j in range(n):
            if goal_state[i][j] == value:
                return (i, j)

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic = 0

    def __lt__(self, other): # Method which implicitly invoked to compare the priority values
        self_priority = self.path_cost + self.heuristic
        other_priority = other.path_cost + other.heuristic
        return self_priority < other_priority

    
    def solution(self):
        actions = []
        node = self
        while node.parent:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions

def actions(state):
    n = len(state)
    actions = []
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:
                if i > 0:
                    actions.append('UP')
                if i < n - 1:
                    actions.append('DOWN')
                if j > 0:
                    actions.append('LEFT')
                if j < n - 1:
                    actions.append('RIGHT')
    return actions

def find_zero_coordinates(state):
    n = len(state)
    for i in range(n):
        for j in range(n):
            if state[i][j] == 0:
                return i, j
    
def result(state, action):
    n = len(state)
    new_state = [row[:] for row in state]  # Create a copy of the state
    zero_i, zero_j = find_zero_coordinates(state)

    if action == 'UP':
        new_state[zero_i][zero_j] = new_state[zero_i - 1][zero_j]
        new_state[zero_i - 1][zero_j] = 0
    elif action == 'DOWN':
        new_state[zero_i][zero_j] = new_state[zero_i + 1][zero_j]
        new_state[zero_i + 1][zero_j] = 0
    elif action == 'LEFT':
        new_state[zero_i][zero_j] = new_state[zero_i][zero_j - 1]
        new_state[zero_i][zero_j - 1] = 0
    elif action == 'RIGHT':
        new_state[zero_i][zero_j] = new_state[zero_i][zero_j + 1]
        new_state[zero_i][zero_j + 1] = 0

    return new_state

def step_cost(state, action):
    return 1

def in_frontier(frontier, state):
    for _, node in frontier.queue:
        if node.state == state:
            return True
    return False


def A_Star_Search(problem):
    node = Node(problem.initial_state)
    node.heuristic = calculate_heuristic(node.state, problem.goal_state)
    node.path_cost = 0
    frontier = PriorityQueue() # frontier as priority queue
    frontier.put((node.path_cost + node.heuristic, node))
    explored = set()

    count = 0
    while not frontier.empty(): 
        print(count)
        _, node = frontier.get()

        if problem.goal_test(node.state): 
            return node

        explored.add(tuple(tuple(row) for row in node.state))  # Convert list state to tuple

        for action in actions(node.state):
            child_state = result(node.state, action)
            child_node = Node(child_state, node, action, node.path_cost + step_cost(node.state, action))
            child_node.heuristic = calculate_heuristic(child_node.state, problem.goal_state)
            
            existing_node = None
        
            # Checking existing in frontier 
            if in_frontier(frontier, child_node):
                for _, existing_node in frontier.queue:
                    if existing_node.state == child_node.state:
                        break
                    
            # Checking Node in explored set
            elif tuple(tuple(row) for row in child_node.state) in explored:
                continue

            # Checking status for existing node 
            if existing_node is not None:
                # if exist and have lower priority than new node then replace existing node
                if child_node.path_cost + child_node.heuristic < existing_node.path_cost + existing_node.heuristic:
                    frontier.queue.remove((existing_node.path_cost + existing_node.heuristic, existing_node))
                    frontier.put((child_node.path_cost + child_node.heuristic, child_node))
            else:
                # if not exist enter new node in frontier
                frontier.put((child_node.path_cost + child_node.heuristic, child_node))

        count += 1
    return None



# Kindly read instructions before runing code

if __name__ == '__main__':

    goal_state=[[[1,2],[3,0]],    # goal_state[0] for 2x2 
                [[1,2,3],[4,5,6],[7,8,0]], # goal_state[1] for 3x3
                [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]] # goal_state[2] for 4x4
    
    # matrix_2D[0] for [0 3 1 2] from file             
    # matrix_2D[1] for [0 3 2 1 6 4 8 7 5] from file   
    # matrix_2D[2] for [3 14 13 7 4 5 6 1 11 12 8 0 15 9 2 10] from file   
    # matrix_2D[3] for [4 8 7 5 0 3 2 1 6] from file   
    # matrix_2D[4] for [5 6 1 11 12 8 0 15 9 2 10 3 14 13 7 4] from file   
    
    initial_state=matrix_2D[1]
    
    N = len(initial_state)
    
    if isSolvable(initial_state,N):
        print("Problem is Solvable")

        # goal_state[0] for 2x2 
        # goal_state[1] for 3x3
        # goal_state[2] for 4x4
                
        problem = Problem(initial_state, goal_state[1])  
        solution_node = A_Star_Search(problem)
        if solution_node:
            actions = solution_node.solution()
            print("Actions:", "->".join(actions))
        else:
            print("Actions Not found.")
    else:
        print("Problem is Not Solvable !!")
