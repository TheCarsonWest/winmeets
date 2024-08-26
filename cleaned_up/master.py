import json
import requests
from openpyxl import load_workbook


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
    def __init__(self):
        self.team_m = []
        self.team_f = []
        self.url = "Blank"
        self.name = "Unnamed Team"
    # At some point make a wrapper for swimmingrank.com because their website is entremly lightweight
    def init_swimcloud(self,url):
            self.url = url # for safekeeping the future
            
            html_m = requests.get(url+"roster/?page=1&gender=M&season_id=27&sort=perf").text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n") # Cuts down the HTML page to just the roster
            html_f = requests.get(url+"roster/?page=1&gender=F&season_id=27&sort=perf").text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n")
            
            html_m.pop(0)
            html_f.pop(0)
            
            self.name = requests.get(url+"roster/?page=1&gender=M&season_id=27&sort=perf").text.split('<meta property="og:title" content="')[1].split('"')[0]
            
            self.team_m = []
            self.team_f = []
            for x in html_m:
                if 'href' not in x.split('            <td class="u-text-end">')[1]:
                    break
                self.team_m.append(Swimmer("https://www.swimcloud.com" + x.split("</td>")[1].split("href=\"")[1].split("\">")[0]))
                print(f"Added {self.team_m[-1].name}")

            for x in html_f:
                if 'href' not in x.split('            <td class="u-text-end">')[1]: ###
                    break
                self.team_f.append(Swimmer("https://www.swimcloud.com" + x.split("</td>")[1].split("href=\"")[1].split("\">")[0]))
                print(f"Added {self.team_f[-1].name}")

    def init_json(self,file):
            t = json.loads(open(file,"r").read())
            self.name = t[0][0]
            self.url = t[0][1]

            self.team_m = []
            self.team_f = []
            for x in t[1]:
                self.team_m.append(Swimmer(x,"l"))

            for x in t[2]:
                self.team_f.append(Swimmer(x,"l"))

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
        if gender:
            self.team_m.append(player)
        if not gender:
            self.team_f.append(player) 

    def remove(self,player): # removes player by name
        for t in [self.team_m,self.team_f]:
            for p in range(len(t)):
                if t[p].name == player:
                    print("removed "+ t.pop(p))

    def refresh(self,person = -1):
        if person == -1:
            self = Team(self.url)
        else:
            for t in [self.team_m,self.team_f]:
                for p in range(len(t)):
                    if t[p].name == person:
                        t[p] = Swimmer(t[p].url)


    def save_to_workbook(self, template_file = './templateClub.xlsx'):
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
        if u == "l": # Loads from list(what a json load will do)
            
            self.name = url[0]
            self.url = url[1]
            self.times = url[2]
        if u == "sr":
            html = requests.get(url).text
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