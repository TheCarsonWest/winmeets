from data import *
import random
import time

log = open(f'./{time.time()}','w')

# Algorithm Variables
pop_size = 50 # how many individuals are in each generation. More = longer
gens = 32 # how many reproduction cycles the algorithm goes through

# Mutation Variables
mut_rate = .1 # how often mutation occurs
replace_num = [1,3] # when mutation occurs, how many people will be changed? random range. Hypothetically larger numbers will make more variation


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


t = Team('./William_Amos_Hough_High_School.json','j')

backstroke_list = getRanks(t, '100 Y Back', 5)
breaststroke_list = getRanks(t, '100 Y Breast', 5)
butterfly_list = getRanks(t, '100 Y Fly', 5)
freestyle_list = getRanks(t, '100 Y Free', 12)


def create_individual(): # Funamental flaw: the first generation has no repeats across the free relays. Enough generations will smooth this out.
    fr = random.sample(freestyle_list,8)
    fr_4 = fr[0:4]
    fr_2 = fr[4:8]
    medley = [ # currently lets duplicates through
        
        random.choice(backstroke_list),
        random.choice(breaststroke_list),
        random.choice(butterfly_list),
        random.choice(freestyle_list)
    ]
    while len(set(item[0] for item in medley)) < len(medley):
        medley = [
            random.choice(backstroke_list),
            random.choice(breaststroke_list),
            random.choice(butterfly_list),
            random.choice(freestyle_list)
        ]


    return [medley,fr_2,fr_4]

def fitness(r):
    relay_times = []
    for x in r:
        for i in x:
            relay_times.append(i[1])
    return sum(relay_times)
    
def crossover(p1, p2): # Big problem: Occasionally there will be no possible way to not duplicate, meaning it has to be force mutated
    child = []
    seen = [[], []]
    for x in range(0, len(p1)):
          # Reset seen list for each relay
        r = []
        n = []
        for i in range(4):
            
            if p1[x][i][0] == p2[x][i][0]:  # if they are the same, just copy
                log.write('Copied equal value\n')
                r.append(p1[x][i])
            elif p1[x][i][0] in n:  # if one is a duplicate in the relay, use the other value
                log.write(f"prevented p1 {p1[x][i]} from duplicating with p2 {p2[x][i]}\n")
                r.append(p2[x][i])
            elif p2[x][i][0] in n:  # if one is a duplicate in the relay, use the other value
                log.write(f"prevented p2 {p2[x][i]} from duplicating with p1 {p1[x][i]}\n")
                r.append(p1[x][i])
                
            elif p1[x][i][0] in seen[1]:  # if name is already used in this relay, don't use it
                log.write(f'prevented triple {p1[x][i]} with {p2[x][i]} \n')
                r.append(p2[x][i])
            elif p2[x][i][0] in seen[1]:
                log.write(f'prevented triple\n')
                r.append(p1[x][i])
            else:  # If none of these scenarios occur, coinflip
                log.write('coinflipped\n')
                if random.random() > 0.5:
                    r.append(p1[x][i])
                else:
                    r.append(p2[x][i])
            n.append(r[-1][0])
            if r[-1][0] in seen[0] and r[-1][0] not in seen[1]:
                seen[1].append(r[-1][0])
            else:
                seen[0].append(r[-1][0])


        child.append(r)

    return child




def mutate(relay, r): # Will only error if the list sent into it is incomplete
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

    

def genetic_algorithm(population_size, generations, mutation_rate):
    population = [create_individual() for _ in range(population_size)] # inidividuals are a 3d list with 3 relays, 4 people on each relay, and a name and time with that person
    for i in range(generations):
        log.write(f"\n\tGeneration {i}\n\n")
        parents = sorted(population, key=fitness)[:len(population)//2] 
        offspring = []
        for x in parents:
            parent_1, parent_2 = random.sample(parents, 2)
            child = crossover(parent_1, parent_2)
            #child = mutate(child, mutation_rate)
            offspring.append(child)
        population = parents + offspring
    return sorted(population, key=fitness)[0]





best_individual = genetic_algorithm(pop_size, gens, mut_rate)
print(f"Best Relay Arrangement:\n{best_individual[0]}\n{best_individual[1]}\n{best_individual[2]}")
print("Total Relay Time:", time_to_string(fitness(best_individual)))

