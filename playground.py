from master import *
from relay import *

#t = Team('https://www.swimcloud.com/team/10001012/')
t = Team('./William_Amos_Hough_High_School.json','j')
t.save()

optimal_relays, best_time = genetic_algorithm(t, gender="m")
print("Optimal Relay Assignments (Men):", display_chromosome(optimal_relays,t.team_m))
print("Best Total Time:", time_to_string(best_time))
print("400 FR: "+time_to_string(calculate_relay_time(optimal_relays["400 Free Relay"],t.team_m,"400 Free Relay")))
print("200 FR: "+time_to_string(calculate_relay_time(optimal_relays["200 Free Relay"],t.team_m,"200 Free Relay")))
print("200 IM: "+time_to_string(calculate_relay_time(optimal_relays["200 Medley Relay"],t.team_m,"200 Medley Relay")))
