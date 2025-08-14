import json
import requests
import random

from openpyxl import load_workbook
import csv

# Add selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


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

def remove_last_word(sentence):
    words = sentence.rsplit(' ', 1)
    if len(words) > 1:
        return words[0]
    else:
        return ''


class Team: 
    """Team Class, contains:
    the name of the team:
    a list of Swimmer objects who are on the team. 
    Usage: team = Team("<url of home page>")"""
    def __init__(self, url = "b",u = "l",s = False):
        """
        Args:
            url (str, optional): The load mode. Defaults to "b".
            u (str, optional): _description_. Defaults to "l".
                - "j": Load from json file, just make the arg a file path
                - "u": Load from swimcloud url
            s (bool, optional): Whether or not to save after running. Defaults to False.
        """
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
            
            html_m = requests.get(url+"roster/?page=1&gender=M&season_id=28&sort=perf", headers=headers).text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n") # Cuts down the HTML page to just the roster
            html_f = requests.get(url+"roster/?page=1&gender=F&season_id=28&sort=perf", headers=headers).text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n")
            
            html_m.pop(0)
            html_f.pop(0)
            
            self.name = requests.get(url+"roster/?page=1&gender=M&season_id=28&sort=perf", headers=headers).text.split('<meta property="og:title" content="')[1].split('"')[0]
            
            self.team_m = []
            self.team_f = []
            for x in html_m:
                if 'href' not in x.split('            <td class="u-text-end">')[1]:
                    break
                self.team_m.append(Swimmer("https://www.swimcloud.com" + x.split("</td>")[1].split("href=\"")[1].split("\">")[0]))
                print(f"Added {self.team_m[-1].name}")
                if s:
                    self.save()
            for x in html_f:
                if 'href' not in x.split('            <td class="u-text-end">')[1]: ###
                    break
                self.team_f.append(Swimmer("https://www.swimcloud.com" + x.split("</td>")[1].split("href=\"")[1].split("\">")[0]))
                print(f"Added {self.team_f[-1].name}")
                if s:
                    self.save()

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
            print(x)
            f += x.save()
        f = f[0:len(f)-2]
        f += '\n\t],\n\t['
        for x in self.team_f:
            f += x.save()
        f = f[0:len(f)-2] # Gets rid of the last comma
        f += '\n\t]\n]'
        file = open(f"{self.name.replace(' ','_')}.json",'w')
        
        file.write(f)
    def add(self,player,gender="m"): # Adds Swimmer() to team_m or team_f
        if gender=="m":
            self.team_m.append(player)
        if gender=="f":
            self.team_f.append(player)
    def remove(self,player): # removes player by name
        for t in [self.team_m,self.team_f]:
            for p in range(len(t)):
                if t[p].name == player:
                    print("removed "+ str(t.pop(p)))
    def refresh(self,person = -1):  
        if person == -1:
            self = Team(self.url)

    def save_to_workbook(self, template_file = './template.xlsx'):
        # Load the template Excel file
        template_wb = load_workbook(template_file)
        
        # Get the desired sheet from the template file to combine data
        time_sheet = template_wb['Time Sheet']  # Assuming the sheet is named "Time Sheet"
        
        importer = []
        l = 2  # Starting row index
        
        for swimmer in self.team_m + self.team_f:
            s_name = swimmer.name
            for event, details in swimmer.times.items():
                r = [s_name]
                r.append(event)
                r.append(details[1])
                r.append("")  # Placeholder for the third column
                r.append(details[1])  # Assuming the same time
                r.append("")  # Placeholder for the sixth column
                r.append(details[0])  # String to time conversion (assuming it's the same format)
                r.append(swimmer in self.team_m)  # True for male, False for female
                r.append(f"=G{l}<HLOOKUP(B{l},Table7[#All],IF('Time Sheet'!H{l},3,2),FALSE)")
                importer.append(r)
                l += 1
        
        # Write data to the template sheet
        for row_data in importer:
            time_sheet.append(row_data)
        print("Time Sheet Created")
        
        # Add names to Boys and Girls sheets
        sheet_m = template_wb['Boys']
        sheet_f = template_wb['Girls']
        
        i = 2
        for swimmer in self.team_m:
            sheet_m[f"A{i}"] = swimmer.name
            i += 1
        
        i = 2
        for swimmer in self.team_f:
            sheet_f[f"A{i}"] = swimmer.name
            i += 1
        
        print('Names put in the sheet')
        
        # Save the workbook
        csv_filename = f"{self.name.replace(' ', '_')}.xlsx"
        template_wb.save(csv_filename)
        print(f"Workbook Saved as {csv_filename}")

    
class Swimmer:
    def __init__(self, url, u = "u"):
        if u == "l":
            # Loads from list(what a json load will do)
            
            self.name = url[0]
            self.url = url[1]
            self.times = url[2]

        else: # otherwise loads from url
            self.url = url
            print(f"Loading {url}/iframe/?splashes_type=fastest")
            chrome_options = Options()
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url + "/iframe/?splashes_type=fastest")
            time.sleep(1)
            html = driver.page_source
            driver.quit()

            soup = BeautifulSoup(html, "html.parser")

            # Extract swimmer name
            name_tag = soup.find("h1", class_="c-title")
            if name_tag and name_tag.a:
                self.name = name_tag.a.text.strip()
            else:
                self.name = "Unknown"

            self.times = {}
            # Find the fastest times table
            table = soup.find("table", class_="c-table-clean")
            if table:
                tbody = table.find("tbody")
                if tbody:
                    for row in tbody.find_all("tr"):
                        event_td = row.find("td", class_="u-text-truncate")
                        time_td = row.find("td", class_="u-text-end u-text-semi")
                        if event_td and time_td:
                            event_name = event_td.text.strip()
                            time_str = time_td.a.text.strip() if time_td.a else time_td.text.strip()
                            self.times[event_name] = [string_to_time(time_str), time_str]

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

"""
Entries: {"Event" : [Swimmer, ...], ...}
Name: String
Date: Excel Format(Days since 1/1/1900) **NOT UNIX** 

"""
class Entry():
    def __init__(self, entries = {}, name = "Untitled team"): 
        self.entries = entries
        self.name = name



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

