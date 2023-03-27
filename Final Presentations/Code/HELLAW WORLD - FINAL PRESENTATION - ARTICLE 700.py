# Laurine LE, Quentin DUPRE, Julien CARRENCE, Bertrand SABATHIER
# Comparaison des montants alloués au titre de l'article 700 entre les cours d'appel de Paris, Versailles, Toulouse, Riom et Pau

import requests
from bs4 import BeautifulSoup
import regex
import pandas as pd
import plotly.express as px
import re

# LOOP 1: creating links on Judilibre
l = []
for x in range(1): #We had to create the links on multiple turns due to the Judilibre website disconnecting us ; the "1000" is just an example
    webpage = requests.get("https://www.courdecassation.fr/recherche-judilibre?search_api_fulltext=&date_du=&date_au=&judilibre_juridiction=ca&judilibre_siege_ca%5B0%5D=ca_paris&judilibre_siege_ca%5B1%5D=ca_pau&judilibre_siege_ca%5B2%5D=ca_riom&judilibre_siege_ca%5B3%5D=ca_toulouse&judilibre_siege_ca%5B4%5D=ca_versailles&judilibre_type_ca%5B0%5D=arret&op=Rechercher%20sur%20judilibre&page="+ str(x))
    soup = BeautifulSoup(webpage.content, features="html.parser") # Making a soup
    div = soup.find("div", class_="view-judilibre") # Finding where the "bit" of URL is
    aas = div.find_all("a")
    for a in aas:
        l.append(a.get("href")) # Appending our links to a list "l"

# LOOP 2: creating a frame with different value columns with the list "l"
tableau = []
for el in l :
    sub = []  # Creating the sublist for the frame
    lien = "https://www.courdecassation.fr" + el # Adding the litte bit of URL

# COLUMN 1: URL LINK added to the frame
    sub.append(lien)
    webpage = requests.get(lien)
    soup2 = BeautifulSoup(webpage.content, features="html.parser")
    text = soup2.getText() # Transforming the soup into a text to be readable

# COLUMN 2: COURT OF APPEAL NAME
    nameofthecourt_start_index = text.lower().find("COUR D'APPEL DE ".lower()) # .lower to ignore different spellings
    if nameofthecourt_start_index != -1:  # Creating an index for the Court of Appeal
        nameofthecourt = text[nameofthecourt_start_index : nameofthecourt_start_index + 30] # Taking the strings after "COUR D'APPEL DE"
        nameofthecourt = nameofthecourt.replace("COUR D'APPEL DE ", "")
    else:
        nameofthecourt_start_index = text.lower().find("COUR D'APPEL D'".lower()) # Same thing but for Courts beginning with vowels
        nameofthecourt = text[nameofthecourt_start_index : nameofthecourt_start_index + 30]
        nameofthecourt = nameofthecourt.replace("COUR D'APPEL D' ", "")
    if nameofthecourt:  # If name of the court exists, append it to the sublist
        sub.append(nameofthecourt.split("\n")[0])
    else:
        sub.append("No Court of Appeal")

# COLUMN 3: DATE
    date = soup2.find("h1") #Finding the "h1" with the inspect method: the date will always be there
    if date:
        sub.append(date.text.split("\n")[0].strip()[-4:]) # The date is the first line, and the year is the last 4 digits
    else:
        sub.append("No date")  # Allows us to check if there is an error

# COLUMN 4: AMOUNT
    dispositif = text.lower().find("Par ces motifs".lower())
    end_text = text[dispositif:]  # In the soup, going forward from "Par ces motifs" now
    art700 = end_text.lower().rfind("article 700".lower()) #Rfind allows us to go from the end to the beginning without reversing the actual letters)  # Finding article 700 in the dispositif

    if art700 != -1: #The condition going through all hypothesis
        art700_short = [end_text[art700 - 100: art700]][-1] # Grabbing the little zone around article 700 reference in the dispositif
        sum_700 = re.search("\d{1,3}(?:([ .'´,\s])?\d{3})*([.,]\d{2})?\s*(Euros?|€|EUROS|euros?)|\d{1}\s\d{3}\s*(Euros?|€|EUROS|euros?)", art700_short) # Searching for the sum close to the article 700 reference within the dispositif
        if sum_700:
            sum_700 = sum_700.group().encode("ascii", "ignore").decode("ascii")
            sum_700 = re.sub("(,|\.)\d\d(?=\D)", "", sum_700) #Taking out all the different . or , or decimals
            sum_700 = re.sub("[^0-9]", "", sum_700) #Putting all the sums into the same format for the CSV
        if sum_700 != None: #Appending the sum if found (if sum_700 is different of None)
            sub.append(sum_700)
        elif sum_700 == None: #Same thing but after the "article 700" reference
            art700_short = [end_text[art700: art700 + 100]][0]  # Grabbing the little zone around article 700 reference in the dispositif
            sum_700 = regex.search("\d{1,3}(?:([ .'´,\s])?\d{3})*([.,]\d{2})?\s*(Euros?|€|EUROS|euros?)|\d{1}\s\d{3}\s*(Euros?|€|EUROS|euros?)", art700_short)  # Searching for the sum close to the article 700 reference within the dispositif
            if sum_700:
                sum_700 = sum_700.group().encode("ascii", "ignore").decode("ascii")
                sum_700 = re.sub("(,|\.)\d\d(?=\D)", "", sum_700)
                sum_700 = re.sub("[^0-9]", "", sum_700)
            if sum_700 != None:
                sub.append(sum_700)
            else:
                sub.append("No EUR value") # Parties requested article 700 but the judge did not grant it
                # print("No EUR value")
    else:
        sub.append("Pas d'Article 700") #No reference to article 700: the parties have not requested so
        # print("Pas d'Article 700")
    tableau.append(sub)

# Creating the dataframe
df = pd.DataFrame(tableau, columns=["URL", "Name of the Court", "Date", "Amount"])

# Creating the CSV file
df.to_csv("/Users/laurinele/PycharmProjects/Legal-Data-Analysis/Final prez 2023/DataframeREAL.csv")

# Plotly
fig = px.histogram(df,x="Amount", color="Name of the Court",
    # marginal="box",  # can be `box`, `violin`
    hover_data=df.columns,
    barmode="group",)

fig.show()



# Note: we have created all the graphs from Plotly. They are stored in different files (one file per plot) and can be put on the GitHub if needed!

