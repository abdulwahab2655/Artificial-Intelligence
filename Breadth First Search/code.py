from collections import deque

state = []
action = []
transition = []
testcase = []

with open("input.txt","r") as f:
    content = f.readline()
    array = content.split(" ")
    m = int(array[0])
    n = int(array[1])
    t = int(array[2])
    f.readline()


    # states
    for i in range(0, m):
        content = f.readline().strip("\n")
        state.append(content)


    f.readline()
    # action
    for i in range(0, n):
        content = f.readline()
        action.append(content.strip())


    f.readline()

    # transition
    for i in range(m):
        data = f.readline().split(" ")
        temp = []
        for j in data:
            j = j.strip("\n")
            temp.append(int(j))
        transition.append(temp)

    f.readline()
    # reading test
    for i in range(t):
        data = f.readline().split("\t")
        data[0] = data[0].strip()
        data[1] = data[1].strip()
        testcase.append(data)




class Node:

    def __init__(self, condition, parent=None, action=None):
        self.condition = condition
        self.parent = parent
        self.action = action


class Problem:
    def __init__(self, test_state, goal_state):
        self.testcase = test_state
        self.goalcase = goal_state

    def goalTest(self, current_state):
        if (self.goalcase == current_state):
            return True
        return False


def Solution(node):
    mystack = []
    while node.parent is not None:
        mystack.append(node.action)
        node = node.parent
    result = []
    while mystack:
        result.append(mystack.pop())
    display(result)


def display(actions):
    if not actions:
        print("No action Required")
    else:
        action_perform = '->'.join(action[v] for v in actions)
        print(action_perform)


def childNode(node, action):
    newChild = Node(transition[node.condition][action], node, action)
    return newChild


def BFS(problem):
    # Create the initial node and check if it is the goal
    N1 = Node(problem.testcase)
    if problem.goalTest(N1.condition):
        return Solution(N1)

    # Create a FIFO queue and add the initial node to it
    frontier = deque()
    frontier.append(N1)

    # Create a set to keep track of visited states
    reached = set()

    # Loop until the frontier is empty
    while len(frontier)>0:
        # Remove the first node from the frontier
        node = frontier.popleft()
        # Add in the explored set
        reached.add(node.condition)
        trans = transition[node.condition]

        # Iterate over the actions in the transition table
        for act, value in enumerate(trans):
            child = childNode(node, act)
            if child.condition not in reached and child not in frontier:
                if problem.goalTest(child.condition):
                    return Solution(child)
                frontier.append(child)


for i in range(t):
    print("Test Case" ,i )
    # print(test[i][0])
    # print(state.index(test[i][0]))       
    p = Problem(state.index(testcase[i][0]), state.index(testcase[i][1]))
    BFS(p)
