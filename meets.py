"""
Things to do add some point
make exportable to .hy3

"""

from data import *
from relay import *
import random

events_order = ['200 Y Medley Relay','200 Y Free','200 Y IM','50 Y Free','100 Y Fly','100 Y Free','500 Y Free','200 Y Free Relay','100 Y Back','100 Y Breast','400 Y Free Relay']

"""
Entries: {"Event" : [Swimmer, ...], ...}
Name: String
Date: Excel Format(Days since 1/1/1900) **NOT UNIX** 

"""
class Meet():
    def __init__(self, entries = {}, name = "Untitled Meet", date = 0): 
        self.entries = entries
        self.name = name
        self.date = date
    def __init__(self, hy3): # Imports meet entries from a hy3 file
        pass


"""
Team 1 (Meet Class)
Team 2 (Meet Class)
Point Scale: Default is the standard high school point scale
Point Swimmers: Most high school meets only allow 4 swimmers to compete for points

Divergence: [Lower, upper] The Random variability in times, how much percent can be added and dropped(scaled to wr) WIP
Fatigue: [Enabled, Decrease, Wear-off] WIP
 - Whether or not this feature is enabled
 - If fatigue is enabled, how much will it slow a swimmer down while doing consecutive events?
 - How many events will it take for fatigue to wear off(or how much time?)
"""
def duel_meet(t1, t2, point_scale = [20,17,16,15,14,13,12,11,9,7,6,5,4,3,2,1], point_swimmers = 4 ,divergence = [0,0], fatigue = [False,0,0]):
    s1 = 0
    s2 = 0
    for x in events_order: 
        event = []
        for t in [[t1,s1],[t2,s2]]: # turns the two entry lists for the event into one with [entry, team score]
            for x in t[0].entries[x]:
                event.append([x,t[1]])
        if x in ["200 Y Medley Relay","200 Y Free Relay","400 Y Free Relay"]: # Relays have different entry values than normal events, and have double points
            event.sort()
        else:
            event.sort(key=lambda x: x[0].times[x][0])  # sort by swimmer's best time
            for y in range(len(event)):
                event[y][1] += point_scale[y]
    
    print("s1= "+s1)
    print("s1= "+s2)