import requests
from bs4 import BeautifulSoup
import regex
import pandas as pd
import plotly.express as px
import re

# import re as re2


l = []  # LOOP 1: creating links on Judilibre
for x in range(10):
    webpage = requests.get(
        "https://www.courdecassation.fr/recherche-judilibre?sort=date-desc&items_per_page=30&judilibre_juridiction=ca&judilibre_siege_ca=ca_agen+ca_paris+ca_riom+ca_toulouse+ca_versailles&op=Sort&page="
        + str(x))
    soup = BeautifulSoup(webpage.content, features="html.parser")
    div = soup.find("div", class_="view-judilibre")
    aas = div.find_all("a")
    for a in aas:
        l.append(a.get("href"))


tableau = []
for el in l[:20] :  # LOOP 2: creating a frame with different value columns
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

    date = soup2.select("h1")[0].text.split("\n")[0].strip()[-4:]
    if date:
        sub.append(date)
    else:
        sub.append("No date") # Allows us to check if there is an error

    dispositif = text.lower().find("Par ces motifs".lower())  # COLUMN 4: AMOUNT
    end_text = text[dispositif:]  # In the soup, going forward from "Par ces motifs" now
    art700 = end_text.lower().rfind(
        "article 700".lower() #Rfind allows us to go from the end to the beginning without reversing the actual letters
    )  # Finding article 700 in the dispositif
    if art700:
        art700_short = end_text[
            art700 - 100 : art700
        ]  # Grabbing the little zone around article 700 reference in the dispositif
        sum_700 = regex.search(
            "\d+\s?\.?(\d+\s?)*(euros|Euros|€|EUROS)", art700_short
        )  # Trouver comment mettre le ' # Searching for the sum close to the article 700 reference within the dispositif
        if sum_700:
            sum_700 = sum_700.group().encode("ascii", "ignore").decode("ascii")
            sum_700 = re.sub("[^0-9]", "", sum_700)
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


fig = px.histogram(
    df,
    x="Amount",
    color="Name of the Court",
    # marginal="box",  # can be `box`, `violin`
    hover_data=df.columns,
    barmode="group",)


fig.show()

print(df)

df.to_csv("/Users/laurinele/PycharmProjects/Legal-Data-Analysis/Final prez 2023/mw.csv")  # Creating the CSV file
