

import json
import requests
def string_to_time(str): # mm:ss.ss -> Float point in fractions of a day
    
      f = 0
      if ":" in str:
        f += int(str.split(":")[0])*60
        f += int(str.split(":")[1].split(".")[0])
        f += int(str.split(".")[1])/100
      else:
            f+= int(str.split(".")[0])
            f+= int(str.split(".")[1])/100
      return f/86400

def time_to_string(fraction_of_day): # Day Fraction float point -> mm:ss.ss
    # Convert fraction_of_day to total seconds
    total_seconds = fraction_of_day * 86400

    # Calculate minutes and seconds
    minutes, seconds = divmod(total_seconds, 60)

    # Format the result as mm:ss.00
    result = f"{int(minutes):02}:{int(seconds):02}.{int((seconds % 1) * 100):02}"
    
    return result

class Team: # Team Class, contains the name of the team, and a list of Swimmer objects who are on the team. Usage: team = Team("<url of home page>")
    def __init__(self, url = "b",u = "l"):
        if u == 'j': # Json team loader
            t = json.loads(open(url,"r").read())
            self.name = t[0][0]
            self.url = t[0][1]

            self.team_m = []
            self.team_f = []
            for x in t[1]:
                self.team_m.append(Swimmer(x,"l"))
            for x in t[2]:
                self.team_f.append(Swimmer(x,"l"))
        elif url == "b": # Blank team loader
            self.team_m = []
            self.team_f = []
            self.url = "Blank"
            self.name = "Unnamed"
        else: # url loader
            print('Url detected, finding data')
            self.url = url # for safekeeping the future
            
            html_m = requests.get(url+"roster/?page=1&gender=M&season_id=27&sort=perf").text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n") # Cuts down the HTML page to just the roster
            html_f = requests.get(url+"roster/?page=1&gender=F&season_id=27&sort=perf").text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n")
            
            html_m.pop(0)
            html_f.pop(0)
            
            self.name = requests.get(url+"roster/?page=1&gender=M&season_id=27&sort=perf").text.split('<meta property="og:title" content="')[1].split('"')[0]
            
            self.team_m = []
            self.team_f = []
            for x in html_m:
                if "&ndash;" in x.split("</td>")[4]: # if they havent scored points, ignore
                    break
                self.team_m.append(Swimmer("https://www.swimcloud.com"+x.split("</td>")[1].split("href=\"")[1].split("\">")[0]))
                print(f"Added {self.team_m[-1].name}")
            for x in html_f:
                if "&ndash;" in x.split("</td>")[4]: # if they havent scored points, ignore
                    break
                self.team_f.append(Swimmer("https://www.swimcloud.com"+x.split("</td>")[1].split("href=\"")[1].split("\">")[0]))
                print(f"Added {self.team_f[-1].name}")

    def __str__(self): # to string(very long)
        f = ''
        f += f"{self.name}\n{self.url}\n\nMen:\n"
        for x in self.team_m:
            f += str(x)
            f += '\n'
        f += "\n\nWomen:\n"
        for x in self.team_f:
            f += str(x)
            f += '\n'
        return f
    def save(self): # Saves file to json
        f = f'[ [\n"{self.name}",\n"{self.url}"\n],\n\t[\n'
        for x in self.team_m:
            f += x.save()
        f = f[0:len(f)-2]
        f += '\n\t],\n\t['
        for x in self.team_f:
            f += x.save()
        f = f[0:len(f)-2] # Gets rid of the last comma
        f += '\n\t]\n]'
        file = open(f"{self.name.replace(' ','_')}.json",'w')
        
        file.write(f)
    def add(self,player,gender): # Adds Swimmer() to team_m or team_f
        if gender=="m":
            self.team_m.append(player)
        if gender=="f":
            self.team_f.append(player)
    def remove(self,player): # removes player by name
        for t in [self.team_m,self.team_f]:
            for p in range(len(t)):
                if t[p].name == player:
                    print("removed "+ t.pop(p))
    def refresh(self,person = -1):
        if person == -1:
            self = Team(self.url)


                    



    
class Swimmer:
    def __init__(self, url, u = "u"):
        if u == "l": # Loads from list(what a json load will do)
            
            self.name = url[0]
            self.url = url[1]
            self.times = url[2]

        else: # otherwise loads from url
            self.url = url
            html = requests.get(url).text.split("<body")[1].split('<span class="u-mr-">')[1]
            self.name = html.split('</span>')[0] # Scraping name from top of page
            self.times = {}
            table = html.split("<tbody>")[2].split("</tbody>")[0].split("</tr>")
            table.pop(-1)
            for x in table:
                
                td = x.split("</td>") # Scraping the times table
                self.times[td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0]] = [string_to_time(td[1].split("</a>")[0].split('">')[2]),td[1].split("</a>")[0].split('">')[2]]
    def __str__(self):
        f = '' # Prints name an times
        f += f'{self.name}\n{self.url}\n'
        for x in self.times:
            f += str(x)+':  ' + self.times[x][1]
            f +='\n'
        return f
    def save(self): # formats to conform with Team() json
        f = f'\t\t[\n\t\t\t"{self.name}", "{self.url}",\n\t\t\t'+'{'
        for x in self.times:             
            f += f'\n\t\t\t\t"{str(x)}" : {self.times[x]},'.replace("'",'"')
        f = f[0:len(f)-1]
        f += '\n\t\t\t}\n\t\t],\n'
        return f
    

def get_ranks(team, event, num, s = True): # Returns the *num* fastest times in [name, time] format
    t = []
    f = []
    if s:
        for x in team.team_m:
            if event in x.times:
                t.append([x.name,x.times[event][0]])
            
        t = sorted(t, key=lambda x: x[1])
        for x in range(num):
            f.append(t[x])
        return f
        
    else: # Shot myself in the foot with these data structures, only way i know of doing this   
        for x in team.team_f:
            if event in x.times:
                t.append([x.name,x.times[event][0]])
            
        t = sorted(t, key=lambda x: x[1])
        for x in range(num):
            f.append(t[x])
        return f
    

def get_rank_obj(team, event, num, s=True):
  """Returns a sorted list of Swimmer objects with the fastest times for an event.

  Args:
      team: Team object containing swimmer data.
      event: Event name (e.g., "100 Free").
      num: Number of fastest times to return.
      s: Flag indicating men's (True) or women's (False) swimmers.

  Returns:
      A list of Swimmer objects sorted by their time in the specified event.
  """

  swimmers = []
  if s:
    for swimmer in team.team_m:
      if event in swimmer.times:
        swimmers.append(swimmer)
  else:
    for swimmer in team.team_f:
      if event in swimmer.times:
        swimmers.append(swimmer)

  # Sort swimmers by their time in the specified event
  swimmers.sort(key=lambda swimmer: swimmer.times[event][0])

  return swimmers[:num]