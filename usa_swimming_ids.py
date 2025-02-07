import requests

teams = []


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

for page in range(1,97):
    link = 'https://www.swimcloud.com/times/iframe/?page=1&region=state_nc&orgcode=9&course=Y&hide_gender=0&hide_season=0&event=150&season=28&gender=M'
    page = requests.get(link,headers=headers).text
    with open("html.txt",'w') as f:
        f.write(page)
    print(link)
    print(page)
    table = page.split('<table')[1].split("</table>")[0]
    rows = table.split("</td>")
    for x in rows:
        teams.append(x)
    with open("teams.txt",'w') as file:
        file.write(str(teams))
    break