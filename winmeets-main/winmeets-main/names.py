# I am going ot use this to turn a bunch of names into a bunch of swimcloud links and then into a bunch of power indexes

import requests


names = ['Alyssa Albertyn','Dillon Albertyn','Lillian Allison','Santiago Alzate','Adriana Amaral','Rilex Anderson','Samantha Anderson','Beck Armstrong','Tuck Bailey','Ryan Barker','Luand Barnard','Zetta Bartee','Hayden Beckley','Charlie Begin','Emma Belk','Richard Bell','Emma Bibza','Brody Blatt','Alyse Block','Mena Boardman','Carter Bradley','Bennett Brady','Catie Brenneman','Molly Brielle','Dilj Brig','Benjamin Brock','John Brostowitz','Gavin Buckley','Emerson Callis','Lilly Caples','Addi Carlile','Nathan Carr','Scott Center','Brody Chandler','Jackson Chiappetta','Maxine Clark','Claire Conklin','Asher Cooper','Rowan Cox','Charlotte Crush','Jack Culberson','Scott Custer','Sara Czrijak','Eduard Daniel','James Darcy','Micah Davis','Oliver Daw','Roman Dawson','Walters Dawson','Ava Deanda','Jackson DeBruin','Macey DeGroot','Ian Disosway','Roger Downey','Owen Durham','Jack Eaddy','Victoria Edgar','Elizabeth Eichbrecht','Owen Eisenhofer','Shayna Elgart','Alyce Elizabeth','Brody Engelstad','Madison Ensing','Andrew Eubanks','Matthew Ferguson','Velizar Filipov','Carson Fish','Lucy Flynn','Sophie Fredericks','Tristan Furlow','Michael Geh','Evan Gluck','Jared Goldstein','Eric Gong','Ava Grazziani','Christopher Gregg','Aiden Grigsby','Jack Grimley','George Groves','Peyton Guo','Brandon Ha','Averie Hager','Jaylee Hager','Aiden Hammer','Kayla Han','Gunnar Hansen','Karrington Hansen','Peyton Harrison','Sam Hennenfent','Maya Hetland','Jay Hickman','Jack Higgins','Audrey Hill','Blake Hill','Lincoln Hoffmann','Hudson Huberg','Lucas Huckabay','Grace Hunt','Adam Huynh','Seth Hyde','Burak Iloglu','Zoie Jare','Taylor Johannsen','Ashton Joswiak','Lucas Jue','Sarah Juiris','Madeleine Kana','Alek Karsic','Gracyn Kehoe','Jolynn Kellis','Iris Kim','Abby King','Oliver Kiss','Taylor Klein','Kaitlyn Kolessar','Mason Kring','Jain Krish','Madis Kryger','Jack Kulp','Zack Kusch','Frosty Kuzm','Nicholas Kwan','Heidi Lange','William Lathrop','Trae Lewis','Grant Lilly','Ryan Liu','Alex Lou','Enzo Lucas','Morin Lucas','Lu Luckna','Jenniffer Lyness','Parker Macho','Curtis Malone','Samuel Marsteiner','Cannon Martenson','Petra Martin','Maddox Matyas','Elena Maximenko','Tristan McCain','Macie McCarter','Libbi McCarthy','Ryan McDonald','Kenneth McGlothen','Zachary McNabb','Ella McWhorter','Alexis Mesina','Ava Metzger','Tammy Montgomery','Vivian Moulson','Paul Mullen','William Murphy','Chandler Neill','Nick Nukee','Julia Ogren','Les Olsson','Ty Ortiz','Sophie Papham','Alex Parent','David Pawlaski','Dayri Pena','Sophia Pero','Tyler Phillips','Noris Pineiro','Adam Polzien','Brian Qian','Ryan Quinn','Mattaus Rammel','Stanley Rayoka','Mike Rice','Kaleb Richmond','Frederick Rosenthal','Eva Rottink','Roos Rottink','Alyssa Sagle','Addison Sala','Natalie Schneider','Sydney Schoeck','Taylor Schwenk','Anton Semenyuk','Oliver Shao','Anna Shnowske','Harrison Short','Albert Smelzer','Liam Smith','Thavaryn Som','Kasey Sorensen','Oliver Stabach','Maxwell Stanislaus','Baylor Stanton','Tyler Stargardt','Tess Stavropoulos','Max Stewart','Sawyer Stolarczyk','Gideon Swan','Gman Teufel','Emma Thomas','Lanie Tietjen','Leah Tigert','Jeremy Ting','Roman Torres','Tommy Tuescher','Andrew Vanas','Matt Vatev','Elin Ville','Peter Vu','Adam Wang','Ava Ward','Joey Warnagiris','Clare Watson','Olivia Wenert','Carson West','Halle West','Avery Whorton','Lilla Wilbur','Chase Wilkerson','Gavin Willyerd','Dylan Winthal','Matthew Wolfle','Blake Wool','Molly Workman','Jackson Wroble','Alexandre Yazman','Chinju Yeh','Darmen Yess','Taewon Yim','Luqui Young','Yofang Yu','Cooper Zakorchemny','Kelsey Zhang','William Zhang','Kaideng Zhao','Katelynn Zhou','Michael Zhou','Nazar Zoukovski','Charles Zuhoski']




for i in range(len(names)):
    names[i] = names[i].replace(" ","+")

with open('./peen.txt',"w") as f:
    for name in names:
        try:
            m = requests.get('https://www.swimcloud.com/recruiting/rankings/2026/M/?name=' + name).text
            if "Data is not available at this time." not in m:
                t = m.split('    <tbody>')[1].split("    </tbody>")[0]
                a = []
                a.append(t.split(' <a class="u-text-semi" href="/swimmer')[1].split(">")[1].split('</a')[0])
                a.append(t.split(' <a class="u-text-semi" href="/swimmer/')[1].split('"')[0])
                a.append(t.split('hidden-xs u-color-mute">')[1].split('</td>')[0])
                a.append(t.split('class="u-text-end">')[1].split('</td>')[0])
                a.append(requests.get('https://www.swimcloud.com/swimmer/' + a[1]).text.split("2026 rank")[1].split("</li>")[0].split('target="_blank">\n')[1].split('</a>')[0].replace("\n",'').replace(' ',''))
                f.write(f"{a[0]},{a[1]},{a[2]},{a[3]},{a[4]}\n")
                print(f"{a[0]},{a[1]},{a[2]},{a[3]},{a[4]}")
        except Exception as e:
            print(f"Error processing {name}: {e}")
