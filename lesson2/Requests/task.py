# Scrap French constitution

import requests
from bs4 import BeautifulSoup
import regex as re

webpage = requests.get("https://www.conseil-constitutionnel.fr/le-bloc-de-constitutionnalite/texte-integral-de-la-constitution-du-4-octobre-1958-en-vigueur")
soup = BeautifulSoup(webpage.content)

cons_div = soup.find("div", class_="field field--name-field-reference-paragraph field--type-entity-reference-revisions field--label-hidden field__items")

section_with_most_arts = ""

len_section = 0
div = soup.find("div", class_="toc-summary two-level")
for child in div.findChildren("a", text=re.compile("Titre")): # Need to look for 'as' because the 'li' in Browser are not with correct class in Soup
    len_arts = len(child.parent.find_all("li"))
    if len_arts > len_section:
        len_section = len_arts
        section_with_most_arts = child.text

print(section_with_most_arts)
