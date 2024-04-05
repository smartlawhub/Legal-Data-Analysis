from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

options = Options()
service = Service(executable_path='/Users/Edouard Tan/LDA/chromedriver')
driver = webdriver.Chrome(service=service, options=options)
url = "https://www.cnil.fr/fr/les-sanctions-prononcees-par-la-cnil"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
articles = soup.find_all('article', class_='result-item')

data = []

rows = soup.find_all('tr')

for row in rows:
    cells = row.find_all('td')
    if len(cells) > 3:
        date = cells[0].text.strip()
        year_match = re.search(r'\b(20\d{2})\b', date)
        if year_match:
            year = int(year_match.group(0))
            if year < 2019:
                continue

        secteur_activite_cell = cells[1]
        for glossary_tooltip in secteur_activite_cell.select('.glossary-tooltips'):
            glossary_tooltip.decompose()

        secteur_activite = ' '.join(secteur_activite_cell.stripped_strings)

        manquements_cell = cells[2]
        for glossary_tooltip in manquements_cell.select('.glossary-tooltips'):
            glossary_tooltip.decompose()

        manquements = ' '.join(manquements_cell.stripped_strings)
        decision = cells[3].text.strip()
        
        amende_match = re.search(r'(\d+[\s]*\d+)', decision)
        montant_amende = amende_match.group(0).replace(' ', '') if amende_match else 'N/A'
        
        data.append({
            'Date': date,
            'Secteur d\'activité': secteur_activite,
            'Manquements principaux': manquements,
            'Montant de l\'amende': montant_amende
        })

df = pd.DataFrame(data)
df.to_csv('DF_CNIL_RAW.csv', index=False, encoding='utf-8-sig')

print("La collecte des données est terminée. Le fichier 'DF_CNIL_RAW.csv' a été enregistré sur votre ordinateur.")

driver.quit()