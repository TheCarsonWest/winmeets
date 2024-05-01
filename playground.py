from data import *
from relay import *
"""
team = ["https://www.swimcloud.com/swimmer/2297622/",
"https://www.swimcloud.com/swimmer/2731807/",
"https://www.swimcloud.com/swimmer/911875/",
"https://www.swimcloud.com/swimmer/2074030/",
"https://www.swimcloud.com/swimmer/2603790/",
"https://www.swimcloud.com/swimmer/1347618/",
"https://www.swimcloud.com/swimmer/1256363/",
"https://www.swimcloud.com/swimmer/659494/",
]

hough_24 = Team()
hough_24.name = "Hough 2024-2025"
for x in team:
    hough_24.add(Swimmer(x),'m')

hough_24.save()
"""

best = genetic_algorithm(Team("./Hough_2024-2025.json","j"),100000,0,0)
print("2024-2025 Best Relay(Without Nikita)")
print(print_results(best))
print("2023-2024 Best Relay Combination")
print(print_results(genetic_algorithm(Team("./cb/William_Amos_Hough_High_School.json","j"),100000,0,0)))
