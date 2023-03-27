# Scrapping

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import csv
import re
import os

driver = webdriver.Chrome()

# Navigate to the web page
url = 'https://www.amf-france.org/fr/sanction-transaction/Decisions-de-la-commission-des-sanctions'
driver.get(url)

# Wait for the dynamic content to load
time.sleep(10)

# Get the HTML content of the page after dynamic content has loaded
html = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Click the "refuser tout" button to disable cookie consent
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tarteaucitronAllDenied2")))
button.click()

# Write to CSV
with open('output1.csv', mode='w') as output_file:
    output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output_writer.writerow(['date', 'theme', 'montant'])

    # Keep scraping the page until the "next page" button is disabled
    count = 0
    while count < 41:
        # Get all <p> tags in the page that contain the Euro symbol
        p_tags = [p for p in soup.find_all('p') if '€' in p.get_text() or 'euros' in p.get_text()]

        # Get all <span> tags with class="tag"
        s_tags = [s for s in soup.find_all('span', {'class': 'tag'})]

        # Get all <span> tags with class="date"
        d_tags = [d for d in soup.find_all('span', {'class': 'date'})]

        # Write the data to the CSV file
        for p, s, d in zip(p_tags, s_tags, d_tags):
            year = d.get_text().split()[-1]  # Extract the last word of the date string
            output_writer.writerow([year, s.get_text(), p.get_text()])
        # Click the "next page" button if it's clickable, otherwise exit the loop
        try:
            button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "DataTables_Table_0_next")), message="Button not clickable within 2 seconds.")
            button.click()
            time.sleep(2)
            # Get the updated HTML content and parse it using BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
        except TimeoutException:
            print("Button not found or not clickable within 10 seconds.")
            break
        count += 1

# Close the browser
driver.quit()

# dans cette partie, je separer les differentes sanctions prononcees dans un meme dossier
with open('output1.csv', mode='r') as input_file, open('output2.csv', mode='w', newline='') as output_file:
    reader = csv.reader(input_file, delimiter=',', quotechar='"')
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        # Split the "montant" column by comma and write each element as a separate column
        montant = re.split('\n(?=\d)', row[2])
        writer.writerow([row[0], row[1]] + montant)

# dans cette partie, je transforme les montants en chiffres

with open('output2.csv', mode='r') as input_file, open('sanctions_amf.csv', mode='w', newline='') as output_file:
    reader = csv.reader(input_file, delimiter=',', quotechar='"')
    writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        row[2] = re.sub(r'\D', '', row[2])  # Remove all non-digit characters from column 2
        writer.writerow(row)

os.remove("output1.csv")
os.remove("output2.csv")

# Dans cette partie nous faisons de la visualisation de données
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (15,8)

#read excel
df = pd.read_excel("/content/sanctions_amf[71] (1).xlsx", header = 1)
df = df.drop(columns=['Unnamed: 3',	'Unnamed: 4',	'Unnamed: 5',	'Unnamed: 6'])
df = df.rename(columns={"Unnamed: 2": "montant"})

# Visualisation
df.head()
df.describe()
df.info()

#Amendes par theme
dict_theme = {}
for theme in df['theme'].unique() : 
    amende_by_theme = df[df['theme']==theme]['montant'].sum()
    number_of_theme = df[df['theme']==theme]['montant'].shape[0]
    dict_theme[theme] = amende_by_theme/number_of_theme
dict_theme = {k: v for k, v in sorted(dict_theme.items(), key=lambda item: item[1])}

plt.scatter(dict_theme.keys(), dict_theme.values())
plt.xticks(rotation=90)
plt.xlabel('Theme')
plt.ylabel('Amende')
plt.title('Amendes infligées en fonction du thème')
plt.show()

#Amendes par date
dict_date = {}
for date in df['date'].unique() : 
    montant_by_date = df[df['date']==date]['montant'].sum()
    number_of_date = df[df['date']==date]['montant'].shape[0]
    dict_date[date] = montant_by_date/number_of_date
dict_date = {k: v for k, v in sorted(dict_date.items(), key=lambda item: item[1])}

plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (15,8)
plt.scatter(dict_date.keys(), dict_date.values())
plt.xticks(rotation=90)
plt.xlabel('Date')
plt.ylabel('Amende')
plt.title('Amendes infligés en fonction des dates')
plt.show()

#Amendes par date sans 2023 (les valeurs sont trop élevées on ne distingue plus les différences des autres années)
dict_date = {}
for date in df['date'].unique() : 
    if date != 2023 : 
        montant_by_date = df[df['date']==date]['montant'].sum()
        number_of_date = df[df['date']==date]['montant'].shape[0]
        dict_date[date] = montant_by_date/number_of_date
dict_date = {k: v for k, v in sorted(dict_date.items(), key=lambda item: item[1])}

plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (15,8)
plt.scatter(dict_date.keys(), dict_date.values())
plt.xticks(rotation=90)
plt.xlabel('Date')
plt.ylabel('Amende')
plt.title('Amendes infligés en fonction des dates sans 2023')
plt.show()


# Comparaison par thème des amendes en fonction du temps
dict_date = {}
for date in df['date'].unique() : 
        montant_by_date = df[df['date']==date]['montant'].sum()
        number_of_date = df[df['date']==date]['montant'].shape[0]
        dict_date[date] = montant_by_date/number_of_date
dict_date = {k: v for k, v in sorted(dict_date.items(), key=lambda item: item[1])}

plt.style.use('ggplot')
plt.rcParams["figure.figsize"] = (15,8)
plt.scatter(dict_date.keys(), dict_date.values())
plt.xticks(rotation=90)
plt.xlabel('Date')
plt.ylabel('Amende')
plt.title('Amendes infligés en fonction du temps')
plt.show()


list_date = df['date'].unique()
dict_df = {}
for theme in df['theme'].unique() :
    dict_montant_date = {}
    #dict_df[theme] = df[df['theme'] == theme]
    for date in list_date :
        dict_montant_date[date] = df[(df['theme'] == theme) & (df['date'] == date)]['montant'].sum()
    dict_df[theme] = dict_montant_date

for i, theme in enumerate(list(dict_df.keys())):
    if i < 5 : 
        plt.plot(list(dict_df[theme].keys()), list(dict_df[theme].values()), label = theme )
    else : 
        plt.plot(list(dict_df[theme].keys()), list(dict_df[theme].values()), label = theme, ls= 'dashed' )

plt.title("Amendes infligés en fonction du temps, par thème")
plt.xlabel('Date')
plt.ylabel('Montant')
plt.legend()
plt.show()


#Histogramme
dict_df_shape = {}
for theme in df['theme'].unique() :
    dict_shape_date = {}
    for date in list_date :
        dict_shape_date[date] = df[(df['theme'] == theme) & (df['date'] == date)].shape[0]
    dict_df_shape[theme] = dict_shape_date

for i, theme in enumerate(list(dict_df_shape.keys())):
    if i < 5 : 
        plt.bar(list(dict_df_shape[theme].keys()), list(dict_df_shape[theme].values()), label = theme )
    else : 
        plt.bar(list(dict_df_shape[theme].keys()), list(dict_df_shape[theme].values()), label = theme )

    plt.title("Nombre de " + theme + " par année")
    plt.xlabel('Date')
    plt.ylabel("Nombre d'infraction")
    plt.legend()
    plt.show()
