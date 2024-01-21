import requests

class Team: # Team Class, contains the name of the team, and a list of Swimmer objects who are on the team. Usage: team = Team("<url of home page>")
    def __init__(self, url):
        self.url = url # for safekeeping the future
        
        self.html_m = requests.get(url+"roster/?page=1&gender=M&season_id=27&sort=perf").text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n") # Cuts down the HTML page to just the roster
        self.html_f = requests.get(url+"roster/?page=1&gender=F&season_id=27&sort=perf").text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n")
        
        self.html_m.pop(0)
        self.html_f.pop(0)
        
        self.name = self.html_m.split('<meta property="og:title" content="')[1].split('"')[0]
        
        self.team_m = []
        self.team_f = []
        for x in self.html_m:
            if "&ndash;" in x.split("</td>")[4]: # if they havent scored points, ignore
                break
            self.team_m.append(Swimmer("https://www.swimcloud.com"+x.split("</td>")[1].split("href=\"")[1].split("\">")[0]))
        for x in self.html_f:
            if "&ndash;" in x.split("</td>")[4]: # if they havent scored points, ignore
                break
            self.team_f.append(Swimmer("https://www.swimcloud.com"+x.split("</td>")[1].split("href=\"")[1].split("\">")[0]))
        
    
    
    
class Swimmer:
    def __init__(self, url):
        self.name = ""
        self.time = []
        
url = input("Input team home page\n > ")



