import requests

for s in ["F"]: 
    for y in ['2027','2024']: 
        table = []
        for p in range(1,41): # ranks 1-1000
            html = requests.get(f'https://www.swimcloud.com/recruiting/rankings/{y}/{s}/?page={str(p)}').text
            html = html.split('<tbody>')[1].split('</tbody>')[0]

            for x in html.split('</tr>'):
                if '</td>' in x:
                    row = []
                    row.append(x.split('<a class="u-text-semi" href="/swimmer/')[1].split("</a>")[0].split('">')[1])
                    row.append(x.split('<td class="c-table-clean__col-fit u-pr0 u-text-center">\n            ')[1].split("\n")[0])
                    row.append(x.split('<td class="u-text-end">')[1].split("</td")[0])

                    table.append(row)
        file = open(f"./powers/{s}{y}.txt",'w')
        file.write(str(table))
     