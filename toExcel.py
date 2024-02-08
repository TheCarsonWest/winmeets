from openpyxl import load_workbook
import os
from data import *

files = []
importer = [["Name","Event","Time","Qualification","Meet","Date","Fixed Time","Sex","RQAL",'team']]
hs_events = ["50 Y Free","100 Y Free","200 Y Free","500 Y Free","100 Y Back","100 Y Breast","100 Y Fly","200 Y IM"]

names_list_m = []
names_list_f = []

teams_list = []

directory = './3a'
csv_filename = '3a'


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        files.append(f)
l = 0
for j in files:
    t = Team(j,'j')
    teams_list.append(t.name)
    for x in t.team_m:
        names_list_m.append([x.name,t.name])

        for e in hs_events:
            if e in x.times:

                importer.append([x.name,e,x.times[e][1],"","","",x.times[e][0],True,"",t.name])
                l += 1
    for x in t.team_f:
        names_list_f.append([x.name,t.name])
        for e in hs_events:
            if e in x.times:
                importer.append([x.name,e,x.times[e][1],"","","",x.times[e][0],False,"",t.name])
                l += 1

print(importer[1])



# This is copied from a previous version

  # Read the CSV file
  
template_file = './template.xlsx'  # Replace with your template Excel file name
  
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
points = template_wb['POINTS']
i = 2
for n in names_list_m:
    sheet_m[f"A{i}"] = n[0]
    sheet_m[f"B{i}"] = n[1]
    i+=1
i = 2
for n in names_list_f:
    sheet_f[f"A{i}"] = n[0]
    sheet_f[f"B{i}"] = n[1]
    i+=1
i = 2
for t in teams_list:
    points[f'A{i}'] = t
    i+=1

print('names put in the sheet')
template_wb.save(csv_filename+'.xlsx')
print(f"Workbook Saved as {csv_filename}.xlsx")