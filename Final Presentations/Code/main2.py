import regex as re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys as KeysBrowser
import pandas as pd
import time
from matplotlib import pyplot as plt
import openpyxl

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.courdecassation.fr/acces-rapide-judilibre")
time.sleep(2)

#if driver.status_code != 201 :
 #   print("status code =" + driver.status_code)
  #  exit(-1)

# écriture dans barre de recherche
att_texte = "edit-search-api-fulltext"
texte = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_texte + '"]')
texte.send_keys("Faillite personnelle")

# click dans expression exacte
att_box = "edit-expression-exacte"
box = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_box + '"]')
box.click()

# click dans décisions cours d'appel
att_circle = "edit-judilibre-juridiction-ca"
circle = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_circle + '"]')
circle.click()

#click dans rechercher
time.sleep(1)
att_rechercher = "edit-submit-judilibre"
rechercher = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_rechercher + '"]')
rechercher.click()

#récupération des URL de chaque décision + URL page suivante
site_cass = "https://www.courdecassation.fr"
rep = "RepDecisions/"
fin = False
counter = 1
while fin == False :
    print ("je consulte la page " + str(counter))
    counter += 1
    soup = BeautifulSoup(driver.page_source)
    decision_div = soup.find_all("div", class_="decision-item--header")
    for div in decision_div :
        h3_div = div.find_next(["h3"])
        t = h3_div.text
        t = t.replace("\n", "")
        t = t.replace("\t", "")
        t = t.replace("°", "_")
        t = t.replace("/", "_")
        t = t.replace("'", " ")
        fic = t + ".txt"
        if os.path.isfile(rep + fic) :
            print("le fichier existe : " + fic)
        else :
            a_div = div.find_next(["a"])
            lien = a_div.get('href')
            webpage_decision = requests.get(site_cass + lien)
            time.sleep(2)
            file = open(rep + fic, "w")
            file.write(webpage_decision.text)
            file.close()
    list_url = soup.find_all("a")
    page_suivante = ""
    for x in list_url:
        lien = x.get('href')
        if lien is not None:
            if lien.startswith("/recherche") :
                title = x.get('title')
                if title == "Aller à la page suivante":
                    page_suivante = lien
    if page_suivante != "":
        driver.get(site_cass + page_suivante)
        time.sleep(2)
        if counter == 3:
            fin = True
    else:
        fin = True


##### FIN

### ANALYSE DES FICHIERS

#lecture boucle sur fichiers du répertoire
for file in os.listdir('RepDecisions')
    fic = open(rep + file, "r")
    contenu = fic.read()
    fic.close()
    soup = BeautifulSoup(contenu, "html.parser")
    decision_div = soup.find("div", class_="decision-content decision-content--main")
    divs = decision_div.find_all_next(["h1"])
    if len(divs) > 1:
        print("STOP")
        exit()
    for sib in decision_div.find_all_next(["h1"]):
        liste = str(sib).split("<br/>")
        for i in range(0, len(liste)):
            liste[i] = liste[i].replace("<h1>", "")
            liste[i] = liste[i].replace("\n", "")
            liste[i] = liste[i].replace("\t", "")
            liste[i] = liste[i].replace("</h1>", "")
    print(liste)
    jugement_div = soup.find_all("div", class_="decision-accordeon paragraph--type--texte-pliable")[-1]
    position_infirme = jugement_div.text.upper().find("ANNULE ")
    position_confirme = jugement_div.text.upper().find("CONFIRME ")
    if position_con
    print(position_infirme)
    print(position_confirme)









### Autre



    soup_decision = BeautifulSoup(webpage_decision.content)
    decision_div = soup_decision.find("div", class_="decision-content decision-content--main")





print("j'ai " + str(len(list_decision)) + " decisions")
df = pd.DataFrame(list_decision)
df.to_excel("Liste-URL-Decisions.xlsx", header = ["URL"])

file = open("RepDecisions/monfichier.txt", "w")
file.write("Voici le texte de mon fichier")
file.close()





















#ouverture de chaque décision et recherche d'infos
# infos à rechercher : numéro décision, date, ville de la CA, infirmer ou pas, sujet

Liste_URL_XLSX = pd.read_excel("Liste-URL-Decisions.xlsx")
for x in Liste_URL_XLSX["URL"]:
    webpage_decision = requests.get(x)
    time.sleep(2)
    soup_decision = BeautifulSoup(webpage_decision.content)
    decision_div = soup_decision.find("div", class_="decision-content decision-content--main")
    divs = decision_div.find_all_next(["h1"])
    if len(divs) > 1:
        print("STOP")
        exit()
    for sib in decision_div.find_all_next(["h1"]):
        liste = str(sib).split("<br/>")
        for i in range(0, len(liste)):
            liste[i] = liste[i].replace("<h1>","")
            liste[i] = liste[i].replace("\n","")
            liste[i] = liste[i].replace("\t","")
            liste[i] = liste[i].replace("</h1>","")




#if driver.status_code != 201 :
 #   print("status code =" + driver.status_code)
  #  exit(-1)


https://www.courdecassation.fr/decision/63f864cfc9488505de11ede2?search_api_fulltext=Faillite+personnelles&op=Rechercher+sur+judilibre&expression_exacte=1&date_du=&date_au=&judilibre_juridiction=ca&previousdecisionpage=&previousdecisionindex=&nextdecisionpage=0&nextdecisionindex=1



Titres_colonnes = ["", "URL", "Numéro de la décision", "Date", "Ville de la CA", "Sujet", "Confirmation ou Infirmation"]

