from data import *

urls = [
'https://www.swimcloud.com/team/9442/',  # Lincoln charter used as a control because their team is small and runs quickly
'https://www.swimcloud.com/team/10026271/', #west cabarus
'https://www.swimcloud.com/team/4444/', #lnhs
'https://www.swimcloud.com/team/10001012/', # hough
'https://www.swimcloud.com/team/4391/', #hickory ridge
'https://www.swimcloud.com/team/10001011/',  # cox mill
'https://www.swimcloud.com/team/4342/',
'https://www.swimcloud.com/team/4334/',
'https://www.swimcloud.com/team/4512/',
'https://www.swimcloud.com/team/4329/', #ak
'https://www.swimcloud.com/team/4341/', #breaks program??? someone has a double profile(providence)
'https://www.swimcloud.com/team/4338/',
'https://www.swimcloud.com/team/10009151/',
'https://www.swimcloud.com/team/10001017/',
'https://www.swimcloud.com/team/4468/',
'https://www.swimcloud.com/team/7492/',
'https://www.swimcloud.com/team/4473/',
'https://www.swimcloud.com/team/4517/',
'https://www.swimcloud.com/team/4470/',
'https://www.swimcloud.com/team/4518/',
'https://www.swimcloud.com/team/4472/',
'https://www.swimcloud.com/team/4469/',
'https://www.swimcloud.com/team/10024716/',
'https://www.swimcloud.com/team/10009150/',
'https://www.swimcloud.com/team/4463/',
'https://www.swimcloud.com/team/4387/',
'https://www.swimcloud.com/team/4324/',
'https://www.swimcloud.com/team/4327/',
'https://www.swimcloud.com/team/7495/']


for x in urls:
    t = Team(x)
    t.save()
