import requests
from bs4 import BeautifulSoup
import regex as re

webpage = requests.get("https://www.hec.edu/fr/grande-ecole-masters/ms-et-msc/ms/llm-droit-et-management-international/programme")
soup = BeautifulSoup(webpage.content)
prix_ao = soup.find(title="Prix Juridique et Fiscal Allen & Overy")
content = prix_ao.parent.parent.text

# Now turning to the Conseil Constitutionnel

webpage = requests.get("https://www.conseil-constitutionnel.fr/le-bloc-de-constitutionnalite/texte-integral-de-la-constitution-du-4-octobre-1958-en-vigueur")
soup = BeautifulSoup(webpage.content)

cons_div = soup.find("div", class_="field field--name-field-reference-paragraph field--type-entity-reference-revisions field--label-hidden field__items")

for child in cons_div.findChildren("h3"):  # Note that all 'find' methods in beautifulsoup work from the point of view of the element you use it on
    print(child)

dic_constitution = {}
for child in cons_div.findChildren("h3"):  # We go over every article
    text = ""  # We create an empty variable to fill with the text
    for sib in child.find_all_next(["h3", "p"]):  # We iterate over the next elements (careful about  'navigableString' elements in siblings
        if sib.name == "h3":  # We check if we have  reached the next article, in which case we  break the loop
            break
        else:  # If we have not reached the next article, we add the text to our variable, separated  by a line-break
            text += "\n" + sib.text.strip()  # Strip because online text often has empty strings at the end and beginning of text
    dic_constitution[child.text.strip()] = text  # Once the loop over the text elements is over, we input it in our dictionary

# Exercise

section_with_most_arts = ""

len_section = 0
div = soup.find("div", class_="toc-summary two-level")
for child in div.findChildren("a", text=re.compile("Titre")): # Need to look for 'as' because the 'li' in Browser are not with correct class in Soup
    len_arts = len(child.parent.find_all("li"))
    if len_arts > len_section:
        len_section = len_arts
        section_with_most_arts = child.text

print(section_with_most_arts)
