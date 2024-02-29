from data import *
import random



backstroke_list = []
breaststroke_list = []
butterfly_list = []
freestyle_list = []

# Algorithm Variables
pop_size = 500 # how many individuals are in each generation. More = longer
gens = 50 # how many reproduction cycles the algorithm goes through

# Mutation Variables
mut_rate = 0 # how often mutation occurs
replace_num = [1,1] # when mutation occurs, how many people will be changed? random range. Hypothetically larger numbers will make more variation


def check_two_times(m, r1, r2, r3): # crimes against computer science here
    f1, f2, f3 = r1, r2, r3
    n_seen = []
    for x in m:
        for i in x:
            if i in n_seen:
                if i in f1:
                    f1.remove(i)
                if i in f2:
                    f2.remove(i)
                for k in f3:
                    if i in k:
                        k.remove(i)
            else:
                n_seen.append(i)
    return f1, f2, f3
    
def getRanks(team, event, num, s = True): # Returns the *num* fastest times in [name, time] format
    t = []
    f = []
    if s:
        for x in team.team_m:
            if event in x.times:
                t.append([x.name,x.times[event][0]])
            
        t = sorted(t, key=lambda x: x[1])
        for x in range(num):
            f.append(t[x])
        return f
        
    else: # Shot myself in the foot with these data structures, only way i know of doing this   
        for x in team.team_f:
            if event in x.times:
                t.append([x.name,x.times[event][0]])
            
        t = sorted(t, key=lambda x: x[1])
        for x in range(num):
            f.append(t[x])
        return f




def create_individual(): # Funamental flaw: the first generation has no repeats across the free relays. Enough generations will smooth this out.
    fr = freestyle_list
    random.shuffle(fr)
    fr_4 = fr[0:4]
    fr_2 = fr[4:8]
    medley = [ # currently lets duplicates through
        
        random.choice(backstroke_list),
        random.choice(breaststroke_list),
        random.choice(butterfly_list),
        fr[8]
    ]
    while len(set(item[0] for item in medley)) < len(medley):

        medley = [
            random.choice(backstroke_list),
            random.choice(breaststroke_list),
            random.choice(butterfly_list),
            fr[8]
        ]


    return [medley,fr_2,fr_4]

def fitness(r):
    relay_times = []
    for x in r:
        for i in x:
            relay_times.append(i[1])
    return sum(relay_times)

def crossover(p1, p2):
    child = []
    for relay_index in range(len(p1)):
        child_relay = []
        used_swimmers = set()  # Keep track of swimmers already added to the relay
        for swimmer_index in range(len(p1[relay_index])):
            # Randomly select a parent's swimmer for the current position
            selected_parent = random.choice([p1, p2])
            attempts = 0
            while attempts < 10:
                selected_swimmer = selected_parent[relay_index][swimmer_index]
                if selected_swimmer[0] not in used_swimmers:
                    # Check if the selected swimmer is not already in the other two relays
                    in_other_relays = any(selected_swimmer in other_relay for other_relay in (p1[i] if i != relay_index else p2[i] for i in range(len(p1))))
                    if not in_other_relays:
                        child_relay.append(selected_swimmer)
                        used_swimmers.add(selected_swimmer[0])
                        break
                # Retry with a different parent if conditions are not met
                selected_parent = p2 if selected_parent == p1 else p1
                attempts += 1
            else:
                # If unable to find a valid swimmer after multiple attempts, force mutate
                child_relay.append(random.choice(freestyle_list))  # Select a random swimmer from the list
        child.append(child_relay)
    return child





def mutate(relay, r): # Lets duplicates through right now
    m = relay
    if random.random() < r:
        for i in range(random.randint(replace_num[0], replace_num[1])):
            r_1 = random.randint(0, 2)
            r_2 = random.randint(0, 3)
            m[r_1][r_2] = True

        available_f_2 = [entry for entry in freestyle_list if entry not in relay[1]]
        available_f_4 = [entry for entry in freestyle_list if entry not in relay[2]]
        available_medley = []
        for x in [backstroke_list, breaststroke_list, butterfly_list, freestyle_list]:
            available_medley.append([entry for entry in x if entry not in relay[0]])

        available_f_2, available_f_4, available_medley = check_two_times(m, available_f_2, available_f_4, available_medley)

        for i in range(len(m[1])):
            if m[1][i] == True:
                s = random.choice(available_f_2)
                m[1][i] = s
                available_f_2.remove(s)

        available_f_2, available_f_4, available_medley = check_two_times(m, available_f_2, available_f_4, available_medley)

        for i in range(len(m[2])):
            if m[2][i] == True:
                s = random.choice(available_f_4)
                m[2][i] = s
                available_f_4.remove(s)

        available_f_2, available_f_4, available_medley = check_two_times(m, available_f_2, available_f_4, available_medley)

        for i, x in enumerate([[available_medley[0], m[0][0]], [available_medley[1], m[0][1]], [available_medley[2], m[0][2]], [available_medley[3], m[0][3]]]):
            if x[1] == True:
                s = random.choice(x[0])
                m[0][i] = s

    return m


def print_results(l):
        f = ''
        i = 0
        for x in ['200 Medley Relay','200 Free Relay','400 Free Relay']:
            f += f'{x}:\n'
            t = 0
            for y in l[i]:
                t += y[1]
                f += f"{y[0]}: {time_to_string(y[1])}\n"
            f += f'Time: {time_to_string(t)}\n'
            f +='\n'
            i +=1

        return f
        

def genetic_algorithm(t, population_size, generations, mutation_rate, g = True):
    global backstroke_list, breaststroke_list, butterfly_list, freestyle_list
    backstroke_list = getRanks(t, '100 Y Back', 5, g)
    breaststroke_list = getRanks(t, '100 Y Breast', 5, g)
    butterfly_list = getRanks(t, '100 Y Fly', 5, g)
    freestyle_list = getRanks(t, '100 Y Free', 12, g)
    population = [create_individual() for _ in range(population_size)] # inidividuals are a 3d list with 3 relays, 4 people on each relay, and a name and time with that person
    for i in range(generations):
        parents = sorted(population, key=fitness)[:len(population)//2] 
        offspring = []
        for x in parents:
            parent_1, parent_2 = random.sample(parents, 2)
            child = crossover(parent_1, parent_2)
            child = mutate(child, mutation_rate)

            offspring.append(child)
            
        population = parents + offspring
    return sorted(population, key=fitness)[0]



