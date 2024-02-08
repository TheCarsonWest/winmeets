from data import *

urls = ['https://www.swimcloud.com/team/9441/',
'https://www.swimcloud.com/team/4321/',
'https://www.swimcloud.com/team/4441/',
'https://www.swimcloud.com/team/4457/',
'https://www.swimcloud.com/team/7474/',
'https://www.swimcloud.com/team/4380/',
'https://www.swimcloud.com/team/4499/',
'https://www.swimcloud.com/team/4357/',
'https://www.swimcloud.com/team/4429/',
'https://www.swimcloud.com/team/10015143/',
'https://www.swimcloud.com/team/4446/',
'https://www.swimcloud.com/team/4360/']


for x in urls:
    t = Team(x)
    t.save()
