from openpyxl import load_workbook

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