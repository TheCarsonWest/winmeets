

### Documentation for Winmeets

This Python script is designed for managing swim teams, including the creation of swimmer objects, team objects, and handling their data. The script can fetch data from URLs, save data to JSON files, and export data to Excel files. Additionally, it includes functionalities for calculating times and rankings for swimmers.

#### Dependencies
- `json`
- `requests`
- `random`
- `relay` (Assumed to be a custom module)
- `openpyxl`

### Functions

#### `string_to_time(str)`
Converts a time string in the format `mm:ss.ss` to a floating point number representing fractions of a day.

**Arguments:**
- `str`: Time string to be converted.

**Returns:**
- `float`: Time in fractions of a day.

#### `time_to_string(fraction_of_day)`
Converts a floating point number representing fractions of a day to a time string in the format `mm:ss.ss`.

**Arguments:**
- `fraction_of_day`: Time in fractions of a day.

**Returns:**
- `str`: Time string in the format `mm:ss.ss`.

#### `remove_last_word(sentence)`
Removes the last word from a given sentence.

**Arguments:**
- `sentence`: The input sentence.

**Returns:**
- `str`: The sentence with the last word removed.

### Classes

#### `Team`
A class representing a swim team. It can be initialized with a URL to fetch team data or with data from a JSON file.

**Attributes:**
- `name`: Name of the team.
- `url`: URL of the team's home page.
- `team_m`: List of male swimmers.
- `team_f`: List of female swimmers.

**Methods:**
- `__init__(self, url='b', u='l')`: Initializes the team object.
- `__str__(self)`: Returns a string representation of the team.
- `save(self)`: Saves the team data to a JSON file.
- `add(self, player, gender)`: Adds a swimmer to the team.
- `remove(self, player)`: Removes a swimmer from the team by name.
- `refresh(self, person=-1)`: Refreshes the team data.
- `save_to_workbook(self, template_file='./template.xlsx')`: Saves the team data to an Excel workbook.

#### `Swimmer`
A class representing a swimmer. It can be initialized with a URL to fetch swimmer data or with data from a JSON file.

**Attributes:**
- `name`: Name of the swimmer.
- `url`: URL of the swimmer's page.
- `times`: Dictionary of event times.

**Methods:**
- `__init__(self, url, u='u')`: Initializes the swimmer object.
- `__str__(self)`: Returns a string representation of the swimmer.
- `save(self)`: Saves the swimmer data in a format compatible with the `Team` class.

#### `Entry`
A class representing an entry in a swim meet.

**Attributes:**
- `entries`: Dictionary of events and their corresponding swimmers.
- `name`: Name of the entry.

**Methods:**
- `__init__(self, entries={}, name='Untitled team')`: Initializes the entry object.

### Helper Functions

#### `get_ranks(team, event, num, s=True)`
Returns the `num` fastest times for a specified event in a given team.

**Arguments:**
- `team`: The team object.
- `event`: The event name.
- `num`: Number of fastest times to return.
- `s`: Boolean indicating whether to consider male (`True`) or female (`False`) swimmers.

**Returns:**
- `list`: List of fastest times in `[name, time]` format.

#### `get_rank_obj(team, event, num, s=True)`
Returns a sorted list of swimmer objects with the fastest times for a specified event.

**Arguments:**
- `team`: The team object.
- `event`: The event name.
- `num`: Number of fastest times to return.
- `s`: Boolean indicating whether to consider male (`True`) or female (`False`) swimmers.

**Returns:**
- `list`: List of swimmer objects sorted by their time in the specified event.

#### `hs_meet(t, point_swimmers=4, divergence=[0, 0], fatigue=[False, 0, 0], point_scale=[20, 17, 16, 15, 14, 13, 12, 11, 9, 7, 6, 5, 4, 3, 2, 1])`
Simulates a high school swim meet with specified parameters.

**Arguments:**
- `t`: List of entry objects.
- `point_swimmers`: Number of swimmers allowed to compete for points.
- `divergence`: Random variability in times.
- `fatigue`: Fatigue settings.
- `point_scale`: Point scale for the meet.

#### `best_entries(team, count)`
Assigns the `count` best swimmers to each event.

**Arguments:**
- `team`: The team object.
- `count`: Number of best swimmers to assign.

**Returns:**
- `Entry`: Entry object with the best swimmers assigned to each event.

#### `genetic_entries(team)`
Generates entries using a genetic algorithm (Work in Progress).

---

this was gpt-ed btw