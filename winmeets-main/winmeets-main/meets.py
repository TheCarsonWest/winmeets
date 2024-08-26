"""
Things to do add some point
make exportable to .hy3

"""

from data import *
from relay import *
import random

events_order = ['200 Y Medley Relay Women','200 Y Medley Relay Men','200 Y Free Women','200 Y Free Men','200 Y IM Women','200 Y IM Men','50 Y Free Women','50 Y Free Men','100 Y Fly Women','100 Y Fly Men','100 Y Free Women','100 Y Free Men','500 Y Free Women','500 Y Free Men','200 Y Free Relay Women','200 Y Free Relay Men','100 Y Back Women','100 Y Back Men','100 Y Breast Women','100 Y Breast Men','400 Y Free Relay Women','400 Y Free Relay Men']

"""
Entries: {"Event" : [Swimmer, ...], ...}
Name: String
Date: Excel Format(Days since 1/1/1900) **NOT UNIX** 

"""
class Entry():
    def __init__(self, entries = {}, name = "Untitled team"): 
        self.entries = entries
        self.name = name

"""
t : [Entry class, ...]
Point Scale: Default is the standard high school point scale
Point Swimmers: Most high school meets only allow 4 swimmers to compete for points

Divergence: [Lower, upper] The Random variability in times, how much percent can be added and dropped(scaled to wr) WIP
Fatigue: [Enabled, Decrease, Wear-off] WIP
 - Whether or not this feature is enabled
 - If fatigue is enabled, how much will it slow a swimmer down while doing consecutive events?
 - How many events will it take for fatigue to wear off(or how much time?)
"""
def hs_meet(t, point_swimmers = 4 ,divergence = [0,0], fatigue = [False,0,0],point_scale = [20,17,16,15,14,13,12,11,9,7,6,5,4,3,2,1]):
    s = [] # Scores for each team
    for x in t:
        s.append(0)
    for x in events_order: 
        event = []
        for i in range(len(t)-1): # turns the two entry lists for the event into one with [entry, team score]
            for x in t[i].entries[x]:
                print(x)
                event.append([x,t[1]])
        if x in ["200 Y Medley Relay","200 Y Free Relay","400 Y Free Relay"]: # Relays have different entry values than normal events, and have double points
            event.sort()
        else:
            event.sort(key=lambda x: x[0].times[x][0])  # sort by swimmer's best time
            for y in range(len(event)):
                event[y][1] += (y < len(point_scale) - 1) if point_scale[y] else 0
    

def best_entries(team, count): # Cheats and simply assigns the <count> best swimmers to each event, genetic algorithms relays
    # Not legal event entries
    events = {}
    for x in events_order:
        if x in ["200 Y Medley Relay Men","200 Y Free Relay Men","400 Y Free Relay Men","200 Y Medley Relay Women","200 Y Free Relay Women","400 Y Free Relay Women"]:
            pass
        else:
            events[x+"Men" in x if " Men" else " Women"] = get_rank_obj(team,x,count,"Men" in x)
    best_relays = genetic_algorithm(team,10000,0,0)
    events["200 Y Medley Relay Men"] = best_relays[0]
    events["200 Y Free Relay Men"] = best_relays[1]
    events["400 Y Free Relay Men"] = best_relays[2]

    best_relays = genetic_algorithm(team,10000,0,0,False)
    events["200 Y Medley Relay Women"] = best_relays[0]
    events["200 Y Free Relay Women"] = best_relays[1]
    events["400 Y Free Relay Women"] = best_relays[2]


    return Entry(events,team.name)

def genetic_entries(team): # Genetic algorithms entries WIP
    pass