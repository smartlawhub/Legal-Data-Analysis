# PARTIE 1 : Importation des différents packages nécessaires
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
from pathlib import Path

# PARTIE 2 : Extractation des décisions correpondant aux critères

# 2.1 : Extraction des décisions avec "Faillite personnelle"

# 2.1.1 : Accès au site de recherche de la Cour de cassation
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.courdecassation.fr/acces-rapide-judilibre") # Accès au site
time.sleep(2) # Attente pour chargement de la page

# 2.1.2 : Ecriture dans la barre de recherche
att_texte = "edit-search-api-fulltext" # Repérage de la barre de recherche
texte = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_texte + '"]')
texte.send_keys("Faillite personnelle") # Ecriture dans barre de recherche
rep_faill = "RepDecisions_FaillitePersonnelle/" # Nom du dossier où s'enregistreront la liste des décisions
rep = rep_faill

# 2.1.3 : Click dans la case "Expression exacte"
att_box = "edit-expression-exacte" # Repérage de la case
box = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_box + '"]')
box.click() # Click sur la case

# 2.1.4 : Click dans la case "Décisions de cours d'appel"
att_circle = "edit-judilibre-juridiction-ca"
circle = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_circle + '"]')
circle.click()

# 2.1.5 : Click dans la case "Rechercher"
att_rechercher = "edit-submit-judilibre"
rechercher = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_rechercher + '"]')
rechercher.click()

# 2.1.6 : Récupération de chaque décision sur toutes les pages
site_cass = "https://www.courdecassation.fr" # Enregistrement dans une variable du début de l'adresse du site
fin = False # Variable pour arrêter la boucle While lorsqu'il y a plus de page
while fin == False :
    print ("je consulte la page " + str(counter)) # Utile lors du débug pour voir la page consultée
    soup = BeautifulSoup(driver.page_source)
    # Repérage du lieu avec les informations qui seront contenues dans le nom du fichier
    decision_div = soup.find_all("div", class_="decision-item--header")
    # Nettoyage du nom du fichier
    for div in decision_div :
        h3_div = div.find_next(["h3"])
        t = h3_div.text
        t = t.replace("\n", "")
        t = t.replace("\t", "")
        t = t.replace("°", "_")
        t = t.replace("/", "_")
        t = t.replace("'", " ")
        fic = t + ".txt" # Nom du fichier

        # Vérification que le fichier n'existe pas déjà s'il y a deux lignes pour la même décision
        if os.path.isfile(rep + fic) :
            print("le fichier existe : " + fic)
        # Sinon récupération du texte de la décision
        else :
            a_div = div.find_next(["a"]) # Récupération du lien
            lien = a_div.get('href')
            webpage_decision = requests.get(site_cass + lien) # Accès à la page de la décision
            time.sleep(2) # Temps de chargement de la page
            tmp_file_name = rep + "tmp" # Création du fichier txt dans répertoire
            tmp_file = open(tmp_file_name, "w") # Ouverture du fichier
            tmp_file.write(webpage_decision.text) # Ecriture dans fichier du text de la décision
            tmp_file.close() # Fermeture du fichier
            os.rename(tmp_file_name, rep + fic) # Changement du nom du fichier

    list_url = soup.find_all("a") # Recherche de tous les liens dans la page
    page_suivante = ""
    for x in list_url:
        lien = x.get('href')
        # Recherche du lien permettant d'accéder à la page suivante
        if lien is not None:
            if lien.startswith("/recherche") :
                title = x.get('title')
                if title == "Aller à la page suivante":
                    page_suivante = lien
    if page_suivante != "": # Si existence du lien, accès à la page suivante
        driver.get(site_cass + page_suivante)
        time.sleep(1)
    else: # Si pas de lien pour page suivante, alors arrêt de la boucle While
        fin = True

# 2.2 : Extraction des décisions avec "Interdiction de gérer"

# 2.2.1 : Accès au site de recherche de la Cour de cassation
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.courdecassation.fr/acces-rapide-judilibre")
time.sleep(2)

# 2.2.2 : Ecriture dans la barre de recherche
att_texte = "edit-search-api-fulltext"
texte = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_texte + '"]')
texte.send_keys("Interdiction de gérer")
rep_inter = "RepDecisions_InterdictionDeGerer/"
rep = rep_inter

# 2.2.3 : Click dans la case "Expression exacte"
att_box = "edit-expression-exacte"
box = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_box + '"]')
box.click()

# 2.2.4 : Click dans la case "Décisions de cours d'appel"
att_circle = "edit-judilibre-juridiction-ca"
circle = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_circle + '"]')
circle.click()

# 2.2.5 : Click dans la case "Rechercher"
att_rechercher = "edit-submit-judilibre"
rechercher = driver.find_element(By.XPATH, r'.//*[@data-drupal-selector="' + att_rechercher + '"]')
rechercher.click()

# 2.2.6 : Récupération de chaque décision sur toutes les pages
site_cass = "https://www.courdecassation.fr"
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
            tmp_file_name = rep + "tmp"
            tmp_file = open(tmp_file_name, "w")
            tmp_file.write(webpage_decision.text)
            tmp_file.close()
            os.rename(tmp_file_name, rep + fic)
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
        time.sleep(1)
    else:
        fin = True

# PARTIE 3 : Analyse des fichiers

# 3.1 : Analyse des fichiers contenant "Faillite personnelle"
erreur = [] # Variable utile pour repérer les décisions ne comportant pas les mots recherchés
rep = rep_faill # Accès au bon dossier
list_of_lists = [] # Liste des listes permettant de former le Data Frame

# Ouverture de chaque fichier du dossier
for file in os.listdir(rep):
    if file.endswith(".txt"):
        fic = open(rep + file, "r")
        contenu = fic.read()
        fic.close()
        soup = BeautifulSoup(contenu, "html.parser") # Conversion du fichier txt en soup
        decision_div = soup.find("div", class_="decision-content decision-content--main")

        # Recherche du titre avec les infos voulues (Date, CA, Numéro)
        divs = decision_div.find_all_next(["h1"])
        if len(divs) > 1: # Vérification qu'il n'y a qu'un titre
            print("STOP car plus d'un H1 dans le fichier " + file + "(" + len(divs)+ ")")
            exit()
        for sib in decision_div.find_all_next(["h1"]):
            liste = str(sib).split("<br/>")

            # Nettoyage des informations
            for i in range(0, len(liste)):
                liste[i] = liste[i].replace("<h1>", "")
                liste[i] = liste[i].replace("\n", "")
                liste[i] = liste[i].replace("\t", "")
                liste[i] = liste[i].replace("</h1>", "")
                # Dans l'ordre liste : Date, CA, Numéro

        # Recherche du verdict du jugement
        jugement_div = soup.find_all("div", class_="decision-content decision-content--main")[-1]
        jugement = ""

        # Recherche de la position du "Par ces motifs" pour chercher le verdict aprèS
        # Synonyme de Par ces motifs : M O T I F et Statuant publique
        position_PCM = jugement_div.text.upper().find("PAR CES MOTIFS")
        if position_PCM == -1:
            position_PCM = jugement_div.text.upper().find("M O T I F")
            if position_PCM == -1 :
                position_PCM = jugement_div.text.upper().find("STATUANT PUBLIQUEMENT")

        # Vérification de l'existence d'un "Par ces motifs" dans la décision
        if position_PCM == -1:
            print("pas de PCM dans " + file)

        # Recherche de la position du verdict d'infirmer
        # Synonyme d'infirmer : infime, infirmons, annule, annulons, annulation, réformant, réforme, suspension,
        # suspend, arrêt de l'exécution, arrêtons l'exécution, arrêter l'exécution, nul et de nul effet le jugement,
        # nullité du jugement.
        position_infirme = jugement_div.text.upper().find("INFIRME",position_PCM)
        if position_infirme == -1:
            position_infirme = jugement_div.text.upper().find("INFIRMONS",position_PCM)
            if position_infirme == -1:
                position_infirme = jugement_div.text.upper().find("ANNULE",position_PCM)
                if position_infirme == -1 :
                    position_infirme = jugement_div.text.upper().find("ANNULONS",position_PCM)
                    if position_infirme == -1:
                        position_infirme = jugement_div.text.upper().find("ANNULATION", position_PCM)
                        if position_infirme == -1:
                            position_infirme = jugement_div.text.upper().find("REFORMANT",position_PCM)
                            if position_infirme == -1 :
                                position_infirme = jugement_div.text.upper().find("RÉFORMANT",position_PCM)
                                if position_infirme == -1:
                                    position_infirme = jugement_div.text.upper().find("REFORME",position_PCM)
                                    if position_infirme == -1:
                                        position_infirme = jugement_div.text.upper().find("RÉFORME",position_PCM)
                                        if position_infirme == -1:
                                            position_infirme = jugement_div.text.upper().find("SUSPENSION",position_PCM)
                                            if position_infirme == -1:
                                                position_infirme = jugement_div.text.upper().find("SUSPEND",position_PCM)
                                                if position_infirme == -1:
                                                    position_infirme = jugement_div.text.upper().find("ARRÊT DE L'EX",position_PCM)
                                                    if position_infirme == -1:
                                                        position_infirme = jugement_div.text.upper().find("ARRET DE L'EX",position_PCM)
                                                        if position_infirme == -1:
                                                            position_infirme = jugement_div.text.upper().find("ARRÊTONS L'EX", position_PCM)
                                                            if position_infirme == -1:
                                                                position_infirme = jugement_div.text.upper().find("ARRETONS L'EX", position_PCM)
                                                                if position_infirme == -1:
                                                                    position_infirme = jugement_div.text.upper().find("ARRÊTER L'EX", position_PCM)
                                                                    if position_infirme == -1:
                                                                        position_infirme = jugement_div.text.upper().find("ARRETER L'EX", position_PCM)
                                                                        if position_infirme == -1:
                                                                            position_infirme = jugement_div.text.upper().find("NUL ET DE NUL EFFET LE JUGEMENT",position_PCM)
                                                                            if position_infirme == -1:
                                                                                position_infirme = jugement_div.text.upper().find("NULLITE DU JUGEMENT",position_PCM)
                                                                                if position_infirme == -1:
                                                                                    position_infirme = jugement_div.text.upper().find("NULLITÉ DU JUGEMENT",position_PCM)

        # Recherche de la position du verdict de confirmer
        # Synonyme d'infirmer : confirme, confirmons, rejetons, rejette, erreur matérielle, déboute, déboutons,
        # écarte, écartons, rectification
        position_confirme = jugement_div.text.upper().find("CONFIRME",position_PCM)
        if position_confirme == -1:
            position_confirme = jugement_div.text.upper().find("CONFIRMONS",position_PCM)
            if position_confirme == -1:
                position_confirme = jugement_div.text.upper().find("REJETONS",position_PCM)
                if position_confirme == -1:
                    position_confirme = jugement_div.text.upper().find("REJETTE",position_PCM)
                    if position_confirme == -1:
                        position_confirme = jugement_div.text.upper().find("ERREUR MATÉRIELLE",position_PCM)
                        if position_confirme == -1 :
                            position_confirme = jugement_div.text.upper().find("DÉBOUTE",position_PCM)
                            if position_confirme == -1:
                                position_confirme = jugement_div.text.upper().find("DEBOUTE",position_PCM)
                                if position_confirme == -1:
                                    position_confirme = jugement_div.text.upper().find("DÉBOUTONS",position_PCM)
                                    if position_confirme == -1:
                                        position_confirme = jugement_div.text.upper().find("DEBOUTONS",position_PCM)
                                        if position_confirme == -1:
                                            position_confirme = jugement_div.text.upper().find("ÉCARTE",position_PCM)
                                            if position_confirme == -1:
                                                position_confirme = jugement_div.text.upper().find("ECARTE",position_PCM)
                                                if position_confirme == -1:
                                                    position_confirme = jugement_div.text.upper().find("ÉCARTONS",position_PCM)
                                                    if position_confirme == -1:
                                                        position_confirme = jugement_div.text.upper().find("ECARTONS",position_PCM)
                                                        if position_confirme == -1 :
                                                            position_confirme = jugement_div.text.upper().find("RECTIFICATION", position_PCM)

        # Recherche de la position de Irrecevable
        position_irrecevable = jugement_div.text.upper().find("IRRECEVABLE",position_PCM)

        # Recherche de la position de Sans objet
        # Synonyme de Sans objet : saisie d'aucun, désistement, radiation
        position_sansobjet = jugement_div.text.upper().find("SANS OBJET",position_PCM)
        if position_sansobjet == -1 :
            position_sansobjet = jugement_div.text.upper().find("SAISIE D'AUCUN", position_PCM)
            if position_sansobjet == -1:
                position_sansobjet = jugement_div.text.upper().find("DÉSISTEMENT", position_PCM)
                if position_sansobjet == -1:
                    position_sansobjet = jugement_div.text.upper().find("DESISTEMENT", position_PCM)
                    if position_sansobjet == -1:
                        position_sansobjet = jugement_div.text.upper().find("RADIATION", position_PCM)

        # Recherche de la position de Caduque
        # Synonyme de Caduque : caducité
        position_caduque = jugement_div.text.upper().find("CADUQUE",position_PCM)
        if position_caduque == -1:
            position_caduque = jugement_div.text.upper().find("CADUCITÉ", position_PCM)
            if position_caduque == -1:
                position_caduque = jugement_div.text.upper().find("CADUCITE", position_PCM)

        # Recher de la position de Reuverture des débats
        # Synonyme de Réouverture des débats : désistement d'appel
        position_reouverture = jugement_div.text.upper().find("OUVERTURE DES DÉBATS",position_PCM)
        if position_reouverture == -1 :
            position_reouverture = jugement_div.text.upper().find("OUVERTURE DES DEBATS",position_PCM)
        position_desistement = jugement_div.text.upper().find("DÉSISTEMENT D'APPEL",position_PCM)

        # Comparaison des positions
        if position_infirme == -1 : # Si pas d'infirmation
            if position_confirme == -1 : # Si pas de confirmation
                if position_irrecevable == -1 : # Si pas d'irrecevabilité
                    if position_sansobjet == -1 : # Si pas de sans objet
                        if position_reouverture == -1 : # Si pas de réouverture
                            if position_desistement == -1 : # Si pas de désistement
                                if position_caduque == -1 : # Si pas de caduque
                                    # Ajout du fichier à la liste d'erreur pour aller trouver le terme utilisé
                                    print("Pas de confirmation ni d'annulation ni d'irrecevable dans " + file)
                                    erreur.append(file)
                                else :
                                    jugement = "Caduque"
                            else :
                                jugement = "Désistement d'appel"
                        else :
                            jugement = "Réouverture des débats"
                    else :
                        jugement = "Sans objet"
                else :
                    jugement = "Irrecevable"
            else :
                jugement = "Confirmation totale"
        # Comparaison des positions d'infirmation et de confirmation
        # Si infirmation apparait avant confirmation alors infirmation partielle
        # Si c'est l'inverse, confirmation partielle
        else :
            if position_confirme == -1:
                jugement = "Infirmation totale"
            else :
                if position_confirme > position_infirme :
                    jugement = "Infirmation partielle"
                else :
                    jugement = "Confirmation partielle"
        # Il y a 9 verdicts possibles : Confirmation totale, Infirmation totale, Confirmation partielle,
        # Infirmation partielle, Caduque, Désistement d'appel, Réouverture des débats, Sans objet, Irrecevable

        liste.append(jugement) # ordre de la liste : Date, CA, Numéro, Verdict
        liste.append("1") # Rajout à la liste de l'information que cette décision vient du dossier Faillite personnelle
        liste.append("0") # Rajout de l'information que cette décision ne vient pas du dossier Interdiction de gérer
        liste.append(file) # Rajout du nom du fichier à la fin
        list_of_lists.append(liste) # Rajout de la liste à la liste de listes

# 3.2 : Analyse des fichiers contenant "Interdiction de gérer"
rep = rep_inter
if file.endswith(".txt"):

    # Vérification de la présence ou non de la décision dans le dossier Faillite personnelle
    for file in os.listdir(rep):
        if Path(rep_faill + file).is_file():
        # Si oui mettre 1 dans la colonne correspondante
            for list in list_of_lists:
                if list[-1] == file:
                    list[-2] = 1

        # Si non faire la même procédure que précédemment et extraction des informations de la décisions
        else :
            fic = open(rep + file, "r")
            contenu = fic.read()
            fic.close()
            soup = BeautifulSoup(contenu, "html.parser")
            decision_div = soup.find("div", class_="decision-content decision-content--main")
            divs = decision_div.find_all_next(["h1"])
            if len(divs) > 1:
                print("STOP car plus d'un H1 dans le fichier " + file + "(" + len(divs) + ")")
                exit()
            for sib in decision_div.find_all_next(["h1"]):
                liste = str(sib).split("<br/>")
                for i in range(0, len(liste)):
                    liste[i] = liste[i].replace("<h1>", "")
                    liste[i] = liste[i].replace("\n", "")
                    liste[i] = liste[i].replace("\t", "")
                    liste[i] = liste[i].replace("</h1>", "")
            jugement_div = soup.find_all("div", class_="decision-content decision-content--main")[-1]
            jugement = ""
            position_PCM = jugement_div.text.upper().find("PAR CES MOTIFS")
            if position_PCM == -1:
                position_PCM = jugement_div.text.upper().find("M O T I F")
                if position_PCM == -1:
                    position_PCM = jugement_div.text.upper().find("STATUANT PUBLIQUEMENT")
            if position_PCM == -1:
                print("pas de PCM dans " + file)
            position_infirme = jugement_div.text.upper().find("INFIRME", position_PCM)
            if position_infirme == -1:
                position_infirme = jugement_div.text.upper().find("INFIRMONS", position_PCM)
                if position_infirme == -1:
                    position_infirme = jugement_div.text.upper().find("ANNULE", position_PCM)
                    if position_infirme == -1:
                        position_infirme = jugement_div.text.upper().find("ANNULONS", position_PCM)
                        if position_infirme == -1:
                            position_infirme = jugement_div.text.upper().find("ANNULATION", position_PCM)
                            if position_infirme == -1:
                                position_infirme = jugement_div.text.upper().find("REFORMANT", position_PCM)
                                if position_infirme == -1:
                                    position_infirme = jugement_div.text.upper().find("RÉFORMANT", position_PCM)
                                    if position_infirme == -1:
                                        position_infirme = jugement_div.text.upper().find("REFORME", position_PCM)
                                        if position_infirme == -1:
                                            position_infirme = jugement_div.text.upper().find("RÉFORME", position_PCM)
                                            if position_infirme == -1:
                                                position_infirme = jugement_div.text.upper().find("SUSPENSION",
                                                                                                  position_PCM)
                                                if position_infirme == -1:
                                                    position_infirme = jugement_div.text.upper().find("SUSPEND",
                                                                                                      position_PCM)
                                                    if position_infirme == -1:
                                                        position_infirme = jugement_div.text.upper().find(
                                                            "ARRÊT DE L'EX", position_PCM)
                                                        if position_infirme == -1:
                                                            position_infirme = jugement_div.text.upper().find(
                                                                "ARRET DE L'EX", position_PCM)
                                                            if position_infirme == -1:
                                                                position_infirme = jugement_div.text.upper().find(
                                                                    "ARRÊTONS L'EX", position_PCM)
                                                                if position_infirme == -1:
                                                                    position_infirme = jugement_div.text.upper().find(
                                                                        "ARRETONS L'EX", position_PCM)
                                                                    if position_infirme == -1:
                                                                        position_infirme = jugement_div.text.upper().find(
                                                                            "ARRÊTER L'EX", position_PCM)
                                                                        if position_infirme == -1:
                                                                            position_infirme = jugement_div.text.upper().find(
                                                                                "ARRETER L'EX", position_PCM)
                                                                            if position_infirme == -1:
                                                                                position_infirme = jugement_div.text.upper().find(
                                                                                    "NUL ET DE NUL EFFET LE JUGEMENT",
                                                                                    position_PCM)
                                                                                if position_infirme == -1:
                                                                                    position_infirme = jugement_div.text.upper().find(
                                                                                        "NULLITE DU JUGEMENT",
                                                                                        position_PCM)
                                                                                    if position_infirme == -1:
                                                                                        position_infirme = jugement_div.text.upper().find(
                                                                                            "NULLITÉ DU JUGEMENT",
                                                                                            position_PCM)

            position_confirme = jugement_div.text.upper().find("CONFIRME", position_PCM)
            if position_confirme == -1:
                position_confirme = jugement_div.text.upper().find("CONFIRMONS", position_PCM)
                if position_confirme == -1:
                    position_confirme = jugement_div.text.upper().find("REJETONS", position_PCM)
                    if position_confirme == -1:
                        position_confirme = jugement_div.text.upper().find("REJETTE", position_PCM)
                        if position_confirme == -1:
                            position_confirme = jugement_div.text.upper().find("ERREUR MATÉRIELLE", position_PCM)
                            if position_confirme == -1:
                                position_confirme = jugement_div.text.upper().find("DÉBOUTE", position_PCM)
                                if position_confirme == -1:
                                    position_confirme = jugement_div.text.upper().find("DEBOUTE", position_PCM)
                                    if position_confirme == -1:
                                        position_confirme = jugement_div.text.upper().find("DÉBOUTONS", position_PCM)
                                        if position_confirme == -1:
                                            position_confirme = jugement_div.text.upper().find("DEBOUTONS",position_PCM)
                                            if position_confirme == -1:
                                                position_confirme = jugement_div.text.upper().find("ÉCARTE",position_PCM)
                                                if position_confirme == -1:
                                                    position_confirme = jugement_div.text.upper().find("ECARTE",position_PCM)
                                                    if position_confirme == -1:
                                                        position_confirme = jugement_div.text.upper().find("ÉCARTONS",position_PCM)
                                                        if position_confirme == -1:
                                                            position_confirme = jugement_div.text.upper().find("ECARTONS", position_PCM)
                                                            if position_confirme == -1:
                                                                position_confirme = jugement_div.text.upper().find("RECTIFICATION", position_PCM)
            position_irrecevable = jugement_div.text.upper().find("IRRECEVABLE", position_PCM)
            position_sansobjet = jugement_div.text.upper().find("SANS OBJET", position_PCM)
            if position_sansobjet == -1:
                position_sansobjet = jugement_div.text.upper().find("SAISIE D'AUCUN", position_PCM)
                if position_sansobjet == -1:
                    position_sansobjet = jugement_div.text.upper().find("DÉSISTEMENT", position_PCM)
                    if position_sansobjet == -1:
                        position_sansobjet = jugement_div.text.upper().find("DESISTEMENT", position_PCM)
                        if position_sansobjet == -1:
                            position_sansobjet = jugement_div.text.upper().find("RADIATION", position_PCM)
            position_caduque = jugement_div.text.upper().find("CADUQUE", position_PCM)
            if position_caduque == -1:
                position_caduque = jugement_div.text.upper().find("CADUCITÉ", position_PCM)
                if position_caduque == -1:
                    position_caduque = jugement_div.text.upper().find("CADUCITE", position_PCM)
            position_reouverture = jugement_div.text.upper().find("OUVERTURE DES DÉBATS", position_PCM)
            if position_reouverture == -1:
                position_reouverture = jugement_div.text.upper().find("OUVERTURE DES DEBATS", position_PCM)
            position_desistement = jugement_div.text.upper().find("DÉSISTEMENT D'APPEL", position_PCM)
            if position_infirme == -1:
                if position_confirme == -1:
                    if position_irrecevable == -1:
                        if position_sansobjet == -1:
                            if position_reouverture == -1:
                                if position_desistement == -1:
                                    if position_caduque == -1:
                                        print("Pas de confirmation ni d'annulation ni d'irrecevable dans " + file)
                                        erreur.append(file)
                                    else:
                                        jugement = "Caduque"
                                else:
                                    jugement = "Désistement d'appel"
                            else:
                                jugement = "Réouverture des débats"
                        else:
                            jugement = "Sans objet"
                    else:
                        jugement = "Irrecevable"
                else:
                    jugement = "Confirmation totale"
            else:
                if position_confirme == -1:
                    jugement = "Infirmation totale"
                else:
                    if position_confirme > position_infirme:
                        jugement = "Infirmation partielle"
                    else:
                        jugement = "Confirmation partielle"
            liste.append(jugement)
            liste.append("0") # Rajout de l'information que cette décision ne vient pas du dossier Faillite personnelle
            liste.append("1") # Rajout à la liste de l'information que cette décision vient du dossier Interdiction de gérer
            list_of_lists.append(liste)

# PARTIE 4 : Exportation dans un document Excel des données
df = pd.DataFrame(list_of_lists,columns=["Date","Ville de la Cour d'appel","Numéro","Verdict","Présence de \"faillite personnelle\"", "Présence de \"Interdiction de gérer\"", "Nom du fichier"])
df = df.drop(columns=['Nom du fichier']) # Suppression de la colonne nom du fichier
df.to_excel("Liste-DecisionsAvecInfos.xlsx") # Exportation dans un Excel

