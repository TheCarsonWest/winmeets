from data import *
import random

# Algorithm Variables
pop_size = 1000 # how many individuals are in each generation. More = longer
gens = 100 # how many reproduction cycles the algorithm goes through

# Mutation Variables
mut_rate = 0.1 # how often mutation occurs
replace_num = (1,3) # when mutation occurs, how many people will be changed? random range. Hypothetically larger numbers will make more variation


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
    fr_4 = fr[0:3]
    fr_2 = fr[4:7]
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
    
    
    
def crossover(p1, p2):
    child = []
    for x in range(0,2):
        r = []
        for i in range(0,3):
            if p1[x][i] == p2[x][i]: # if the same person is in the same spot in the same relay, just append it
                r.append(p1[x][i])
            else: # fundemental flaw: items towards the end will be changed less
                if p1[x][i] in r: # if the first parent doesnt pass the duplicate rules, use the second parent, vice versa
                    r.append(p2[x][i])
                elif p2[x][i] in r: # if the first parent doesnt pass the duplicate rules, use the second parent, vice versa
                    r.append(p1[x][i])
                else:
                    if random.random() > .5: # if no conflicts, coinflip
                        r.append(p1[x][i])
                    else:
                        r.append(p2[x][i])
        child.append(r)
    return child


def mutate(relay, r):
    m = relay
    if random.random() < r:

        
        for x in range(random.randint(replace_num)):
            r_1 = random.randint(0,2)
            r_2 = random.randint(0,3)
            m[r_1][r_2] = "Placeholder"

        available_f_2 = [entry for entry in freestyle_list if entry not in relay[1]] # every person not currrently in the 2 free relay
        available_f_4 = [entry for entry in freestyle_list if entry not in relay[2]] # every person not currrently in the 4 free relay
        available_medley = [] # every person not currrently in the 2 medley, 
        for x in [backstroke_list, breaststroke_list, butterfly_list, freestyle_list]:
            available_medley.append([entry for entry in x if entry not in relay[0]])
            
        # getting rid of everyone already in two relays    
        available_f_2, available_f_4, available_medley = check_two_times(m, available_f_2, available_f_4, available_medley)
            
        for x in m[1]: # 2fr, Replaces removed individuals with availabe ones, removes the one used
            if x == "Placeholder":
                s = random.choice(available_f_2)
                x = s
                available_f_2.remove(s)
        available_f_2, available_f_4, available_medley = check_two_times(m, available_f_2, available_f_4, available_medley)
        for x in m[2]: # 4fr, Replaces removed individuals with availabe ones, removes the one used
            if x == "Placeholder":
                s = random.choice(available_f_4)
                x = s
                available_f_4.remove(s)
        available_f_2, available_f_4, available_medley = check_two_times(m, available_f_2, available_f_4, available_medley)
        
        for x in [[available_medley[0],m[0][0]], [available_medley[1],m[0][1]], [available_medley[2],m[0][2]], [available_medley[3],m[0][3]]]:
            if x[1] == "Placeholder":
                s = random.choice(x[0])
                x[1] = s
            
    return m
    

def genetic_algorithm(population_size, generations, mutation_rate):
    population = [create_individual() for _ in range(population_size)] # inidividuals are a 3d list with 3 relays, 4 people on each relay, and a name and time with that person
    for i in range(generations):
        parents = population[:len(population)//2]
        offspring = []
        for x in parents:
            parent_1, parent_2 = random.sample(parents, 2)
            child = crossover(parent_1, parent_2)
            child = mutate(child, mutation_rate)
            offspring.append(child)
        population = parents + offspring
    return sorted(population, key=fitness)[0]





best_individual = genetic_algorithm(pop_size, gens, mut_rate)
print("Best Relay Arrangement:", best_individual)
print("Total Relay Time:", time_to_string(fitness(best_individual)))
