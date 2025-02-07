from master import *
from relay import *

t = Team('https://www.swimcloud.com/team/4338/')
t.save()



my_team = t
optimal_relays, best_time = genetic_algorithm(my_team, gender="m")
print("Optimal Relay Assignments (Men):", display_chromosome(optimal_relays,my_team.team_m))
print("Best Total Time:", time_to_string(best_time))
print("400 FR: "+time_to_string(calculate_relay_time(optimal_relays["400 Free Relay"],my_team.team_m,"400 Free Relay")))
print("200 FR: "+time_to_string(calculate_relay_time(optimal_relays["200 Free Relay"],my_team.team_m,"200 Free Relay")))
print("200 IM: "+time_to_string(calculate_relay_time(optimal_relays["200 Medley Relay"],my_team.team_m,"200 Medley Relay")))
