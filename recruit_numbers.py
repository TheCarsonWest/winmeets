import requests

import csv
teams = ['https://www.swimcloud.com/team/376/',
'https://www.swimcloud.com/team/258/',
'https://www.swimcloud.com/team/14',
'https://www.swimcloud.com/team/280/',
'https://www.swimcloud.com/team/416/',
'https://www.swimcloud.com/team/17/',
'https://www.swimcloud.com/team/283/',
'https://www.swimcloud.com/team/259/'
'https://www.swimcloud.com/team/401/',
'https://www.swimcloud.com/team/393/',
'https://www.swimcloud.com/team/89/',
'https://www.swimcloud.com/team/34/',
'https://www.swimcloud.com/team/134/',
'https://www.swimcloud.com/team/272/',
'https://www.swimcloud.com/team/477/',
'https://www.swimcloud.com/team/33/',
'https://www.swimcloud.com/team/60/',
'https://www.swimcloud.com/team/73/',
'https://www.swimcloud.com/team/123/']


ids = []
for t in teams:
    ids.append(t.split('https://www.swimcloud.com/team/')[1].split('/')[0])
years = ["2022","2023","2024","2025"]

f = []
for t in ids:
    r = [requests.get('https://www.swimcloud.com/team/'+t+"/roster/?page=1&gender=M&season_id=27&sort=perf").text.split('<meta property="og:title" content="')[1].split('"')[0]]

    for y in years:
        html = requests.get(f'https://www.swimcloud.com/recruiting/commitments/?team_id={t}&gradhs={y}&gender=M').text
        cards = html.split('<article class="c-commit">')[1:]
        for card in cards:
            untrimmed = card.split(f'<p class="c-list-bar__subheader" title="{y} rank">')[1].split('<p class="c-list-bar__description">')[1].split("</p>")[0]
            if untrimmed == "1000th+":  
                r.append(1000)
            else:
                r.append(int(untrimmed[0:len(untrimmed)-2]))
    print(r)
    f.append(r)
    
csv_file_path = "output.csv"


with open(csv_file_path, 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write each row of 'f' to the CSV file
    for row in f:
        csv_writer.writerow(row)