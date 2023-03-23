import requests
from bs4 import BeautifulSoup
import regex
import pandas as pd
import plotly.express as px
import re

# import re as re2


l = []  # LOOP 1: creating links on Judilibre
for x in range(6):
    webpage = requests.get(
        "https://www.courdecassation.fr/recherche-judilibre?search_api_fulltext=&date_du=&date_au=&judilibre_juridiction=ca&judilibre_siege_ca%5B0%5D=ca_paris&judilibre_siege_ca%5B1%5D=ca_pau&judilibre_siege_ca%5B2%5D=ca_riom&judilibre_siege_ca%5B3%5D=ca_toulouse&judilibre_siege_ca%5B4%5D=ca_versailles&judilibre_type_ca%5B0%5D=arret&op=Rechercher%20sur%20judilibre&page="
        + str(x))
    soup = BeautifulSoup(webpage.content, features="html.parser")
    div = soup.find("div", class_="view-judilibre")
    aas = div.find_all("a")
    for a in aas:
        l.append(a.get("href"))


tableau = []
for el in l[:50] :  # LOOP 2: creating a frame with different value columns
    sub = []  # Creating the sublist for the frame
    lien = "https://www.courdecassation.fr" + el
    sub.append(lien)  # COLUMN 1: URL LINK
    webpage = requests.get(lien)
    soup2 = BeautifulSoup(webpage.content, features="html.parser")
    text = soup2.getText()

    nameofthecourt_start_index = text.lower().find("COUR D'APPEL DE ".lower())  # COLUMN 2: COURT OF APPEAL NAME
    if nameofthecourt_start_index != -1:  # Creating an index for the Court of Appeal
        nameofthecourt = text[nameofthecourt_start_index : nameofthecourt_start_index + 30]
        nameofthecourt = nameofthecourt.replace("COUR D'APPEL DE ", "")
    else:
        nameofthecourt_start_index = text.lower().find("COUR D'APPEL D'".lower())
        nameofthecourt = text[nameofthecourt_start_index : nameofthecourt_start_index + 30]
        nameofthecourt = nameofthecourt.replace("COUR D'APPEL D' ", "")
    if nameofthecourt:  # If name of the court exists, append it to the sublist
        sub.append(nameofthecourt.split("\n")[0])
    else:
        sub.append("No Court of Appeal")

    #date = soup2.select("h1")[0].text.split("\n")[0].strip()[-4:] # COLUMN 3: DATE
    #if date:
        #sub.append(date)
    #else:
     #   sub.append("No date") # Allows us to check if there is an error

    date = soup2.find("h1") # COLUMN 3: DATE
    if date:
        sub.append(date.text.split("\n")[0].strip()[-4:])
    else:
        sub.append("No date")  # Allows us to check if there is an error

    dispositif = text.lower().find("Par ces motifs".lower())  # COLUMN 4: AMOUNT
    end_text = text[dispositif:]  # In the soup, going forward from "Par ces motifs" now
    art700 = end_text.lower().rfind(
        "article 700".lower() #Rfind allows us to go from the end to the beginning without reversing the actual letters
    )  # Finding article 700 in the dispositif
    if art700:
        art700_short = end_text[art700 - 150: art700 + 150] # Grabbing the little zone around article 700 reference in the dispositif
        sum_700 = regex.search(
            "\d{1,3}(?:([ .'´`])?\d{3})*([.,]\d{2})?\s*(Euros?|€|euros|Euros|€|EUROS)", art700_short
        ) # Searching for the sum close to the article 700 reference within the dispositif
        if sum_700:
            sum_700 = sum_700.group().encode("ascii", "ignore").decode("ascii")
            sum_700 = re.sub("[^0-9]", "", sum_700) #Finding the sum even if we are going reverse and replacing the sum that can be in multiple format by a comparable sum
            sub.append(sum_700)
        else:
            sub.append("No EUR value")
            # print("No EUR value")
    else:
        sub.append("Pas d'Article 700")
        # print("Pas d'Article 700")
    tableau.append(sub)
    # print(tableau)

df = pd.DataFrame(
    tableau, columns=["URL", "Name of the Court", "Date", "Amount"]
)  # Creating the dataframe


fig = px.histogram(df,x="Amount", color="Name of the Court",
    # marginal="box",  # can be `box`, `violin`
    hover_data=df.columns,
    barmode="group",)


fig.show()

print(df)

df.to_csv("/Users/laurinele/PycharmProjects/Legal-Data-Analysis/Final prez 2023/mw.csv")  # Creating the CSV file

#mean_amount = df['AMOUNT'].mean()
#print(mean_amount)