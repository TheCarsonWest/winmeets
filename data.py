""" 
In the future:
- Make methods to add people and times
"""
import json
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
    def __init__(self, url,u = "l"):
        if u == 'j':
            print('importing list to object') # doesnt work yet

            t = json.loads(open(url,"r").read())
            self.name = t[0][0]
            self.url = t[0][1]

            self.team_m = []
            self.team_f = []
            for x in t[1]:
                self.team_m.append(Swimmer(x,"l"))
            for x in t[2]:
                self.team_f.append(Swimmer(x,"l"))

        else:
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

    def __str__(self):
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
    def save(self):
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

    
class Swimmer:
    def __init__(self, url, u = "u"):
        if u == "l":
            
            self.name = url[0]
            self.url = url[1]
            self.times = url[2]

        else:
            self.url = url
            html = requests.get(url).text.split("<body")[1].split('<span class="u-mr-">')[1]
            self.name = html.split('</span>')[0]
            self.times = {}
            table = html.split("<tbody>")[2].split("</tbody>")[0].split("</tr>")
            table.pop(-1)
            for x in table:
                
                td = x.split("</td>")
                self.times[td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0]] = [string_to_time(td[1].split("</a>")[0].split('">')[2]),td[1].split("</a>")[0].split('">')[2]]
    def __str__(self):
        f = ''
        f += f'{self.name}\n{self.url}\n'
        for x in self.times:
            f += str(x)+':  ' + self.times[x][1]
            f +='\n'
        return f
    def save(self):
        f = f'\t\t[\n\t\t\t"{self.name}", "{self.url}",\n\t\t\t'+'{'
        for x in self.times:             
            f += f'\n\t\t\t\t"{str(x)}" : {self.times[x]},'.replace("'",'"')
        f = f[0:len(f)-1]
        f += '\n\t\t\t}\n\t\t],\n'
        return f
    

lc = Team("./lc.json",'j')

print(lc)

