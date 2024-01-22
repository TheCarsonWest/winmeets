# Team file format reference


```py
team[0][0] = Team Name
team[0][1] = Url to teams Swimcloud

team[1] = Mens Team
team[2] = Womens Team

team[x][x] = Swimmer object

team[x][x][0][0] = Swimmer Name
team[x][x][0][1] = Url to Swimmers Swimcloud
team[x][x][1] = Dictionary of Swimmers times
team[x][x][1]["<event>"][0] = Day fraction of time
team[x][x][1]["<event>"][1] = Human usable time(MM:SS.00)
```