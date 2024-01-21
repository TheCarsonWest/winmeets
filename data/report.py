

import requests
from openpyxl import load_workbook

hs_events = ["50 Y Free","100 Y Free","200 Y Free","500 Y Free","100 Y Back","100 Y Breast","100 Y Fly","200 Y IM"]

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


names_list_m = []
names_list_f = []

importer = [["Name","Event","Time","Qualification","Meet","Date","Fixed Time","Sex","RQAL"]]


url = input("Input team home page\n > ")


url_m = url+"roster/?page=1&gender=M&season_id=27&sort=perf"
url_f = url+"roster/?page=1&gender=F&season_id=27&sort=perf"



html = requests.get(url_m).text
csv_filename = html.split('<meta property="og:title" content="')[1].split('"')[0].replace(" ","_")
print(csv_filename)

html_m = html.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n") # gets html page of roster
html_m.pop(0) # the first raw has nothing in it, popped it


each_m = []


for x in html_m: # creates a list of swimcloud links for everyone with a point value
        if "&ndash;" in x.split("</td>")[4]: # if they havent scored points, ignore
            break
        each_m.append("https://www.swimcloud.com"+x.split("</td>")[1].split("href=\"")[1].split("\">")[0])
print(f"Found {len(each_m)} male swimmers")

# repeats the exact same steps but for the women's team

html_f = requests.get(url_f).text.split("<tbody>")[1].split("</tbody>")[0].split("<tr \n          >\n") # gets html page of roster
html_f.pop(0) # the first raw has nothing in it, popped it


each_f = []
f = 0
for x in html_f: # creates a list of swimcloud links for everyone with a point value
        if "&ndash;" in x.split("</td>")[4]: # if they havent scored points, ignore
            break
        each_f.append("https://www.swimcloud.com"+x.split("</td>")[1].split("href=\"")[1].split("\">")[0])
        f +=1
print(f"Found {f} female swimmers")        

l = 2

for x in each_m:
      
      s_html = requests.get(x).text.split("<body")[1].split('<span class="u-mr-">')[1] # Gets the HTML and cuts it down right to where we need stuff
      s_name = s_html.split('</span>')[0] # Their name, for importing

      #print(f"Found {s_name}'s Times")
      s_table = s_html.split("<tbody>")[2].split("</tbody>")[0].split("</tr>")
      s_table.pop(-1)
      print(f"Found {str(len(s_table))} events for {s_name}")
      names_list_m.append(s_name)


      for i in s_table: 
            r = [s_name]
            s_td = i.split("</td>") # we are going to ignore this variable name
            if s_td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0] in hs_events:
                if len(s_td)==6:

                        r.append(s_td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0])
                        r.append(s_td[1].split("</a>")[0].split('">')[2])
                        r.append("")
                        r.append(s_td[3].split("</a>")[0].split('">')[2])
                        r.append(s_td[4].split('<td class="u-text-truncate">')[1])
                else:        
                        r.append(s_td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0])
                        r.append(s_td[1].split("</a>")[0].split('">')[2])
                        r.append("")
                        r.append(s_td[2].split("</a>")[0].split('">')[2])
                        r.append(s_td[3].split('<td class="u-text-truncate">')[1])

                r.append(string_to_time(r[2]))
                r.append(True)
                r.append(f"=G{l}<HLOOKUP(B{l},Table7[#All],IF('Time Sheet'!H{l},3,2),FALSE)")

                importer.append(r)
                l+=1
# low tech solution
for x in each_f:
      
      s_html = requests.get(x).text.split("<body")[1].split('<span class="u-mr-">')[1] # Gets the HTML and cuts it down right to where we need stuff
      s_name = s_html.split('</span>')[0] # Their name, for importing

      #print(f"Found {s_name}'s Times")
      s_table = s_html.split("<tbody>")[2].split("</tbody>")[0].split("</tr>")
      s_table.pop(-1)
      print(f"Found {str(len(s_table))} events for {s_name}")
      names_list_f.append(s_name)


      for i in s_table: 
            r = [s_name]
            s_td = i.split("</td>") # we are going to ignore this variable name
            if s_td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0] in hs_events:
                if len(s_td)==6:

                        r.append(s_td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0])
                        r.append(s_td[1].split("</a>")[0].split('">')[2])
                        r.append("")
                        r.append(s_td[3].split("</a>")[0].split('">')[2])
                        r.append(s_td[4].split('<td class="u-text-truncate">')[1])
                else:        
                        r.append(s_td[0].split('<td class="u-text-truncate">')[1].split('class="js-event-link">')[1].split("</")[0])
                        r.append(s_td[1].split("</a>")[0].split('">')[2])
                        r.append("")
                        r.append(s_td[2].split("</a>")[0].split('">')[2])
                        r.append(s_td[3].split('<td class="u-text-truncate">')[1])

                r.append(string_to_time(r[2]))
                r.append(False)
                r.append(f"=G{l}<HLOOKUP(B{l},Table7[#All],IF('Time Sheet'!H{l},3,2),FALSE)")

                importer.append(r)
                l+=1



# Read the CSV file

template_file = 'template.xlsx'  # Replace with your template Excel file name

# Load the template Excel file
template_wb = load_workbook(template_file)

# Get the desired sheet from the template file to combine data
time_sheet = template_wb['Time Sheet']  # Assuming the sheet is named "Time Sheet"
# Write data to the template sheet
for row_data in importer:
    time_sheet.append(row_data)
print("Time Sheet Created)")

sheet_m = template_wb['Boys']
sheet_f = template_wb['Girls']
i = 2
for n in names_list_m:
     sheet_m[f"A{i}"] = n 
     i+=1
i = 2
for n in names_list_f:
     sheet_f[f"A{i}"] = n
     i+=1

print('names put in the sheet')
template_wb.save(csv_filename+'.xlsx')
print(f"Workbook Saved as {csv_filename}.xlsx")
        