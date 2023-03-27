import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 

lien = r"https://hudoc.echr.coe.int/fre#{%22sort%22:[%22respondentOrderFre%20Ascending%22],%22languageisocode%22:[%22FRE%22],%22respondent%22:[%22FRA%22],%22documentcollectionid2%22:[%22GRANDCHAMBER%22,%22CHAMBER%22],%22violation%22:[%222%22,%222-1%22,%223%22,%224%22,%224-1%22,%224-2%22,%225%22,%225-1%22,%225-1-c%22,%225-1-e%22,%225-1-f%22,%225-2%22,%225-3%22,%225-4%22,%225-5%22,%226%22,%226+6-3%22,%226+6-3-c%22,%226+13%22,%226-1%22,%226-1+6-3-a%22,%226-1+6-3-b%22,%226-1+6-3-c%22,%226-1+6-3-d%22,%226-2%22,%226-3%22,%226-3-a%22,%226-3-b%22,%226-3-c%22,%226-3-c+6-1%22,%226-3-d%22,%227%22,%227-1%22,%228%22,%228-1%22,%228-2%22,%229%22,%229-1%22,%2210%22,%2210-1%22,%2211%22,%2213%22,%2214%22]}"

driver = webdriver.Firefox()
driver.get(lien) #Ouvre un navigateur et va sur le lien

time.sleep(5)

# Trouve le lien du premier article et clique dessus

titreArticle = driver.find_element(By.CLASS_NAME, "lineone")
element = titreArticle.find_element(By.PARTIAL_LINK_TEXT, "AFFAIRE")
element.click()

# Clique sur le bouton pour voir l'affaire suivante
def suivant():
    boutonSuivant = driver.find_element(By.ID, "nextdocumentbutton")
    boutonSuivant.click()
    
# Lance la recherche des articles et des montants dans l'affaire
def recherche():
    corpsTexte = driver.find_element(By.TAG_NAME, "body")
    
    while "PAR CES MOTIFS" not in corpsTexte.text:
        corpsTexte = driver.find_element(By.TAG_NAME, "body")
        time.sleep(4)

    phrases = corpsTexte.text.split('\n')
    listeArticle = []
    totalMontant = 0
    debutRecherche = False

    for texte in phrases:
        if 'DE 742' in texte:
            print(texte)
            
        if "PAR CES MOTIFS" in texte :
            debutRecherche = True

        if "Fait en français" in texte :
            debutRecherche = False
            
        if not debutRecherche: continue 
    
        if "il y a eu violation de" in texte : 
            temp = texte.split("article")
            for i in temp:
                if "de la Convention" in i:
                    article = i.split("de la Convention")[0].strip()
                    print("Article detecté :", article)

                    if "§" in article:
                        article = article.split("§")[0].strip()
                  

                    listeArticle.append(article)

        if "EUR" in texte : 
            montants = texte.split("EUR")
            try:
                for i in montants[:-1]:
                    a = i.split()

                    indice = -1
                    stringMontant = ""
      
                    while a[indice].isdigit():
                        stringMontant = a[indice].strip() + stringMontant
      
                        indice -= 1
                    
                    montant = float(stringMontant.replace(',', '.'))
                    totalMontant += montant

                    print("Montant detecté :", montant)
            except :
                pass 
    
    listeArticle = list(set(listeArticle))
    print()
    print("Liste des articles recoltés :", *listeArticle)
    print("Somme des montants :", totalMontant)
    print()
    
    return listeArticle, totalMontant

articles = dict()
montants = dict()

for i in range(742):
    if (i+1) in [116, 533, 540, 572, 664, 697] : 
        time.sleep(5)
        suivant()
        continue

    listeArticle, montant = recherche()
    


    for article in listeArticle:
        if article in articles:
            articles[article] += 1
            montants[article] += montant
            
        else:
            articles[article] = 1
            montants[article] = montant

    if i != 741:
        suivant()
    time.sleep(2)


maxDecompte = 0
articleMax = ""


for article, decompte in articles.items():
    print("L'article", article, "a été enfreint", decompte, "fois pour un montant total de", round(montants[article], 2), "€.")

    if decompte > maxDecompte:
        maxDecompte = decompte
        articleMax = article

print()
print("L'article le plus enfreint est l'article", articleMax, "enfreint", maxDecompte, "fois pour un montant total de", round(montants[articleMax], 2), "€.")