import random
import numpy as np
from master import *

# Parameters
POPULATION_SIZE = 1000
NUM_GENERATIONS = 100
MUTATION_RATE = 0.2
NUM_RELAY_SLOTS = 12  # 4 swimmers per relay * 3 relays

# Helper functions
def create_chromosome(swimmers):
    """Generate a chromosome with constraints:
       - Each swimmer appears at most once in a single relay.
       - Each swimmer appears at most twice in total.
    """
    swimmer_ids = list(range(len(swimmers)))  # Swimmer indices as IDs
    chromosome = [-1] * NUM_RELAY_SLOTS  # Placeholder chromosome
    
    used_counts = {sw: 0 for sw in swimmer_ids}  # Track swimmer usage

    def assign_relay(start, end):
        """Assign unique swimmers to a relay slot range."""
        available_swimmers = [sw for sw in swimmer_ids if used_counts[sw] < 2]
        relay_swimmers = random.sample(available_swimmers, end - start + 1)
        for i, sw in enumerate(relay_swimmers):
            chromosome[start + i] = sw
            used_counts[sw] += 1

    assign_relay(0, 3)  # 400 Free Relay
    assign_relay(4, 7)  # 200 Free Relay
    assign_relay(8, 11)  # 200 Medley Relay

    return chromosome


def decode_chromosome(chromosome):
    """Decode the chromosome into relay assignments."""
    return {
        "400 Free Relay": chromosome[:4],
        "200 Free Relay": chromosome[4:8],
        "200 Medley Relay": chromosome[8:12]
    }

def calculate_relay_time(relay, swimmers, relay_type):
    """Calculate the total time for a relay based on swimmer assignments."""
    if relay_type == "400 Free Relay":
        times = [swimmers[sw].times.get("100 Y Free", [float('inf')])[0] for sw in relay]
    elif relay_type == "200 Free Relay":
        times = [swimmers[sw].times.get("50 Y Free", [float('inf')])[0] for sw in relay]
    elif relay_type == "200 Medley Relay":
        strokes = ["100 Y Back", "100 Y Breast", "100 Y Fly", "100 Y Free"]
        times = [swimmers[sw].times.get(stroke, [float('inf')])[0] for sw, stroke in zip(relay, strokes)]
    
    if float('inf') in times:
        return float('inf')
    
    return sum(times) if relay_type != "200 Medley Relay" else sum(times) / 2

def fitness_function(chromosome, swimmers):
    """Calculate fitness (lower is better) with strict penalties for illegal relays."""
    relays = decode_chromosome(chromosome)
    total_time = 0
    used_swimmers = {}

    for relay_type, relay in relays.items():
        relay_time = calculate_relay_time(relay, swimmers, relay_type)
        
        if relay_time == float('inf'):  # Handle missing times
            return float('inf')  

        total_time += relay_time
        for swimmer in relay:
            used_swimmers[swimmer] = used_swimmers.get(swimmer, 0) + 1

    # **Strict Constraint Handling**
    # If any swimmer appears more than twice in total → DISQUALIFY relay
    if any(count > 2 for count in used_swimmers.values()):
        return float('inf')

    # If a swimmer appears multiple times in the same relay → DISQUALIFY relay
    for relay in relays.values():
        if len(relay) != len(set(relay)):  # Duplicate swimmers in the same relay
            return float('inf')

    return total_time  # No penalties needed if constraints are met


def select_parents(population, fitnesses):
    """Select two parents using tournament selection."""
    tournament = random.sample(list(zip(population, fitnesses)), k=5)
    tournament.sort(key=lambda x: x[1])  # Sort by fitness
    return tournament[0][0], tournament[1][0]





def crossover(parent1, parent2):
    """Perform single-point crossover."""
    point = random.randint(1, NUM_RELAY_SLOTS - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome):
    """Mutate a chromosome by swapping two random genes."""
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(NUM_RELAY_SLOTS), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]

def genetic_algorithm(team, gender="m"):

    """Run the genetic algorithm for a specified team and gender."""
    # Select the appropriate team (male or female)
    swimmers = team.team_m if gender == "m" else team.team_f
    # Create initial population
    population = [create_chromosome(swimmers) for _ in range(POPULATION_SIZE)]

    best_solution = None
    best_fitness = float("inf")

    for generation in range(NUM_GENERATIONS):
        print(best_fitness)
        # Calculate fitness for each chromosome
        fitnesses = [fitness_function(chromosome, swimmers) for chromosome in population]

        # Track best solution
        min_fitness_idx = np.argmin(fitnesses)
        if fitnesses[min_fitness_idx] < best_fitness:
            best_fitness = fitnesses[min_fitness_idx]
            best_solution = population[min_fitness_idx]

        # Selection and breeding
        next_generation = []
        for _ in range(POPULATION_SIZE // 2):
            parent1, parent2 = select_parents(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            next_generation.extend([child1, child2])

        population = next_generation

        if generation % 50 == 0:
            print(f"Generation {generation}: Best Fitness = {time_to_string(best_fitness)}")

    return decode_chromosome(best_solution), best_fitness

def display_chromosome(chromosome, swimmers):
    """Display the chromosome with swimmer names and their times."""
    if chromosome is None:
        return "No valid solution found."

    relays = chromosome
    display = {}

    for relay_type, relay in relays.items():
        display[relay_type] = []
        for sw in relay:
            swimmer = swimmers[sw]
            if relay_type == "400 Free Relay":
                event = "100 Y Free"
            elif relay_type == "200 Free Relay":
                event = "50 Y Free"
            elif relay_type == "200 Medley Relay":
                strokes = ["100 Y Back", "100 Y Breast", "100 Y Fly", "100 Y Free"]
                event = strokes[relay.index(sw)]
            time = swimmer.times[event][0] if event in swimmer.times else 1
            display[relay_type].append([swimmer.name, time_to_string(time)])

    return display
# Example usage
# Assuming you have a Team object named `my_team` already loaded
# You can call the genetic algorithm for the men's or women's team like this:
my_team = Team('William_Amos_Hough_High_School.json','j')
optimal_relays, best_time = genetic_algorithm(my_team, gender="m")
print("Optimal Relay Assignments (Men):", display_chromosome(optimal_relays,my_team.team_m))
print("Best Total Time:", time_to_string(best_time))
print("400 FR: "+time_to_string(calculate_relay_time(optimal_relays["400 Free Relay"],my_team.team_m,"400 Free Relay")))
print("200 FR: "+time_to_string(calculate_relay_time(optimal_relays["200 Free Relay"],my_team.team_m,"200 Free Relay")))
print("200 IM: "+time_to_string(calculate_relay_time(optimal_relays["200 Medley Relay"],my_team.team_m,"200 Medley Relay")))
