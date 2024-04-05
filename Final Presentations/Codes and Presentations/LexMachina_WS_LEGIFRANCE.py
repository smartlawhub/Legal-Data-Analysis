from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import urllib.parse

options = Options()
service = Service(executable_path='/Users/Edouard Tan/LDA/chromedriver')
driver = webdriver.Chrome(service=service, options=options)
url = "https://www.legifrance.gouv.fr/search/cnil?facetteNatureDelib=Sanction&page=1&pageSize=100&searchField=ALL&searchType=ALL&sortValue=DATE_DECISION_DESC&tab_selection=cnil&typePagination=DEFAULT"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
articles = soup.find_all('article', class_='result-item')

data = []

for article in articles:
    link = article.find('a')['href']
    full_link = f"https://www.legifrance.gouv.fr{link}"
    driver.get(full_link)
    time.sleep(5)
    detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    sanction_intro = detail_soup.find('div', class_='intro under-frame').strong.text
    sanction_titre_regex = r"Délibération de la formation restreinte (?:n°|no |n°)?\s*(SAN[\s–-]*\d+[\s–-]*\d+) du (\d+\s?\w+ \d+) (?:concernant|prononçant une sanction (?:pécuniaire )?à l[’']encontre de) (?:(?:la |le |les |l[’']))?(société|SOCIETE|sociétés|commune|personne physique|GIE|Madame|Monsieur|Association|Fédération)? ?(.+)"
    match = re.search(sanction_titre_regex, sanction_intro)
    
    if match:
        sanction_numero = match.group(1)
        sanction_date = match.group(2)
        entite_type = match.group(3) if match.group(3) else "Non spécifié"
        entite_nom = match.group(4).strip()

        if any(pattern in entite_nom.lower() for pattern in [' x ', ' X ', 'x et y', '[...]']):
            query = f"CNIL {sanction_numero}"
            entite_nom = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    
    else:
        continue
    
    sanction_corps = detail_soup.get_text()
    
    rgpd_ref_regex = r"Vu le règlement \(UE\)"
    if not re.search(rgpd_ref_regex, sanction_corps):
        print("Référence au RGPD non trouvée, arrêt du programme.")
        break
    
    start_index = sanction_corps.find("PAR CES MOTIFS")
    end_index = sanction_corps.find("Alexandre LINDEN", start_index)
    if start_index != -1 and end_index == -1:
        end_index = len(sanction_corps)
    sanction_corps_focus = sanction_corps[start_index:end_index] if start_index != -1 else ""

    amendes_regex = r"montant de.*?(\d{1,3}(?:[\s\.,]?\d{3})*).*?(?:pour|au regard|au titre)?"
    amendes_match = re.findall(amendes_regex, sanction_corps_focus, re.IGNORECASE | re.DOTALL)
    amendes_str = "; ".join(amendes_match) if amendes_match else "Aucune amende pécuniaire prononcée."
    
    articles_vise_set = set()

    amendes_regex = r"articles? (\d+(?:[-.]\d+)?(?:-[a-z]\)?)?(?:,? paragraphe\s?\d+)?(?:\s?[a-z]\)?)?(?:\s*(?:,|et)\s*\d+(?:[-.]\d+)?(?:-[a-z]\)?)?(?:,? paragraphe\s?\d+)?(?:\s?[a-z]\)?)?)*)\b"
    fondement_regex = r"(du RGPD|du règlement \(UE\)|du règlement no|de la loi (Informatique et Libertés|informatique et libertés|n° 78-17|du 6 janvier 1978 modifiée?)|\"Informatique et Libertés\"|\"informatique et libertés\"|\"[ ]?Informatique et Libertés[ ]?\")"

    articles_matches = re.findall(amendes_regex, sanction_corps_focus, re.IGNORECASE | re.DOTALL)

    for article_match in articles_matches:
        subsequent_text = sanction_corps_focus[sanction_corps_focus.find(article_match) + len(article_match):]
        fondement_match = re.search(fondement_regex, subsequent_text, re.IGNORECASE)

        fondement_reformulation = ""
        if fondement_match:
            extracted_text = fondement_match.group()
            if "RGPD" in extracted_text or "règlement" in extracted_text:
                fondement_reformulation = "du RGPD"
            elif "loi" in extracted_text:
                fondement_reformulation = "de la LIL"
            result = f"Article {article_match} {fondement_reformulation}".strip()
            articles_vise_set.add(result)

    articles_vise_str = "; ".join(sorted(articles_vise_set)) if articles_vise_set else "Non trouvés"

    data.append([sanction_numero, sanction_date, entite_type, entite_nom, amendes_str, articles_vise_str])

driver.quit()

df = pd.DataFrame(data, columns=['Numéro de sanction', 'Date', 'Type d\'entité', 'Nom de l\'entité', 'Montants des amendes', 'Articles violés'])
df.to_csv('DF_LEGIFRANCE_RAW.csv', index=False)

print("La collecte des données est terminée. Le fichier CSV 'DF_LEGIFRANCE_RAW.csv' a été enregistré sur votre ordinateur.")