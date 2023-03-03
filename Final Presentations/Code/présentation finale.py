import os
import pandas as pd
from datetime import timedelta, datetime
from matplotlib.pyplot import plot
import regex as re
import requests
from bs4 import BeautifulSoup
from lxml import etree
os.chdir("..")
os.chdir("..")
os.chdir("./Desktop/projet final")
file = pd.read_csv("projetb.csv", encoding="utf8")
file = file.fillna("")
file["dateparution"] = pd.to_datetime(file["dateparution"], format = "%Y-%m-%d")
file["datefindiffusion"] = pd.to_datetime(file["datefindiffusion"], format = "%Y-%m-%d", errors="coerce")
file["difference"] = file["datefindiffusion"].sub((file["dateparution"]), axis=0)
suspect = file["difference"]
Suspect = file[suspect < timedelta(days=10)]
Suspect.to_excel("/Users/timothegendre/Desktop/projet final/nouveaufichierprojet.xlsx", index=False)
len(Suspect)
Suspect.nomacheteur.value_counts()
occurence = []
for x, count in Suspect.nomacheteur.value_counts().items():
    if count > 20:
        occurence.append(x)
#Dans occurence, nous la liste de tous les acheteurs dont le nom apparait plus de 20 fois dans le fichier suspect
#Ceci signifie que notre premier objectif est atteint


#Affichons le type de marchés suspects
Suspect.descripteur_libelle.value_counts()[:10].plot.pie()
Suspect.descripteur_code.value_counts()[:10].plot.pie()

#nous allons ensuite créer un dataframe de tous les marchés d'AMO
df = pd.DataFrame(columns= Suspect.columns)
for index, row in Suspect.iterrows():
    if re.search("AMO", row["objet"]):
        df = df.append(row)
df.to_excel("/Users/timothegendre/Desktop/projet final/df.xlsx", index=False)

#Travail sur les marchés d'AMO avec la base DECP qui est plus précise grâce aux codes CPV
os.chdir("/Users/timothegendre/Desktop/projet final/Fichierxml")
files = os.listdir(".")
xml_file = etree.parse(files[3])#vérifier le fichier à ouvrir
root = xml_file.getroot()
for paragraph in root.iter("objet"):
    if re.search("AMO", paragraph.text):
        print(paragraph.text)

#solution ChatGPT
data = []
for marche in root.findall("marche"):
    acheteur = marche.find("acheteur").findall("*")
    titulaire = marche.find("titulaires/titulaire")
    if titulaire is not None:
        row = {
            'id': marche.find('id').text if marche.find('id') is not None else "",
            'objet': marche.find('objet').text if marche.find('objet') is not None else "",
            'dateNotification': marche.find('dateNotification').text if marche.find('dateNotification') is not None else "",
            'datePublicationDonnees': marche.find('datePublicationDonnees').text if marche.find('datePublicationDonnees') is not None else "",
            'montant': marche.find('montant').text if marche.find('montant') is not None else "",
            'procedure': marche.find('procedure').text if marche.find('procedure') is not None else "",
            'acheteur_id': acheteur[0].text if acheteur and len(acheteur) > 0 and acheteur[0] is not None else "",
            'acheteur_nom': acheteur[1].text if acheteur and len(acheteur) > 1 and acheteur[1] is not None else "",
            'codeCPV': marche.find('codeCPV').text if marche.find('codeCPV') is not None else "",
            'titulaire_denominationSociale': titulaire.find('denominationSociale').text if titulaire.find('denominationSociale') is not None else "",
            'titulaire_id': titulaire.find('id').text if titulaire.find('id') is not None else "",
            'titulaire_typeIdentifiant': titulaire.find('typeIdentifiant').text if titulaire.find('typeIdentifiant') is not None else ""
        }
        data.append(row)
df = pd.DataFrame(data)

#Ceci nous permet de soulever un deuxième point d'alerte qui se trouve être les marchés passés juste en-dessous des seuils
df['montant'] = df['montant'].astype(float).astype(int)
for index, row in df.iterrows():
    if 210000 <= row['montant'] <= 215000:
        print(row)
df_filtre = df.query("montant >= 210000 and montant <= 215000")#Ce code affiche les marchés passés juste en-dessous du seuils de procédure formalisée


#Avec les codes CPV il est facile d'extraire de manière plus précise les marchés d'AMO
marche_amo = pd.DataFrame(columns = df.columns)
for index, row in df.iterrows():
    if re.search("71000000|79998000-6|79110000-8|79100000-5|79000000-4", row["codeCPV"]):
        marche_amo = pd.concat([marche_amo, row.to_frame().T]) #on met le résultat dans un DF


#scrapper la cour des comptes
webpage = requests.get("https://www.ccomptes.fr/fr/publications?f%5B0%5D=institution%3A152&items_per_page=10&region=/fr/crc-provence-alpes-cote-dazur&search=&taxonomy_term=all&page=1")
soup = BeautifulSoup(webpage.content)
doc_div = soup.find("div", class_="view view-search-publications view-id-search_publications view-display-id-page_4 js-view-dom-id-d84108f645e2ce570ef750828844861978d5d50310b710de271f47797a0600bd")
print(len([x for x in doc_div.descendants]))
for child in doc_div.findChildren("h2"):
    print(child)












