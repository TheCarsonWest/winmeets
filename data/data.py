import requests
def string_to_time(str):
    
      f = 0
      if ":" in str:
        f += int(str.split(":")[0])*60
        f += int(str.split(":")[1].split(".")[0])
        f += int(str.split(".")[1])/100
      else:
            f+= int(str.split(".")[0])
            f+= int(str.split(".")[1])/100
      return f/86400

class Team: # Team Class, contains the name of the team, and a list of Swimmer objects who are on the team. Usage: team = Team("<url of home page>")
    def __init__(self, url):
        self.url = url # for safekeeping the future
        
        self.html_m = requests.get(url+"roster/?page=1&gender=M&season_id=27&sort=perf").text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n") # Cuts down the HTML page to just the roster
        self.html_f = requests.get(url+"roster/?page=1&gender=F&season_id=27&sort=perf").text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n")
        
        self.html_m.pop(0)
        self.html_f.pop(0)
        
        self.name = requests.get(url+"roster/?page=1&gender=M&season_id=27&sort=perf").text.split('<meta property="og:title" content="')[1].split('"')[0]
        
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
        self.url = url
        html = requests.get(url).text.split("<body")[1].split('<span class="u-mr-">')[1]
        self.name = html.split('</span>')[0]
        self.times = {}
        table = html.split("<tbody>")[2].split("</tbody>")[0].split("</tr>")
        print(table)
        for x in table:
            td = x.split("</td>")
            self.times[td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0]] = string_to_time(td[1].split("</a>")[0].split('">')[2])

                 
        
hough = Team('https://www.swimcloud.com/team/10001012/')

print(hough)