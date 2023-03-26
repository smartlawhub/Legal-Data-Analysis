Importation des librairies utiles
In [ ]:
from selenium import webdriver
from selenium.webdriver.common.by import By
import concurrent.futures as cf
import pandas as pd
import json
import matplotlib.pyplot as plt
import requests
import re
N'ayant pas besoin d'intéragir avec les éléments de la page, le module requests aurait été suffisant et même plus efficace. Cependant le site du gouvernement est protégé par Incapsula contre le scraping, il est donc nécessaire d'utiliser Selenium qui utilise un vrai navigateur (mais qui est donc plus lent).
In [ ]:
def getDriver():
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    options.add_argument("--headless")
    return webdriver.Chrome(chrome_options=options, executable_path="C:\\Windows\\chromedriver.exe")
In [ ]:
base_url = "https://www.legifrance.gouv.fr/search/juri?tab_selection=juri&searchField=ALL&query=*&searchType=ALL&dateDecision=01%2F01%2F1946+%3E+01%2F01%2F2023&cassPubliBulletin=T&cassPubliBulletin=F&cassDecision=ARRET&cassFormation=ASSEMBLEE_PLENIERE&cassFormation=CHAMBRE_MIXTE&cassFormation=CHAMBRES_REUNIES&cassFormation=CHAMBRE_CIVILE_1&cassFormation=CHAMBRE_CIVILE_2&cassFormation=CHAMBRE_CIVILE_3&cassFormation=CHAMBRE_COMMERCIALE&cassFormation=CHAMBRE_SOCIALE&cassFormation=CHAMBRE_CRIMINELLE&cassFormation=COMMISSION_REEXAMEN&cassFormation=COMMISSION_REPARATION_DETENTION&cassFormation=COMMISSION_REVISION&cassFormation=COUR_REVISION&cassFormation=JURIDICTION_NATIONALE_LIBERTE_CONDITIONNELLE&cassFormation=ORDONNANCE_PREMIER_PRESIDENT&cassDecisionAttaquee=COMMISSION_INDEMNISATION_VICTIMES_INFRACTIONS&cassDecisionAttaquee=CONSEIL_PRUDHOMME&cassDecisionAttaquee=COUR_APPEL&cassDecisionAttaquee=COUR_ASSISES&cassDecisionAttaquee=COUR_CASSATION&cassDecisionAttaquee=COUR_JUSTICE_REPUBLIQUE&cassDecisionAttaquee=COUR_NATIONAL_INCAPACITE_TARIFICATION&cassDecisionAttaquee=TRIBUNAL_CORRECTIONNEL&cassDecisionAttaquee=TRIBUNAL_COMMERCE&cassDecisionAttaquee=TRIBUNAL_GRANDE_INSTANCE&cassDecisionAttaquee=TRIBUNAL_POLICE&cassDecisionAttaquee=TRIBUNAL_PREMIERE_INSTANCE&cassDecisionAttaquee=TRIBUNAL_AFFAIRES_SECURITE_SOCIALE&cassDecisionAttaquee=TRIBUNAL_FORCES_ARMEES&cassDecisionAttaquee=TRIBUNAL_INSTANCE&cassDecisionAttaquee=TRIBUNAL_CONTENTIEUX_INCAPACITE&cassDecisionAttaquee=TRIBUNAL_MARITIME_COMMERCIAL&cassDecisionAttaquee=TRIBUNAL_PARITAIRE_BAUX_RURAUX&cassDecisionAttaquee=TRIBUNAL_SUPERIEURS_APPEL&juridictionJudiciaire=Cour+de+cassation&typePagination=DEFAULT&sortValue=DATE_ASC&pageSize=100&page=1&tab_selection=juri#juri"
driver = getDriver()
driver.get(base_url)
Ce code permet de retrouver le nombre de pages qu'il va falloir parcourir :
nombre de pages
In [ ]:
nb_pages = int(
    driver.find_element(By.CLASS_NAME, "container-pager")\
          .find_elements(By.CLASS_NAME, "pager-item")[3]\
          .find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
)
Le but dans un premier temps est de parcourir ces 4691 pages de résultats pour récupérer les 100 liens par page
Fonction permettant de trouver l'année dans une phrase
In [ ]:
def extractYear(sentence):
    ys = [str(y) for y in range(1946, 2024)]
    for y in ys:
        if (sentence.find(y) > 0):
            return int(y)
Liste des pages à parcourir
In [ ]:
pages = [f"https://www.legifrance.gouv.fr/search/juri?tab_selection=juri&searchField=ALL&query=*&searchType=ALL&dateDecision=01%2F01%2F1946+%3E+01%2F01%2F2023&cassPubliBulletin=T&cassPubliBulletin=F&cassDecision=ARRET&cassFormation=ASSEMBLEE_PLENIERE&cassFormation=CHAMBRE_MIXTE&cassFormation=CHAMBRES_REUNIES&cassFormation=CHAMBRE_CIVILE_1&cassFormation=CHAMBRE_CIVILE_2&cassFormation=CHAMBRE_CIVILE_3&cassFormation=CHAMBRE_COMMERCIALE&cassFormation=CHAMBRE_SOCIALE&cassFormation=CHAMBRE_CRIMINELLE&cassFormation=COMMISSION_REEXAMEN&cassFormation=COMMISSION_REPARATION_DETENTION&cassFormation=COMMISSION_REVISION&cassFormation=COUR_REVISION&cassFormation=JURIDICTION_NATIONALE_LIBERTE_CONDITIONNELLE&cassFormation=ORDONNANCE_PREMIER_PRESIDENT&cassDecisionAttaquee=COMMISSION_INDEMNISATION_VICTIMES_INFRACTIONS&cassDecisionAttaquee=CONSEIL_PRUDHOMME&cassDecisionAttaquee=COUR_APPEL&cassDecisionAttaquee=COUR_ASSISES&cassDecisionAttaquee=COUR_CASSATION&cassDecisionAttaquee=COUR_JUSTICE_REPUBLIQUE&cassDecisionAttaquee=COUR_NATIONAL_INCAPACITE_TARIFICATION&cassDecisionAttaquee=TRIBUNAL_CORRECTIONNEL&cassDecisionAttaquee=TRIBUNAL_COMMERCE&cassDecisionAttaquee=TRIBUNAL_GRANDE_INSTANCE&cassDecisionAttaquee=TRIBUNAL_POLICE&cassDecisionAttaquee=TRIBUNAL_PREMIERE_INSTANCE&cassDecisionAttaquee=TRIBUNAL_AFFAIRES_SECURITE_SOCIALE&cassDecisionAttaquee=TRIBUNAL_FORCES_ARMEES&cassDecisionAttaquee=TRIBUNAL_INSTANCE&cassDecisionAttaquee=TRIBUNAL_CONTENTIEUX_INCAPACITE&cassDecisionAttaquee=TRIBUNAL_MARITIME_COMMERCIAL&cassDecisionAttaquee=TRIBUNAL_PARITAIRE_BAUX_RURAUX&cassDecisionAttaquee=TRIBUNAL_SUPERIEURS_APPEL&juridictionJudiciaire=Cour+de+cassation&typePagination=DEFAULT&sortValue=DATE_ASC&pageSize=100&page={i}&tab_selection=juri#juri" for i in range(1, nb_pages+1)]
Fonction qui scrap les informations utiles (lien et année), page par page
In [ ]:
def retrieve(url):
    to_add = []
    dr = getDriver()
    dr.get(url)
    articles = dr.find_elements(By.CLASS_NAME, "result-item")
    for article in articles:
        a = article.find_element(By.TAG_NAME, 'a')
        link = a.get_attribute("href")
        title = a.get_attribute("innerText")
        to_add.append((link, extractYear(title)))
    dr.quit()
    return to_add
Code qui récupére réelement les liens et années. 10 navigateurs sont lancés en paralèlle pour accélérer le processus. Les résultats sont finalement enregistrés dans un fichier json
In [ ]:
with cf.ThreadPoolExecutor(max_workers=10) as executor:
   futures = [executor.submit(retrieve, url) for url in pages]
   for future in cf.as_completed(futures):
      try:
         results = [future.result() for future in futures]
         with open("data.json", "w") as json_file:
            json.dump(results, json_file)
      except requests.ConnectTimeout:
         pass
Malheuresement, le site du gouvernement nous complique une fois de plus la tâche en nous autorisant l'accès aux 10 000 premiers résultats seulement.
affichage limite
Nos datas s'arrêtent donc à 1973. Pour palier à ça, nous pourrions affiner la fenêtre temporelle de la recherche année par année et répéter le processus ci-dessus
fenetre temporelle
Formatage des datas dans un DataFrame pandas
In [ ]:
with open("data.json", "r") as json_file:
    data = json.load(json_file)
data = [sub for sub in data if len(sub) > 0]
flat = []
for sub in data:
    for item in sub:
        flat.append(item)
df = pd.DataFrame(flat, columns=['url', 'year'])
On se limite à maximum 100 données par an
In [ ]:
to_concat = []
for y in set(df['year']):
    subdf = df[df['year'] == y]
    to_concat.append(subdf.sample(n = min(100, len(subdf)), random_state = 42))
normalized = pd.concat(to_concat, axis=0).reset_index(drop=True)
On va maintenant scraper les 688 liens des jugements que nous avons gardés pour en retirer les informations qui nous intéressent:
Date exacte
Sexe du président
Juridiction
In [ ]:
results = {'date': [], 'gender': [], 'juridiction': []}
Le multithreading aurait pu être utilisé ici aussi, mais le nombre d'itérations est suffisament faible pour s'en affranchir
In [ ]:
driver = getDriver()
patternF = r"Mme "
patternM = r"M\.|M "
patternDate = r"\b\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b"
for url in normalized['url']:
    driver.get(url)
    try:
        juridiction = driver.find_elements(By.CLASS_NAME, "horsAbstract")[0]\
                            .get_attribute("innerText")
        juridiction = juridiction[juridiction.find("- ")+2:]
    except Exception as e:
        juridiction = ''
        print("An error occurred:", str(e))
    try:
        pdt = driver.find_elements(By.CLASS_NAME, 'frame-block')[1]\
              .find_elements(By.TAG_NAME,'div')[0]\
              .find_elements(By.TAG_NAME, 'dd')[0]\
              .get_attribute("innerText")
        if re.findall(patternF, pdt, re.IGNORECASE):
            gender = 'F'
        elif re.findall(patternM, pdt, re.IGNORECASE):
            gender = 'M'
        else:
            gender = ''
    except Exception as e:
        gender = ''
        print("An error occurred:", str(e))
    try:
        date = driver.find_elements(By.CLASS_NAME, "horsAbstract")[1]\
                            .get_attribute("innerText")
        date = re.findall(patternDate, date, re.IGNORECASE)[0]
    except Exception as e:
        date = ''
        print("An error occurred:", str(e))
    results['date'].append(date)
    results['gender'].append(gender)
    results['juridiction'].append(juridiction)
Les résultats sont mis en forme dans un DataFrame puis sont sauvés dans un fichier csv
In [ ]:
results = pd.DataFrame(results)
results.to_csv("dataframe.csv", index=False)
Il n'y aurait qu'une femme qui a présidé entre 1946 et 1973 😅
In [48]:
results[results['gender'] == 'F']
Out[48]:
date	gender	juridiction
58	28 octobre 1957	F	Chambre sociale
On se rend compte qu'il y a beacoup de données manquantes
In [49]:
print(f"Nombre de jugements étudiés: {len(results)}\nNombre de jugements où le sexe du président est indiqué: {len(results[results['gender'] != ''])}")
Nombre de jugements étudiés: 689
Nombre de jugements où le sexe du président est indiqué: 571
On retire en suite les lignes vides
In [ ]:
clean = results[results['gender'] != '']
Puis on convertit les dates en datetime, de sorte à avoir des time series
In [ ]:
mois = {" janvier ": "/01/", " février ": "/02/", " mars ": "/03/", " avril ": "/04/", " mai ": "/05/", " juin ": "/06/", " juillet ": "/07/", " août ": "/08/", " septembre ": "/09/", " octobre ": "/10/", " novembre ": "/11/", " décembre ": "/12/"}
def convert(dt):
    for m in mois:
        if m in dt:
            return dt.replace(m, mois[m])
In [ ]:
clean.loc[:, 'date'] = clean['date'].apply(convert)
clean.loc[:, 'date'] = pd.to_datetime(clean['date'], format='%d/%m/%Y')
clean.set_index('date', inplace=True)
Enfin, on compte le nombre de femmes présidentes par année et on affiche le graphe des résultats
In [ ]:
serie = clean.groupby(clean.index.year)['gender'].sum()
serie = serie.apply(lambda val: val.count('F'))
In [50]:
serie.plot.bar()
plt.xlabel('Year')
plt.ylabel('# Women Presidents')
plt.title('Women presidents by year')
plt.show()
