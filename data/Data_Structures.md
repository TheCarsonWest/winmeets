# SwimCloud Team and Swimmer Data Structures

## Team Class

### `Team(url, u="l")`
- Represents a swim team on SwimCloud.
- Parameters:
  - `url`: The URL of the SwimCloud home page for the team.
  - `u`: Optional parameter, default is "l". If "l", the class will fetch data from the provided URL; if "j", it will import data from a JSON file.
- Attributes:
  - `name`: The name of the team.
  - `url`: The URL of the SwimCloud home page for the team.
  - `team_m`: A list of male swimmers (Swimmer objects) on the team.
  - `team_f`: A list of female swimmers (Swimmer objects) on the team.

### `__str__()`
- Returns a string representation of the team, including the team name, URL, and a list of male and female swimmers.

### `save()`
- Saves the team data in a JSON format. The saved file will have the team name as the filename.

## Swimmer Class

### `Swimmer(url, u="u")`
- Represents an individual swimmer on SwimCloud.
- Parameters:
  - `url`: The URL of the SwimCloud profile page for the swimmer.
  - `u`: Optional parameter, default is "u". If "u", the class will fetch data from the provided URL; if "l", it will import data from a JSON file.
- Attributes:
  - `name`: The name of the swimmer.
  - `url`: The URL of the SwimCloud profile page for the swimmer.
  - `times`: A dictionary containing event names as keys and corresponding swim times as values. The swim times are represented as a list containing a float and a string (for human-readable time).

### `__str__()`
- Returns a string representation of the swimmer, including the swimmer's name, URL, and a list of swim times for various events.

### `save()`
- Saves the swimmer data in a format suitable for JSON. The saved data includes the swimmer's name, URL, and swim times.
- This will typically just be used to send up to the Team() `save()` function
## Important Note
- If a swimmer does not have their SwimCloud profiles merged, not all of their times may be displayed. This issue is significant for high school teams, where swimmers may have separate profiles for high school and club events. A guide on resolving this issue is available [here](https://support.swimcloud.com/hc/en-us/articles/115004776054-I-have-duplicate-profiles).

## Conversion Formula for Swim Times
- The swim times are represented as a float corresponding to the fraction of a day. The formula for conversion is: `(<Minutes>*60 + <Seconds>) / 86400`.

---

**Note**: I made this with chatgpt because I have better uses for my time than writing docuemntation to code nobody else is going to use.

Last update 1/28/24