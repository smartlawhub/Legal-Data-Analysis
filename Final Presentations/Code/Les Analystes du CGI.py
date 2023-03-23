
#This is a Python code that scrapes data from the French legal website "www.legifrance.gouv.fr" and creates a DataFrame for further analysis. The code is divided into two main steps.

#In the first step, the code scrapes the "Code Général des Impôts" (CGI) and extracts information about each article. This information includes the article number, its version, the date it was created, and its text. The text of each article is then modified to replace instances of the word "articles" with "article" and to list all referenced articles explicitly. The code then creates a DataFrame with this information.

#In the second step, the code reads a CSV file that contains the versions of CGI articles in force for each year from 1979 to 2023. The code then counts the number of references to other articles in each version of each article and stores this information in a separate DataFrame. Finally, the code creates a graph that shows how the number of references to other articles has evolved over time.



        #Première étape - SCRAPPING : scrapper le CGI Première étape - SCRAPPING : scrapper le CGI 

In [?]: for code in CGI:
   ...:     driver.get("https://www.legifrance.gouv.fr/" + codes[code])
   ...:     soup = BeautifulSoup(driver.page_source)
   ...:     set_articles = soup.find_all("a", string=re.compile("^Article"))
   ...:     for article in set_articles:
   ...:         legiarti_match = re.search("LEGIARTI.*?#", article.get("href"))
   ...:         if legiarti_match:
   ...:             legiarti = legiarti_match.group()[:-1]
   ...:         else:
   ...:             continue
   ...:         driver.get("https://www.legifrance.gouv.fr/codes/article_lc/" + legiarti)
   ...:         time.sleep(1)
   ...:         driver.find_element(By.XPATH, ".//button[@data-articleid='" + legiarti + "']|.//bu
   ...: tton[@data-articlecid='" + legiarti + "']").click()
   ...:         time.sleep(2)
   ...:         article_num = driver.find_element(By.CLASS_NAME, "name-article").text
   ...:         version_urls = [x.get_attribute("href") for x in driver.find_elements(By.CLASS_NAM
   ...: E, "version")]
   ...:         count_version = len(version_urls)
   ...:         for version_url in [x for x in version_urls if x is not None]:
   ...:             driver.get(version_url)
   ...:             legiver = re.search("LEGIARTI.*?/", version_url).group()[:-1]
   ...:             time.sleep(1)
   ...:             driver.find_element(By.XPATH, ".//button[@data-articleid='" + legiver + "']|//
   ...: button[@data-num='" + article_num.split(" ")[-1] + "']").click()
   ...:             time.sleep(1)
   ...:             try:
   ...:                 origin = driver.find_element(By.CLASS_NAME, "date").text
   ...:             except:
   ...:                 origin = ""
   ...:             article_text = driver.find_elements(By.CLASS_NAME, "content")[2].text
   ...:             temp_list = [article_num, version_url.split("/")[-2], count_version, article_t
   ...: ext, origin]
   ...:             count_version -= 1
   ...:             data_scrapped.append(temp_list)
   ...: driver.close()

        #1.2. En cas d'erreur lors du scrapping, une fonction permet de modifier la variable set_articles pour faire reprendre le scrapping à un endroit voulu. 

In [?]: for i, article in enumerate(set_articles):
              if "1613 bis" in article.text:
                  set_articles = set_articles[i:]
                  breakIn [?]: for i, article in enumerate(set_articles):
              if "1613 bis" in article.text:
                  set_articles = set_articles[i:]
                  break 

In [?]: df = pd.DataFrame(data_scrapped, columns=["Art", "Date", "version", "Text", "Created"])In [?]: df = pd.DataFrame(data_scrapped, columns=["Art", "Date", "version", "Text", "Created"]) 

        #1.3. Pour compter le nombre de renvois présents dans chaque article, il convient de modifier le texte de chaque article de telle manière :

In [?]: def remplacer_articles(texte):
    ...:     texte = texte.replace('articles', 'article')
    ...: 
    ...:     # Remplacer "article X à Y" par une liste de numéros d'articles correspondante
    ...:     texte = re.sub(r'article (\d+) à (\d+)', lambda match: ' '.join([f'article {i}' for i
    ...:  in range(int(match.group(1)), int(match.group(2))+1)]), texte)
    ...: 
    ...:     # Remplacer "article X, Y et Z" par une liste de numéros d'articles correspondante
    ...:     texte = re.sub(r'article ((\d+)(, |\s+et\s+))+(\d+)', lambda match: ' '.join([f'artic
    ...: le {i}' for i in sorted([int(x) for x in re.findall(r'\d+', match.group(0))])]), texte)
    ...: 
    ...:     # Remplacer "articles X et Y" par "article X article Y"
    ...:     texte = re.sub(r'articles? (\d+(?: et \d+)+)', lambda match: ' '.join([f'article {i}'
    ...:  for i in re.findall(r'\d+', match.group(0))]), texte)
    ...: 
    ...:     return texte
    ...: 
                                                                                  
In [?]: df['Text'] = df['Text'].apply(remplacer_articles) #Ainsi, du texte sous la forme "les articles 4 à 7" seront modifiées pour indiquer "article 4 article 5 article 6 article 7". 

        #Deuxième étape - Première analyse : l'évolution du nombre de renvois depuis 1980, au fil du temps 

        #2.1 : fichiers contenant pour chaque année la version des articles du CGI en vigueur
                                                                                     

# Boucler sur chaque année de 1979 à 2023
for year_limit in range(1979, 2024):

    # Ouvrir le fichier CSV
    with open(filename, encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')

        # Création d’un dictionnaire pour stocker les articles
        articles = {}

        # Création d’un dictionnaire pour compter le nombre de renvois
        num_articles = {}

        # Boucler sur chaque ligne du fichier CSV
        for row in reader:
            # Extraction de l'année
            date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
            year = date_obj.year

            # Si l'année est avant ou égale à la limite définie
            if year <= year_limit:
                # Extraction du numéro de l'article et de sa version
                article = row['Art']
                version = int(row['version'])

                # Si l'article n'est pas déjà dans le dictionnaire ou si la version est plus récente
                if article not in articles or version > articles[article][1]:
                    # Ajouter l'article avec sa version
                    articles[article] = (row, version)

                    # Extraction du nombre de renvois pour cet article
                    num_articles[article] = int(row['Num_articles'])
                elif version == articles[article][1]:
                    # Si la version est identique, utiliser le nombre de renvois pour cet article
                    num_articles[article] = int(row['Num_articles'])

    # Création d’un nouveau fichier CSV avec les articles en vigueur pour l'année déterminée
    with open('articles_{}.csv'.format(year_limit), mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')

        # Écriture de l'en-tête
        writer.writerow(['Date', 'Art', 'version', 'Num_articles'])

        # Boucler sur chaque article enregistré dans le dictionnaire
        for article, (row, version) in articles.items():
            # Formater la date en AAAA-MM-JJ
            date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
            date_str = date_obj.strftime('%Y-%m-%d')

            # Écriture de la ligne correspondant à la version la plus récente de l'article
            writer.writerow([date_str, article, version, num_articles[article]])filename = "Datamodifiée.csv"


        #2.2. : somme des renvois pour chaque année et graphique

# Délimitation des années de début et de fin
annee_debut = 1979
annee_fin = 2023

# Initialisation du dictionnaire pour stocker les totaux par année
annee_total = {}

# Boucler à travers chaque année
for annee in range(annee_debut, annee_fin+1):
    # Définir le nom de fichier pour cette année
    nom_fichier = f"articles_{annee}.csv"
    # Vérifier si le fichier existe
    if os.path.isfile(nom_fichier):
        # Charger le fichier CSV dans un DataFrame Pandas
        df = pd.read_csv(nom_fichier)
        # Calculer la somme de la colonne "Num_articles" (nombre de renvois)
        total = df["Num_articles"].sum()
        # Stocker le total dans le dictionnaire
        annee_total[annee] = total

# Conversion du dictionnaire en DataFrame Pandas
df_total = pd.DataFrame.from_dict(annee_total, orient="index", columns=["Total"])
# Tri des données par année croissante
df_total = df_total.sort_index()

# Création d’un graphique avec Matplotlib (courbe rouge ; graphique 1)
plt.plot(df_total.index, df_total["Total"], color='r')
plt.xlabel("Année")
plt.ylabel("Nombre total de renvois")
plt.title("Les renvois à d’autres articles au sein du CGI au fil du temps")
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
plt.show()

#Graphique 2 (fonction polynomiale de degré 3): 

# Création d’une figure et d’un axe
fig, ax = plt.subplots()

# Ajout de la courbe avec une ligne plus épaisse et une couleur rouge
x = df_total.index
y = df_total["Total"]
f = np.polyfit(x, y, 3)
p = np.poly1d(f)
ax.plot(x, y, 'o', color="red", markersize=3)
ax.plot(x, p(x), '-', color="blue", linewidth=2)

# Ajout des cadrillages
ax.grid(True)

# Ajout des labels d'axes et du titre en gras
ax.set_xlabel("Année")
ax.set_ylabel("Nombre total de renvois")
ax.set_title("Les renvois à d’autres articles au sein du CGI au fil du temps", fontweight='bold')

# Ajout d’une bordure autour de la courbe pour la rendre plus en relief
for spine in ax.spines.values():
    spine.set_edgecolor('gray')
    spine.set_linewidth(1.5)
  
# Affichage du graphique
plt.show()

#2.3. : Autres analyses du dataset

#Analyse des 10 articles contenant le plus de renvois (1980 & 2023) :

# Lecture du fichier CSV
df = pd.read_csv('articles_2023.csv')

# Trier le dataframe par ordre décroissant de la colonne "Num_articles"
df_sorted = df.sort_values(by=['Num_articles'], ascending=False)

# Extraire les 10 premiers articles avec le chiffre le plus élevé
top_articles = df_sorted.head(10)

# Créer un graphique à partir des données extraites
plt.figure(figsize=(8,6))
plt.bar(top_articles['Art'], top_articles['Num_articles'])
plt.title('Top 10 des articles du CGI contenant le plus de renvois en 1980', fontsize=14, fontweight='bold')
plt.xlabel('Article', fontsize=12, fontweight='bold', color='black')
plt.ylabel('Nombre de renvois', fontsize=12, fontweight='bold', color='black')
plt.tick_params(axis='both', labelsize=12, width=2, color='black')
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.gca().spines['bottom'].set_linewidth(2)
plt.gca().spines['left'].set_linewidth(2)
plt.show()


#Analyse des 10 articles ayant subi le + de versions (en 2023) :

# Lecture du fichier CSV
df = pd.read_csv("articles_2023.csv")

# Groupement des articles par nom et calcul du nombre de versions
versions_count = df.groupby("Art")["version"].max().sort_values(ascending=False)[:10]

# Création d’un graphique en diagramme
colors = ["#ff5733", "#33a7ff"] # Alternance entre rouge et bleu vif
plt.bar(versions_count.index, versions_count.values, color=colors * 5)
plt.title("Les 10 articles ayant subi le plus de versions")
plt.xlabel("Nom de l'article")
plt.ylabel("Nombre de versions")
plt.show()

        #Troisième étape - Deuxième analyse : Prestige de chaque article et Network Analysis
                                                                                        

In [?]: df['Art'] = df['Art'].str.lower()
        df['Text'] = df['Text'].str.lower()

In [?]:# Tri du dataframe par article et version (en ordre décroissant) pour obtenir que les versions la plus récente (en vigueur)
    ...: df = df.sort_values(["Art", "version"], ascending=[True, False])
    ...: 
    ...: # Groupement par article et sélection de la première ligne (version la 
    ...: plus élevée)
    ...: df = df.groupby("Art").first().reset_index()                                                                                        
                                                                                           
In [?]:
    ...: # Créer un graphe vide
         G = nx.Graph()
    ...: # Ajouter chaque article comme un noeud du graphe
    ...: for article in df['Art']:
    ...:     G.add_node(article)
    ...: 
    ...: # Parcourir chaque article et ajouter les arêtes correspondantes
    ...: for index, row in df.iterrows():
    ...:     article = row['Art']
    ...:     text = row['Text']
    ...:     for mentioned_article in df['Art']:
    ...:         if mentioned_article != article and mentioned_article in text:
    ...:             G.add_edge(article, mentioned_article)
    ...: 
    ...: # Calculer la centralité de degré pour chaque noeud
    ...: degree_centrality = nx.degree_centrality(G)
    ...: 
    ...: # Trier les noeuds par ordre décroissant de centralité de degré
    ...: sorted_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], re
    ...: verse=True)
    ...: 
    ...: # Afficher les 10 articles les plus prestigieux
    ...: for article, degree in sorted_nodes[:10]:
    ...:     print(article, degree)
    ...: 
article 16 0.1579136690647482
article 15 0.1341726618705036
article 10 0.08273381294964029
article 8 0.08201438848920864
article 14 0.07194244604316546
article 39 0.06546762589928058
article 6 0.05611510791366907
article 158 0.055395683453237414
article 5 0.055395683453237414
article 108 0.052158273381294966
                                                                                          
In [?]:  import networkx as nx
    ...: import matplotlib.pyplot as plt
    ...: 
    ...: # Créer le graphique vide
    ...: G = nx.DiGraph()
    ...: 
    ...: # Ajouter les noeuds correspondants aux articles
    ...: for article in df['Art']:
    ...:     G.add_node(article)
    ...: 
    ...: # Ajouter les liens entre les articles
    ...: for i, row in df.iterrows():
    ...:     text = row['Text']
    ...:     art = row['Art']
    ...:     # Chercher les articles mentionnés dans le texte
    ...:     mentions = [s for s in df['Art'] if s != art and s in text.lower()]
    ...:     # Ajouter les liens
    ...:     for mention in mentions:
    ...:         G.add_edge(art, mention)
    ...: 
    ...: # Dessiner le graphe
    ...: plt.figure(figsize=(40,40))
    ...: pos = nx.random_layout(G, seed=42)
    ...: nx.draw_networkx(G, pos, node_size=3, node_color='lightblue', edge_color='#1f78b4', arrowsize=4,
    ...:                  font_size=2.5, font_weight='bold', with_labels=True, width = 0.05)
    ...: 
    ...: # Afficher le graphe avec un fond blanc
    ...: ax = plt.gca()
    ...: ax.set_facecolor('white')
    ...: 
    ...: plt.axis('off')
    ...: plt.savefig('graphN.png', dpi=300, bbox_inches ='tight')	

                                                                                           
