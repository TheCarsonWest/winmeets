from data import *
from relay import *
import os
directory = './cb'

files = []


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        files.append(f)

for f in files:
    t = Team(f,'j')
    best_individual = genetic_algorithm(t ,50000, 0, 0)

    print(f"Total Relay Time for {t.name}:", time_to_string(fitness(best_individual)))
