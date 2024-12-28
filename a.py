import hytek
import json
from collections import defaultdict
import pandas as pd
import openpyxl  # For Excel export
import matplotlib.pyplot as plt
import os
import datetime

def get_event_name(event_code):
  """Converts a swimming event code into its full name.

  Args:
    event_code: A string representing the event code.

  Returns:
    A string representing the full name of the event.
  """

  distance = int(event_code[:-1])
  stroke = int(event_code[-1])

  stroke_names = {
      1: "Freestyle",
      2: "Backstroke",
      3: "Breaststroke",
      4: "Butterfly",
      5: "Individual Medley",
  }

  return f"{distance}m {stroke_names[stroke]}"


def group_tuples(tuples):
    """Groups tuples by their 3rd and 4th indices (event and heat)."""
    grouped_tuples = defaultdict(list)
    for t in tuples:
        grouped_tuples[(t[2], t[3])].append(t)
    return list(grouped_tuples.values())


def string_to_seconds(str):
    if str in ['DQ', 'NS', "DF", "SC"]:
        return -1
    f = 0
    if ":" in str:
        f += int(str.split(":")[0]) * 60
        f += int(str.split(":")[1].split(".")[0])
        try:
            f += int(str.split(".")[1]) / 100
        except IndexError:
            pass
    else:
        f += int(str.split(".")[0])
        try:
            f += int(str.split(".")[1]) / 100
        except IndexError:
            pass
    return f


def parse_line(line):
    name = line[7:39].strip()
    event = line[67:72].strip()
    e_num = line[72:75].strip()
    heat = line[:145].split()[-5] if line[:145].split()[
                                         -3] == "0" else line[:145].split()[-3]
    time = line[98:].split()[0][:-1]
    date_str = line[80:88]
    date = datetime.datetime.strptime(date_str, "%m%d%Y").date()
    return name, event, e_num, heat, string_to_seconds(time), date


def elo_calculation(ra, rb, k=32):
    """Calculates new Elo ratings after a match."""
    ea = 1 / (1 + 10 ** ((rb - ra) / 400))
    eb = 1 / (1 + 10 ** ((ra - rb) / 400))

    new_ra = ra + k * (1 - ea)  # Assuming player A wins
    new_rb = rb + k * (0 - eb)
    return new_ra, new_rb




def process_file(filepath, elo_ratings, elo_history, date, heat_results):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        meet_name = lines[1][11:85].strip()  # Extract meet name

    data_lines = [parse_line(x) for x in filter(lambda x: "D01" in x[0:3], lines)]
    data_lines.sort(key=lambda x: (x[2], x[3], x[4] if x[4] != -1 else float('inf')))
    data_lines = group_tuples(data_lines)


    for heat in data_lines:
        event_number = heat[0][2]
        event_type = heat[0][1]
        heat.sort(key=lambda x: x[4] if x[4] != -1 else float('inf'))
        heat_data = [] # List to store heat data

        for i in range(len(heat)):
            swimmer_a = heat[i][0]
            initial_elo = elo_ratings[event_type][swimmer_a] # Store initial ELO

            for j in range(i + 1, len(heat)):
                swimmer_b = heat[j][0]

                #Store initial ELOs for both swimmers before calculation
                initial_elo_a = elo_ratings[event_type][swimmer_a]
                initial_elo_b = elo_ratings[event_type][swimmer_b]

                elo_ratings[event_type][swimmer_a], elo_ratings[event_type][swimmer_b] = elo_calculation(
                    elo_ratings[event_type][swimmer_a], elo_ratings[event_type][swimmer_b])


                # Calculate and store ELO changes
                elo_change_a = elo_ratings[event_type][swimmer_a] - initial_elo_a
                elo_change_b = elo_ratings[event_type][swimmer_b] - initial_elo_b


                elo_history[swimmer_a][event_type].append((elo_ratings[event_type][swimmer_a], event_number, get_event_name(event_type), meet_name, str(date), elo_change_a))
                elo_history[swimmer_b][event_type].append((elo_ratings[event_type][swimmer_b], event_number, get_event_name(event_type), meet_name, str(date), elo_change_b))

            # Append heat data for swimmer_a
            heat_data.append({
                "swimmer": swimmer_a,
                "time": heat[i][4],
                "elo_change": elo_ratings[event_type][swimmer_a] - initial_elo, # Use the initial ELO stored earlier
            })

        heat_results[(meet_name, get_event_name(event_type), heat[0][3])] = heat_data
    return elo_ratings, elo_history



folder_path = './ye/'  # Replace with the path to your folder
heat_results = {} # Initialize heat_results
elo_ratings = defaultdict(lambda: defaultdict(lambda: 1000))  # Initialize Elo ratings
elo_history = defaultdict(lambda: defaultdict(list))



files = []
for root, _, filenames in os.walk(folder_path):
    for filename in filenames:
        if filename.endswith(".cl2"):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                first_line = next((line for line in f if "D01" in line[0:3]), None)
                if first_line:
                    date_str = first_line[80:88]
                    date = datetime.datetime.strptime(date_str, "%m%d%Y").date()
                    files.append((filepath, date))






files.sort(key=lambda x: x[1]) # Sort files by date
for file, date in files:
    elo_ratings, elo_history = process_file(file, elo_ratings, elo_history, date, heat_results)


with open("heat_results.json", "w") as f:
    f.write(str(heat_results))


# Extract and sort final ELOs
final_elos = {}
for swimmer, events in elo_history.items():
    last_elos_per_event = []
    for event, elo_list in events.items():
        if elo_list:  # Check if the list is not empty
            last_elos_per_event.append(elo_list[-1])
    if last_elos_per_event:  # Only add swimmers with ELO entries
        # Sort by event number within the list of last ELOs
        last_elos_per_event.sort(key=lambda x: x[1])
        final_elos[swimmer] = last_elos_per_event[-1][0]  # Get the last ELO value

# Sort final_elos by ELO score in descending order
sorted_final_elos = dict(sorted(final_elos.items(), key=lambda item: item[1], reverse=True))

open("elo_ratings.txt", 'w').write(json.dumps(sorted_final_elos, indent=4))

final_elos = {}
for swimmer, events in elo_history.items():
    a = []
    for event, elo_list in events.items():
        a.append(elo_list[-1])
    final_elos[swimmer] = a

open("elo_history.txt", 'w').write(json.dumps(final_elos, indent=4))

