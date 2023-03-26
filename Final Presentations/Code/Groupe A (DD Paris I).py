
import regex as re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys as KeysBrowser
import pandas as pd
import time
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

url = ["https://www.legifrance.gouv.fr/juri/id/JURITEXT000045267337?page=1&pageSize=10&query=%22article+149+du+Code+de+procédure+pénale%22&searchField=ALL&searchType=ALL&sortValue=DATE_DESC&tab_selection=juri&typePagination=DE,FAULT",
"https://www.legifrance.gouv.fr/juri/id/JURITEXT000042438721?page=1&pageSize=10&query=%22article+149+du+Code+de+procédure+pénale%22&searchField=ALL&searchType=ALL&sortValue=DATE_DESC&tab_selection=juri&typePagination=DEFAULT",
"https://www.legifrance.gouv.fr/juri/id/JURITEXT000041810311?page=1&pageSize=10&query=%22article+149+du+Code+de+procédure+pénale%22&searchField=ALL&searchType=ALL&sortValue=DATE_DESC&tab_selection=juri&typePagination=DEFAULT",
"https://www.legifrance.gouv.fr/juri/id/JURITEXT000036980551?page=1&pageSize=10&query=%22article+149+du+Code+de+procédure+pénale%22&searchField=ALL&searchType=ALL&sortValue=DATE_DESC&tab_selection=juri&typePagination=DEFAULT"]

# response = requests.get(url)

# print(driver.status_code)


# créer le dictionnaire finale dans lequel on va stocker la data
all_judgment_dict = {'Title': [], 'Date': [], 'Price': []}

for url in url:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)

    print("scraping in process...")

    # aller chercher le titre
    title = soup.find("h1", class_="main-title").text

    # aller chercher la date
    date_long = soup.find(class_="h2 title horsAbstract print-black").text

    # cut the date after "du"
    date = date_long.split("du ", 1)[1]

    # find the amount after "lui alloue"
    main_div = soup.find("div", class_="content-page")
    text_var = main_div.get_text()

    # check if there is a lui alloue in the content
    result_dispositif = re.search(r"lui alloue | LUI ALLOUE : | LUI ALLOUE", text_var)

    # aller chercher montant (regex qui nous permet de récuperer ces les chiffres avant euros)
    reg = r"(\d+[\ ,\.,\d]*)\s*(e|eur|euros|€|euro)(?:\s|$)"  # r" \b((?:\d+|\d{1,3} (?:[,.\s]\d{3})) (?:[,.\s]*\d+)?)\d*00\s (?: euros?
    article_149 = re.findall(reg, text_var)
    # print(article_149)

    # now we separate space between numbre 12 000 (str) -> 12000 (int)
    pattern = re.compile(r'\s+')
    # get all str and turn them into a int with a loop

    list_eu = [re.sub(pattern, '', x[0]) for x in article_149]
    list_clean_comma = [x.split(',')[0] for x in list_eu]
    list_clean_point = [x.split('.')[0] for x in list_clean_comma]
    list_to_int = [int(x) for x in list_clean_point]

    # sum the int to get a total amount on the judgement.
    montant = sum(list_to_int)

    # feed the dictionnary with the 3 variable that we scraped

    all_judgment_dict["Title"].append(title)

    all_judgment_dict["Date"].append(date)

    all_judgment_dict["Price"].append(montant)

# for number in article_149:
# no_eur_number = re.sub (r [euros | € €│¿|\x80]", "", number, re. IGNORECASE) #la somme de 800, 00 euros no_space_character re.sub (r"\xa0","", ", no_eur_number)
# no_space = re.sub (r" \n", "", no_space_character)
# replaced_number = re.sub (r" [\.], ]\d{2,2}$", “ “, no_space)
# dot_digit = replaced_number.replace(".
# comma_digit = dot_digit.replace(“,”, “ “)
# joined digit = comma_digit.replace(“,”, “ “)
# if re.search(r" \d{3,5}", joined_digit) and re.search(r"0{2,4}", joined_digit) : #end_with_0_digit re.sub (r" ([1-9]+)$", "0", joined digit)
# digit = int (joined_digit)
# digit_list.append(digit)
# else:
# digit_list.append(0)
# if len(digit_list)>0:
# max_amount=max(digit_list)
# print (max_amount)
# sub_list.append(max_amount)
# else:
# sub_list.append(0)
# print(text_var)
# print(result_dispositif)

print(all_judgment_dict)

...

data_frame = pd.DataFrame.from_dict(all_judgment_dict)
data_frame.to_excel("/Users/lina/Desktop/LDA.xlsx", engine="openpyxl", index=False)