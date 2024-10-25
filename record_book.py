# https://www.swimcloud.com/team/10001012/times/?dont_group=false&event=1100&event_course=Y&gender=M&page=1&region&season_id=19&tag_id&team_id=10001012&year=2024
# 2016 100 free
# https://www.swimcloud.com/team/10001012/times/?dont_group=false&event=1100&event_course=Y&gender=M&page=1&region&season_id=20&tag_id&team_id=10001012&year=2024
# 2017 100 free

import requests
import time
records = {}
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

f = []
team_id = "9441"
for s in ["M","F"]:
    for e in ['150','1100','1200','1500','2100','3100','4100','5200','6200','6400','7200']:
        """
        Stroke is the first number(1: FR, 2: BK, 3: BR, 4: FL, 5: IM, 6: Free Relay, 7: Medley Relay)
        The next digits are the distance(50, 100, 200, 400, 500)       
        This is the system that HYTEK uses and is pretty standardized across swimming
        """
        bests = []
        for y in range(12,28):

            html = requests.get(f'https://www.swimcloud.com/times/iframe/?page=1&team={team_id}&orgcode=9&course=Y&hide_gender=0&hide_season=0&event={e}&season={y}&gender={s}').text
            if "Data is not available at this time" not in html:
                html = html.split("<tbody>")[1].split("</tbody>")[0]
                html = html.split("</tr>")[0]
                bests.append([html.split('<a ')[1].split('\n              \n            </a>')[0].split('">\n              ')[1],"https://www.swimcloud.com"+(html.split('<td class="u-text-semi u-text-end">')[1].split('">')[0].split('<a href=')[1])[1:],html.split('<td class="u-text-semi u-text-end">')[1].split('">')[1].split('</a>')[0],f"{s}{e}"])

        bests = sorted(bests,key=lambda x: string_to_time(x[2]))
        print(bests[0])
        f.append(bests[0])

open(f"{f[8][0]}.txt","w").write(str(f).replace("],","],\n"))