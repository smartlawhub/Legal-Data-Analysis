# -*- coding: utf-8 -*-
"""Leniency 1/2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HDnlFruvPNbELOuDrSnLuYs-b6sUAIMo
"""

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

base_url = "https://www.autoritedelaconcurrence.fr"
search_url = f"{base_url}/fr/liste-des-decisions-et-avis?page="
total_decisions = 0
decisions_entente = []
decisions_clemence_entente = []
decisions_transaction = []  # Liste pour les décisions ayant fait l'objet d'une transaction

# Parcourir les pages de liste des décisions/avis
for page in range(127):  # Ajuster le nombre de pages si nécessaire
    response = requests.get(f"{search_url}{page}")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Collecter les URLs des décisions/avis
    for h2 in soup.find_all('h2'):
        a = h2.find('a')
        if a and 'href' in a.attrs:
            total_decisions += 1
            decision_url = base_url + a['href']
            decision_response = requests.get(decision_url)
            decision_soup = BeautifulSoup(decision_response.content, 'html.parser')

            # Vérifier si c'est une décision d'entente
            is_entente = "L. 420-1" in decision_soup.text
            if not is_entente:  # Chercher dans les <span>
                for span in decision_soup.find_all('span'):
                    if "L. 420-1" in span.text:
                        is_entente = True
                        break

            if is_entente:
                decisions_entente.append(decision_url)

            # Vérifier la présence de la procédure de clémence
            procedure_element = decision_soup.find('th', class_="field--label", string="Procédure(s)")
            if procedure_element and procedure_element.find_next_sibling('td').find('a', href="/fr/clemence-0", hreflang="fr"):
                decisions_clemence_entente.append(decision_url)

            # Vérifier la présence de "L. 464-2 III" pour détecter une transaction
            if "L. 464-2 III" in decision_soup.text:
                decisions_transaction.append(decision_url)

# Affichage des résultats
print(f"Nombre total d'avis/décisions : {total_decisions}")
print(f"Nombre de décisions d'entente : {len(decisions_entente)}")
print(f"Nombre de décisions d'entente ayant fait l'objet d'une clémence : {len(decisions_clemence_entente)}")
print(f"Nombre de décisions d'entente et APD ayant fait l'objet d'une transaction : {len(decisions_transaction)}")

# Création du graphique
fig, ax = plt.subplots()
categories = ['Total décisions/avis', 'Décisions d\'entente', 'Décisions d\'entente avec clémence', 'Décisions avec transaction']
values = [total_decisions, len(decisions_entente), len(decisions_clemence_entente), len(decisions_transaction)]
colors = ['blue', 'orange', 'red', 'green']
ax.barh(categories, values, color=colors)
ax.set_xlabel('Nombre')
ax.set_title('Résumé des décisions/avis')
plt.show()