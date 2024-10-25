from master import *


mens = ["https://www.swimcloud.com/swimmer/1715032/",
"https://www.swimcloud.com/swimmer/2297622/",
"https://www.swimcloud.com/swimmer/1748563/",
"https://www.swimcloud.com/swimmer/1714772/",
"https://www.swimcloud.com/swimmer/1768382/",
"https://www.swimcloud.com/swimmer/2074029/",
"https://www.swimcloud.com/swimmer/2828844/",
"https://www.swimcloud.com/swimmer/2418223/",
"https://www.swimcloud.com/swimmer/2074028/",
"https://www.swimcloud.com/swimmer/1860788/",
"https://www.swimcloud.com/swimmer/2074030/",
"https://www.swimcloud.com/swimmer/1347618/",
"https://www.swimcloud.com/swimmer/911875/",
"https://www.swimcloud.com/swimmer/2568123/",
"https://www.swimcloud.com/swimmer/2498308/",
"https://www.swimcloud.com/swimmer/1733787/",
"https://www.swimcloud.com/swimmer/2824512/",
"https://www.swimcloud.com/swimmer/2071713/",
"https://www.swimcloud.com/swimmer/2178326/",
"https://www.swimcloud.com/swimmer/778629/",
"https://www.swimcloud.com/swimmer/2421611/",
"https://www.swimcloud.com/swimmer/2203223/",
"https://www.swimcloud.com/swimmer/2485500/",
"https://www.swimcloud.com/swimmer/659494/",
"https://www.swimcloud.com/swimmer/2416879/",
"https://www.swimcloud.com/swimmer/2663475/",
"https://www.swimcloud.com/swimmer/2428577/",
"https://www.swimcloud.com/swimmer/2731807/",
"https://www.swimcloud.com/swimmer/1256600/",
"https://www.swimcloud.com/swimmer/2114641/",
"https://www.swimcloud.com/swimmer/2491034/",
"https://www.swimcloud.com/swimmer/2603790/",
"https://www.swimcloud.com/swimmer/1256363/",
"https://www.swimcloud.com/swimmer/2536391/",
"https://www.swimcloud.com/swimmer/778663/",
"https://www.swimcloud.com/swimmer/1256366/",
"https://www.swimcloud.com/swimmer/1808929/",
"https://www.swimcloud.com/swimmer/2204838/",
"https://www.swimcloud.com/swimmer/911716/"]

womens = ["https://www.swimcloud.com/swimmer/2182822/",
"https://www.swimcloud.com/swimmer/2576739/",
"https://www.swimcloud.com/swimmer/777522/",
"https://www.swimcloud.com/swimmer/2450496/",
"https://www.swimcloud.com/swimmer/1844038/",
"https://www.swimcloud.com/swimmer/1844304/",
"https://www.swimcloud.com/swimmer/2804956/",
"https://www.swimcloud.com/swimmer/2405921/",
"https://www.swimcloud.com/swimmer/778615/",
"https://www.swimcloud.com/swimmer/2434357/",
"https://www.swimcloud.com/swimmer/2584376/",
"https://www.swimcloud.com/swimmer/778559/",
"https://www.swimcloud.com/swimmer/1347658/",
"https://www.swimcloud.com/swimmer/1520239/",
"https://www.swimcloud.com/swimmer/2719368/",
"https://www.swimcloud.com/swimmer/2419454/",
"https://www.swimcloud.com/swimmer/2403739/",
"https://www.swimcloud.com/swimmer/911707/",
"https://www.swimcloud.com/swimmer/1124840/",
"https://www.swimcloud.com/swimmer/778589/",
"https://www.swimcloud.com/swimmer/683436/",
"https://www.swimcloud.com/swimmer/778626/",
"https://www.swimcloud.com/swimmer/2808155/",
"https://www.swimcloud.com/swimmer/1605267/",
"https://www.swimcloud.com/swimmer/1256347/",
"https://www.swimcloud.com/swimmer/1712469/",
"https://www.swimcloud.com/swimmer/779078/",
"https://www.swimcloud.com/swimmer/2585443/",
"https://www.swimcloud.com/swimmer/1256414/",
"https://www.swimcloud.com/swimmer/2042589/",
"https://www.swimcloud.com/swimmer/1212418/"]
senior_north = Team("b","l",False)
senior_north.name = "Senio"
for x in mens:
    senior_north.add(Swimmer(x),"m")
for x in womens:
    senior_north.add(Swimmer(x),"m")


senior_north.save()
senior_north.save_to_workbook("./templateClub.xlsx")

senior_north = Team("b","l",False)
senior_north.name = "carter"
senior_north.add(Swimmer("https://www.swimcloud.com/swimmer/2535048/"),'m')
senior_north.save_to_workbook("./templateClub.xlsx")