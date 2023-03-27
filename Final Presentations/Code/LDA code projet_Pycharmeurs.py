# Libraries

import re
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys as KeysBrowser

import matplotlib.pyplot as plt
import seaborn as sns

import locale
locale.setlocale(locale.LC_ALL, "fr_FR")


# We open a driver on the correct url
url = 'https://recherche.conseil-constitutionnel.fr/?mid=a35262a4dccb2f69a36693ec74e69d26&filtres[]=type_doc%3AversionHTML&filtres[]=sous_type_decision%3A%22DC-loi%22&filtres[]=sous_type_decision%3A%22DC-LO%22&offsetCooc=&offsetDisplay=10&nbResultDisplay=10&nbCoocDisplay=&UseCluster=&cluster=&showExtr=&sortBy=date&typeQuery=4&dateBefore=&dateAfter=&xtmc=&xtnp=p2&rech_ok=1&datepicker=&date-from=1993-04-01&date-to=2022-06-30'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
soup = BeautifulSoup(driver.page_source)
# To browse all pages, we first scrape the total number of decisions. The website shows 10 decisions/webpage, so we'll have to iterate

results = soup.find_all(string=re.compile('résultats$', re.IGNORECASE))
number = int(results[0].split()[0])
number_of_pages = number//10

decisions = [] 
for i in range(number_of_pages+1): # We iterate through all the pages
    # We open the correct url for the current page
    url = 'https://recherche.conseil-constitutionnel.fr/?mid=a35262a4dccb2f69a36693ec74e69d26&filtres[]=type_doc%3AversionHTML&filtres[]=sous_type_decision%3A%22DC-loi%22&filtres[]=sous_type_decision%3A%22DC-LO%22&offsetCooc=&offsetDisplay='+str(10*i)+'&nbResultDisplay=10&nbCoocDisplay=&UseCluster=&cluster=&showExtr=&sortBy=date&typeQuery=4&dateBefore=&dateAfter=&xtmc=&xtnp=p2&rech_ok=1&datepicker=&date-from=1993-04-01&date-to=2022-06-30'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    set_articles = soup.find_all("article", {"class": "type-decision"}) # We get a set of html div of class 'type_decision'
    for article in set_articles: # Iterate through these articles
        date = article.find_next('span',class_="date").text
        article_number = article.find_next('div',class_="title").text.split(' - ')[1] # The article number is in a div with class 'title'
        outcome = article.find_next('span',class_="type").text.replace('[','').replace(']','').split('-')[0].rstrip() # the outcome is in a span with class 'type'
        if(outcome in ['Conformité', 'Non conformité partielle', 'Non conformité totale']):
            decisions.append([date, article_number, outcome]) # We add our info into a list


decisions_df = pd.DataFrame(decisions, columns = ['Date', 'Numero', 'Outcome']) # Transform our list of lists into a dataframe
decisions_df["Date"] = pd.to_datetime(decisions_df["Date"], format="%d %B %Y", errors="coerce") # Convert the date from str to datetime
decisions_df.set_index('Date', inplace = True) # Set the date as index of the dataframe

# For our study, we will need to split decisions based on the mandat in which they occured. We add a column to simplify the next steps
mandat = []
for i in range(len(decisions_df)):
    date = decisions_df.index[i]
    if(date <= pd.to_datetime('1997-04-21', format = "%Y-%m-%d")):
        mandat.append(str(1))
    elif(date >= pd.to_datetime('1997-06-12', format = "%Y-%m-%d") and date <= pd.to_datetime('2002-06-18', format = "%Y-%m-%d")):
        mandat.append(str(2))
    elif(pd.to_datetime('2002-06-19', format = "%Y-%m-%d") and date <= pd.to_datetime('2007-06-19', format = "%Y-%m-%d")):
        mandat.append(str(3))
    elif(date >= pd.to_datetime('2007-06-20', format = "%Y-%m-%d") and date <= pd.to_datetime('2012-06-19', format = "%Y-%m-%d")):
        mandat.append(str(4))
    elif(date >= pd.to_datetime('2012-06-20', format = "%Y-%m-%d") and date <= pd.to_datetime('2017-06-20', format = "%Y-%m-%d")):
        mandat.append(str(5))
    else:
        mandat.append(str(6))
        
decisions_df['mandat'] = mandat


decisions_df.to_csv('decisions.csv') # Save the dataframe to a csv file

decisions_df['year'] = decisions_df.index.year # add a column 'year' to make our graphs

# First graph: a chart about the evolution of decisions through the years
plt.figure()
evolution_years = decisions_df.groupby('year').Outcome.value_counts().unstack().fillna(0)
evolution_years.plot().figure.savefig('Courbes_evolution.png')
plt.close()

# Second graph: an histogram about the repartition of decisions depending on the mandate
plt.figure()
decisions_by_mandat_hist = sns.histplot(data=decisions_df.reset_index(), x = 'mandat', hue = 'Outcome', multiple="dodge", shrink=.8)
fig = decisions_by_mandat_hist.get_figure()
fig.savefig('Histogramme.png')
plt.close()

# Third graph: a pie chart about the repartition of decisions for each mandate
decisions_by_mandat = decisions_df.groupby('mandat').Outcome.value_counts().unstack().fillna(0)
labels = decisions_by_mandat.columns
colors = sns.color_palette('pastel')[0:3]

# We iterate through all mandates
for i in range(1,7):
    plt.figure()
    print('Mandat '+str(i))
    plt.pie(decisions_by_mandat.loc[str(i)], labels = labels, colors = colors, autopct='%.0f%%')
    plt.title('Mandat '+str(i)) 
    plt.savefig('Camembert_mandat_'+str(i)+'.png')
    plt.close()

