from data import *
from relay import *
import os
directory = './jsons'

files = []


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        files.append(f)

for f in files:
    t = Team(f,'j')
    best_individual = genetic_algorithm(t ,500, 50, 0)
    print(f"Best Relay Arrangement for {t.name}:\n\n{print_results(best_individual)}")
    print("Total Relay Time:", time_to_string(fitness(best_individual)))