import regex as re # We need to upload all the packages necessary for the different functions of the algorith to work
import pandas as pd
import requests
from bs4 import BeautifulSoup

testQPC = [] # We create a list to collect the entire url
l = [] # We create a list to collect the changing part of the url
ll = [] # We create a list to correct the list of url
for x in range(-1, 64): # We create a loop to collect all the changing part of the url
    webpage = requests.get("https://www.conseil-constitutionnel.fr/les-decisions?items_per_page=100&page=0" + str(x)) # We get to the webpage in which all the QPC decisions are
    soup = BeautifulSoup(webpage.content, "html.parser") # We create a soup with the content of the webpage
    cconsti_div = soup.find("div", class_="view-content") # We create a variable to find all the changing parts of the url
    for link in cconsti_div.findAll('a'):
        l.append(link.get("href")) # We append the list with all the url
for ll in l:
    w = ll[-7:-4] # We search in the url to identify the QPC decisions, as all the url for the QPC decisions contains "QPC" in the url
    if w == 'QPC':
        testQPC.append(f"https://www.conseil-constitutionnel.fr" + str(ll)) # If the decision is a QPC decision, we append the url of the decision in a list

i=0 # We start a count to create a new row to collect the data for each decision
df=pd.DataFrame([],columns=["Numéro-décision","date","solution","visa"]) # We create a DataFrame to collect all the data, with four column: the number of the decision, the date, the solution and the visa
for url in testQPC: # We create a loop to extract information for each decision
    webpage = requests.get(url)
    try: # We use the try function to correct a small error on a decision without stopping the whole algorithm
        soup2 = BeautifulSoup(webpage.content, "html.parser") # We create a soup with the content of the webpage
        solution = soup2.find("div", class_="field field--name-field-solution-normalisee field--type-string field--label-hidden field__item").text  # We extract the solution for each decision
        date = soup2.find("span", class_="date").get_text()  # We extract the date for each decision
        date2 = date[4:] # We correct the data
        number_decision = soup2.find("h1", class_="title").get_text() # We extract the number of the decision for each decision
        date3 = date2[-4:] # We create a new variable which contains only the year for each date
        visa = [] # We create lists to collect the data related to the visa for each decision
        visa2 = []
        visa2correction = []
        if date3 > "2016": # The redaction of the visa for the QPC decisions changed from May 18, 2016. Therefore, the collection of the visa data changes. We use the following algorithm for all decisions rendered after 2016.
            soup3 = BeautifulSoup(webpage.content, "html.parser") # We create a soup with all the data from each webpage
            visa = soup3.find_all("div", class_="wrapper-content")[0].find_all("ul")[0].find_all("li") # We collect all the visas from the decision
        else:
            if date3 < "2016": # We use the following algorithm for all decision rendered before 2016 because of the change of the redaction
                soup22 = BeautifulSoup(webpage.content, "html.parser") # We create a soup with the content from the webpage
                visa2 = soup22.find("div", class_="clearfix text-formatted field field--name-field-contenu-original field--type-text-long field--label-hidden field__item").text  # We extract the whole part of the decision related to the visa
                visa2list = visa2.split("\n") # We split the part of the decision related to the visa at each line break to create a list with all the different texts in the visa
                for elt2 in visa2list: # We create this loop to clean the list of visa and the supress all elements which are not visa
                    if re.match("Vu", elt2): # We create this condition to delete from the list the part of the webpage we extracted which does not refer to visa
                        if re.match("Vu le règlement du 4 février 2010", elt2): # We stop the collection of the data after the last text referred in each visa to collect only the text in the visa
                            break
                        elif visa2correction.append(elt2): # Until the algorithm finds the "règlement du 4 février 2010" in the list, it appends to the visa2correction list all the visa
                            continue
                    else:
                        continue
                visa = visa2correction # We correct the name of the list containing all the visa to have the same list name that for the decisions rendered before 2016
            else: # We have to create a new algorithm to extract the visa of all the decision rendered in 2016, depending on the month
                if re.search("janvier|février|mars|avril|10", date2, re.I): # Thanks to this condition, we extract the data of all decisions rendered in january, february, march, april and the 10th of a month as the redaction of the visa changed staring from May 18th 2016. The only decisions rendered in May before the change of redaction were rendered on May 10th, 2016 and no other decision was rendered in 2016 the 10th of a month
                    soup22 = BeautifulSoup(webpage.content, "html.parser")
                    visa2 = soup22.find("div", class_="clearfix text-formatted field field--name-field-contenu-original field--type-text-long field--label-hidden field__item").text  # on récupère toute les balises paragraphe du div wrapper content, qu'on stock dans la variable temp (tableau de balise p)
                    visa2list = visa2.split("\n")
                    for elt2 in visa2list:
                        if re.match("Vu", elt2):
                            if re.match("Vu le règlement du 4 février 2010", elt2):
                                break
                            elif visa2correction.append(elt2):
                                continue
                        else:
                            continue
                    visa = visa2correction
                else:
                    soup3 = BeautifulSoup(webpage.content, "html.parser")
                    visa = soup3.find_all("div", class_="wrapper-content")[0].find_all("ul")[0].find_all("li")
        sublist = 4 * [""]  # We create a sublist to collect all the data we extracted from the decision for each decision
        sublist[0] = number_decision  # The first element of the sublist will be the number of the decision
        sublist[1] = date2  # The second element of the sublist will be the date of the decision
        sublist[2] = solution  # The third element of the sublist will be the solution of the decision
        sublist[3] = visa # The fourth element of the sublist will be the visa of the decision
        df.loc[i] = sublist # We add the four elements of the sublist on a new row created in the ith place
        i = i+1 # We add 1 to the count, so the elements of the next decision are added on a new row
    except: # This function allows the algorithm to keep working even thought there is a small difference in the redaction of a decision
        pass

df.to_csv('scrapping.csv') # This function copy the results of the DataFrame in a csv file

# Now that we have a Dataframe with all the information for each decision, we need to clean the data to create graphs

import os # We import the new packages we will use
import numpy as np
import pandas as pd
os.getcwd()  # We import the csv file in python
Out[15]: '/Users/robinsolene/PycharmProjects/Legal-Data-Analysis'
os.chdir("/Users/robinsolene/Documents/M2 droit des affaires et fiscalité/HEC/legal data analysis")
os.getcwd()
Out[5]: '/Users/robinsolene/Documents/M2 droit des affaires et fiscalité/HEC/legal data analysis'
df = pd.read_csv("scrapping.csv", header="infer", encoding="utf8")
import regex as re
for index, row in df.iterrows(): # We clean the "solution" column to create two types of solution: "conforme" or "non conforme"
    if re.search("non conformité", row["solution"], re.S | re.I):
        df.at[index, "résultat"] = "non conforme" # We start be the "non conforme" result to avoid that all solutions are considered as "conforme" since "non conforme" contains the word "conforme"
    elif re.search("conformité", row["solution"], re.S | re.I):
        df.at[index, "résultat"] = "conforme"
    else:
        df.at[index, "résultat"] = "non conforme" # All decisions whose result is neither "conforme" nor "non conforme" are considered as "non conforme"
print(df.résultat.value_counts(normalize=True) * 100)

# Now that we cleaned the data depending on whether the solution is a conformity or not to the Fench Constitution, we can create a graph to show the number of "conforme" or "non conforme" decisions

import locale
locale.setlocale(locale.LC_ALL, "fr_FR")
df["date2"] = pd.to_datetime(df["date"], format="%d %B %Y", errors="coerce") # Making the information in the "date" column understandable for python
df.groupby("date2").résultat.value_counts(normalize=True).unstack().plot()
df["date3"] = df["date"].str[-4:].astype(int)
df.groupby("date3").résultat.value_counts(normalize=True).unstack().plot()

# We clean the "solution" column to identify the decisions rendered with or without reservation

for index, row in df.iterrows():
    if re.search("réserve", row["solution"], re.S | re.I):
        df.at[index, "Réserve"] = "réserve"
    else:
        df.at[index, "Réserve"] = "pas de réserve"
print(df.Réserve.value_counts(normalize=True) * 100)
df.groupby("date3").Réserve.value_counts(normalize=True).unstack().plot()

L= [] # We create a new Dataframe with a different row for each visa
for index, row in df.iterrows():
    for x in re.split("</?li>", row["visa"]): # We split the visa part of the decision to identify each visa
        if len(x) >4:
            l = [row["Numéro-décision"], row ["date"], row["date3"], row["solution"], row["résultat"], row["Réserve"], x] # We create the new Dataframe with the number of the decision, the date, the solution, the result (conformity or not) and the reservation
            L.append(l)
newdf = pd.DataFrame(L, columns=["Numéro-décision", "date", "date3", "solution", "résultat", "Réserve", "visa"])
newdf.to_clipboard(index=False, encoding="utf8")
newdf.to_csv("scrapping clean")
newdf.to_csv("scrapping clean.csv") # We extract the new Dataframe
print(newdf.head(15))

# Now that we cleaned the data, we can create graphs and analyse the results

# Creation of a graph to show the codes most invoked in non-compliance decisions through time without reserve

import pandas as pd
import matplotlib.pyplot as plt
import locale
import regex as re

# specify the access to the document
path = "C:/Users/33781/Mes documents/Legal Data/DatasetCC.csv"

# Read CSV file in a DataFrame
df = pd.read_csv(path, header="infer", encoding="utf8")

# Synthetize data to obtain only one code name
df["Code"] = "" # Create blank column
for index, row in df.iterrows():
   sea = re.search("code [\w \']+", row["visa"]) # We search the codes among all the visas (the word "code" plus words after)
   if sea:
       df.at[index, "Code"] = sea.group()

#Obtain a list of codes most cited at least 20 times
count_codes = df.Code.value_counts().to_dict()
most_codes = []
for key in count_codes:
   if count_codes[key] > 20 and len(key) > 2:
       most_codes.append(key)

# select only decisions that cite a code as non-conformes, and avec réserve
df_nonconforme = df[(df['résultat'] == 'non conforme') & (df["Code"] != "") & (df["Réserve"] != "réserve") ]

# group year by year then for each group count the number of decisions
df_count = df_nonconforme.groupby([df_nonconforme['date3'], df_nonconforme['Code']]).size().reset_index(name='count')

# create a graph to compare codes invoked in non conforme decisions through time
for code in most_codes:
   df_code = df_count[df_count['Code'] == code]
   plt.plot(df_code['date3'], df_code['count'], label=code)

# add a legend and label axes
plt.legend()
plt.xlabel('Année')
plt.ylabel('Nombre de décisions non-conformes')

# show graph
plt.show()

# We create a graph to show the Codes most invoked in non-compliance decisions through time with reserve

import pandas as pd
import matplotlib.pyplot as plt
import locale
import regex as re

# specify access to CSV file
path = "C:/Users/33781/Mes documents/Legal Data/DatasetCC.csv"

# Read CSV file in a dataframe
df = pd.read_csv(path, header="infer", encoding="utf8")

# Synthetize data to obtain only one code name
df["Code"] = "" # Create blank column
for index, row in df.iterrows():
   sea = re.search("code [\w \']+", row["visa"])
   if sea:
       df.at[index, "Code"] = sea.group()

#Obtain a list of codes invoked at least 20 times
count_codes = df.Code.value_counts().to_dict()
most_codes = []
for key in count_codes:
   if count_codes[key] > 20 and len(key) > 2:
       most_codes.append(key)

# select only codes invoked as non conforme avec réserve
df_nonconforme = df[(df['résultat'] == 'non conforme') & (df["Code"] != "") & (df["Réserve"] != "pas de réserve") ]

# group year by year and by code then count number of decisions for each group
df_count = df_nonconforme.groupby([df_nonconforme['date3'], df_nonconforme['Code']]).size().reset_index(name='count')

# create a graph to compare non-compliant decisions through time
for code in most_codes:
   df_code = df_count[df_count['Code'] == code]
   plt.plot(df_code['date3'], df_code['count'], label=code)

# add legend and label axes
plt.legend()
plt.xlabel('Année')
plt.ylabel('Nombre de décisions non-conformes')

# whox graph
plt.show()

# We create a graph to show the number of non conformity decisions through time for the French code de procédure pénale

import pandas as pd
import matplotlib.pyplot as plt
import locale
import regex as re
path = "C:/Users/33781/Mes documents/Legal Data/DatasetCC.csv"
df = pd.read_csv(path, header="infer", encoding="utf8")
df["Code"] = ""
df_nonconforme = df[(df['visa'].str.contains("code de procédure pénale")) & (df['résultat'] == 'non conforme')]
df_count = df_nonconforme.groupby('date3').size().reset_index(name='count')
plt.plot(df_count['date3'], df_count['count'])
plt.legend()
plt.xlabel('Année')
plt.ylabel('Nombre de décisions non-conformes')
plt.show()

# We create a graph to show the number of non conformity decisions through time for the French code pénal

import pandas as pd
import matplotlib.pyplot as plt
import locale
import regex as re
path = "C:/Users/33781/Mes documents/Legal Data/DatasetCC.csv"
df = pd.read_csv(path, header="infer", encoding="utf8")
df["Code"] = ""
df_nonconforme = df[(df['visa'].str.contains("code pénal")) & (df['résultat'] == 'non conforme')]
df_count = df_nonconforme.groupby('date3').size().reset_index(name='count')
plt.plot(df_count['date3'], df_count['count'])
plt.legend()
plt.xlabel('Année')
plt.ylabel('Nombre de décisions non-conformes')
plt.show()

# We create a graph to show the number of non conformity decisions through time for the French code de la santé publique

import pandas as pd
import matplotlib.pyplot as plt
import locale
import regex as re
path = "C:/Users/33781/Mes documents/Legal Data/DatasetCC.csv"
df = pd.read_csv(path, header="infer", encoding="utf8")
df["Code"] = ""
df_nonconforme = df[(df['visa'].str.contains("code de la santé publique")) & (df['résultat'] == 'non conforme')]
df_count = df_nonconforme.groupby('date3').size().reset_index(name='count')
plt.plot(df_count['date3'], df_count['count'])
plt.legend()
plt.xlabel('Année')
plt.ylabel('Nombre de décisions non-conformes')
plt.show()