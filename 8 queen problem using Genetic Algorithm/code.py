import random

def generate_random_state():
    state = []
    for i in range(8):
        state.append(random.randint(0, 7))
    return state

def random_selection(population, fitness):
    probabilities = [fitness(states) for states in population]
    total_fitness = sum(probabilities)
    probabilities = [fitness / total_fitness for fitness in probabilities]
    return random.choices(population, probabilities)[0]

def mutate(states):
    mutated_states = list(states)
    index = random.randint(0, len(mutated_states) - 1)
    value = random.randint(0, len(mutated_states) - 1)
    mutated_states[index] = value
    return mutated_states

def fitness(states):
    attacks = 0
    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            if states[i] == states[j] or abs(states[i] - states[j]) == abs(i - j):
                attacks += 1
    fitness = 28 - attacks 
    return fitness

def genetic_algorithm(population, fitness):
    while True:
        new_population = []
        for _ in range(len(population)):
            parent_x = random_selection(population, fitness)
            parent_y = random_selection(population, fitness)
            child = crossover(parent_x, parent_y)
            if random.random() <= MUTATION_RATE:
                child = mutate(child)
            new_population.append(child)

        population = new_population
        best_states = max(population, key=lambda ind: fitness(ind))

        if fitness(best_states) == FIT_THRESHOLD:
            return best_states, fitness(best_states)

def crossover(x, y):
    n = len(x)
    c = random.randint(0, n-1)
    child = x[:c] + y[c:]
    return child

POPULATION_SIZE = 8
FIT_THRESHOLD = 28
MUTATION_RATE = 0.05

# Generate the initial population
initial_population = [generate_random_state() for _ in range(POPULATION_SIZE)]

best_states, best_fitness = genetic_algorithm(initial_population, fitness)

print("Best states:", best_states)
print("Fitness of best states:", best_fitness)

