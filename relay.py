from . import data
import random
import copy

def getRanks(team, event, num, s = True): 
    t = []
    if s:
        for x in team.team_m:
            t.append([x.name,x.times[event]])
        
    else: # Shot myself in the foot with these data structures, only way i know of doing this   
        for x in team.team_f: 
            print('s')


t = data.Team('https://www.swimcloud.com/team/10001012/')
t.save()
# Everything below is ai generated, no clue if it works




# Function to perform crossover and mutation
def crossover_and_mutate(selected_parents):
    new_generation = []

    while len(new_generation) < population_size:
        # Select two parents for crossover
        parent1, parent2 = random.sample(selected_parents, 2)

        # Perform crossover (you can choose different crossover methods)
        crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        # Perform mutation (you can choose different mutation methods)
        mutate_child(child1)
        mutate_child(child2)

        # Add children to the new generation
        new_generation.append(child1)
        new_generation.append(child2)

    return new_generation

# Function to perform mutation on an individual
def mutate_child(child):
    # Define mutation rate (adjust as needed)
    mutation_rate = 0.1

    for relay, pairs in child.items():
        for i in range(len(pairs)):
            # Apply mutation with a certain probability
            if random.random() < mutation_rate:
                # Replace a pair with a new random one from the corresponding table
                if relay == "200_medley_relay":
                    # For medley relay, select from the corresponding table
                    if i == 0:
                        child[relay][i] = random.choice(backstroke_table)
                    elif i == 1:
                        child[relay][i] = random.choice(breaststroke_table)
                    elif i == 2:
                        child[relay][i] = random.choice(butterfly_table)
                    elif i == 3:
                        child[relay][i] = random.choice(freestyle_table)
                else:
                    # For freestyle relays, select from the freestyle table
                    child[relay][i] = random.choice(freestyle_table)

# Input tables, should have just enough information for the theoretical perfect relay
backstroke_table = getRanks(t, "100 Y Back",5, True)  # List of 5 name-time pairs for 100 Backstroke
breaststroke_table = getRanks(t, "100 Y Breast",5, True)  # List of 5 name-time pairs for 100 Breaststroke
butterfly_table = getRanks(t, "100 Y Fly",5, True)  # List of 5 name-time pairs for 100 Butterfly
freestyle_table = getRanks(t, "100 Y Free",8)  # List of 8 name-time pairs for 100 Freestyle

# Define relay lengths
relay_lengths = {
    "200_freestyle_relay": 4,
    "400_freestyle_relay": 4,
    "200_medley_relay": 4
}

# Define the number of generations and population size
num_generations = 100
population_size = 50

# Function to generate a random individual
def generate_individual():
    # Randomly select name-time pairs for each relay from the tables
    individual = {
        "200_freestyle_relay": random.sample(freestyle_table, relay_lengths["200_freestyle_relay"]),
        "400_freestyle_relay": random.sample(freestyle_table, relay_lengths["400_freestyle_relay"]),
        "200_medley_relay": [
            random.choice(backstroke_table),
            random.choice(breaststroke_table),
            random.choice(butterfly_table),
            random.choice(freestyle_table)
        ]
    }
    return individual

# Function to calculate fitness (sum of relay times)
def calculate_fitness(individual):
    return sum([sum(pair[1] for pair in relay) for relay in individual.values()])

# Genetic algorithm
def genetic_algorithm():
    population = [generate_individual() for _ in range(population_size)]

    for generation in range(num_generations):
        # Evaluate fitness for each individual
        fitness_scores = [(calculate_fitness(ind), ind) for ind in population]

        # Sort population by fitness
        population = [ind for _, ind in sorted(fitness_scores)]

        # Select the top individuals for reproduction (you can implement various selection methods)
        selected_parents = population[:population_size // 2]

        # Generate new individuals through crossover and mutation (you need to implement these)
        new_generation = crossover_and_mutate(selected_parents)

        # Replace the old generation with the new one
        population = new_generation

    # Get the best individual from the final generation
    best_individual = min([(calculate_fitness(ind), ind) for ind in population], key=lambda x: x[0])[1]

    return best_individual

# You need to implement the crossover_and_mutate function according to your requirements

# Example usage
best_solution = genetic_algorithm()
print("Best solution:", best_solution)
print("Fitness:", calculate_fitness(best_solution))
