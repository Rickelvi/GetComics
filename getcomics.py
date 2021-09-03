import requests
from requests import get
from bs4 import BeautifulSoup

#Open the file with the list of ongoing comics
comics = open("comics.txt", "r")
cont = comics.readlines()

#Declare empty lists for read comics and new comics
new_titles = []
read_titles = []

for line in cont:
    #split the title in name and number of the comic
    #convert the number to an integer type
    #search the name of the comic in the site
    title = line.split(" #")
    num = str(title[1][0:2])
    title[1] = int(num)
    url = "https://getcomics.info/?s="+title[0]
    results = requests.get(url)

    #use bs4 shenanigans to parse the page
    soup = BeautifulSoup(results.text, "html.parser")
    comic_div = soup.find_all('div', class_="post-info")

    for container in comic_div:
        #find the name of the comic
        name = container.h1.a.text

        #find the year the comic was launched
        #new comics are launched the current year
        name_length = len(name)
        year_start = name_length-6
        year = name[year_start+1:name_length-1]
        name = name[:year_start-1]

        #not all comics have enumeration
        #for those that don't have, define it as 0
        if " #" in name:
            name = name.split(" #")
            if " " in name[1]:
                name[1] = name[1][0]
        else:
            name = [name, 0]

        #then convert the comics numeration to integer        
        name[1] = int(name[1])

        #print(name)

        #check if the comics are the same series
        #and if the comic has been read or a new edition was launched
        if name[0]==title[0] and name[1]>=title[1] and year=="2021":
            if name[1]==title[1]:
                read_titles.append(name)
            else:
                new_titles.append(name)

#Print the list of new comics and read comics
print("\tNew Comics\n")
if new_titles == []:
    print("None")
else:
    for nt in new_titles:
        print("{} #{}".format(nt[0], nt[1]))

print("\n\tRead Comics\n")
if read_titles == []:
    print("None")
else:
    for rt in read_titles:
        print("{} #{}".format(rt[0], rt[1]))

comics.close()
