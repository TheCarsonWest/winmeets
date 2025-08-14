from master import *
from relay import *
import pprint

t = Team('./University_of_Texas.json','j')

optimal_relays, best_time = genetic_algorithm(t, gender="m")
pp = pprint.PrettyPrinter(indent=4)
print("Optimal Relay Assignments (Men):")
pp.pprint(display_chromosome(optimal_relays, t.team_m))
print("Best Total Time:", time_to_string(best_time))
print("200 IM: " + time_to_string(calculate_relay_time(optimal_relays["200 Medley Relay"], t.team_m, "200 Medley Relay")))
print("200 FR: " + time_to_string(calculate_relay_time(optimal_relays["200 Free Relay"], t.team_m, "200 Free Relay")))
print("400 FR: " + time_to_string(calculate_relay_time(optimal_relays["400 Free Relay"], t.team_m, "400 Free Relay")))