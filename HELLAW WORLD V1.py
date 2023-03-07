import requests
from bs4 import BeautifulSoup
import regex as re

l = []
for x in range(1):
    webpage=requests.get("https://www.courdecassation.fr/recherche-judilibre?sort=date-desc&items_per_page=30&search_api_fulltext=&expression_exacte=&date_du=2022-09-15&date_au=&judilibre_chambre=&judilibre_type=&judilibre_publication=&judilibre_solution=&judilibre_juridiction=ca&judilibre_formation=&judilibre_zonage=&judilibre_doctype=&judilibre_siege_ca=ca_paris&judilibre_nature_du_contentieux=&judilibre_type_ca=arret&op=Trier&page=" + str(x))
    soup = BeautifulSoup(webpage.content)
    div = soup.find("div",class_="view-judilibre")
    aas = div.find_all("a")
    for a in aas:
        l.append(a.get("href"))

for el in l:
    lien = "https://www.courdecassation.fr"+el
    webpage = requests.get(lien)
    soup2 = BeautifulSoup(webpage.content)
    tableau = lien.split(" ")
    print(tableau)

for y in lien:#On a essayé d'aller chercher le dispositif avec re.search
    webpage = requests.get(lien)
    soup = BeautifulSoup(webpage.content)
    dispositif = re.search("Par ces motifs", soup, re.I)

    
 # Solution 
tableau = []
for el in l[:3]:
    sub = []
    sub.append(lien)
    lien = "https://www.courdecassation.fr"+el
    webpage = requests.get(lien)
    soup2 = BeautifulSoup(webpage.content)
    dispositif = re.search("Par ces motifs", soup2.getText(), re.I)
    art700 = re.search("article 700", soup2.getText()[dispositif.start():], re.I)
    sum = re.search("\d+\s?(\d+\s?)*euros", soup2.getText()[dispositif.start() + art700.start() - 50:])
    if sum:
        sub.append(sum.group())
    else:
        sub.append("Pas d'Article 700")
    tableau.append(sub)
