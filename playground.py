from master import *

teams = [Team("./jsons/West_Cabarrus_High_School.json","j"),Team('./cb/Marvin_Ridge_High_School.json','j')]


entries = []
for x in teams:
    entries.append(best_entries(x,4))

for x in entries:
    for y in x.entries:
        print(y)