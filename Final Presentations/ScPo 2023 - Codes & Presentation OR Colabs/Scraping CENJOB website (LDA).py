import selenium
import re
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.poderjudicial.es/search/indexAN.jsp")
time.sleep(2)
jurisdiccion =  driver.find_element(By.XPATH, "/html/body/section/div/div/section/section/div[1]/div[2]/div[1]/form/div[3]/div[1]/div[1]/div/button")
jurisdiccion.click()
time.sleep(1)
jurisdiccion2 =  driver.find_element(By.XPATH, "//*[@id='frmBusquedajurisprudencia']/div[3]/div[1]/div[1]/div/ul/li[2]/a/label/input")
jurisdiccion2.click()
time.sleep(1)
sentencias = driver.find_element(By.XPATH, "/html/body/section/div/div/section/section/div[1]/div[2]/div[1]/form/div[3]/div[1]/div[2]/div/button")
sentencias.click()
time.sleep(1)
sentencias2 = driver.find_element(By.XPATH, "//*[@id='SUBTIPORESOLUCIONpanel']/li[2]/a/b/b")
sentencias2.click()
time.sleep(1)
sentencias3 = driver.find_element(By.XPATH, "//*[@id='list_SENTENCIA']/li[2]/label/b")
sentencias3.click()
time.sleep(1)
tipodeorgano =  driver.find_element(By.XPATH, "/html/body/section/div/div/section/section/div[1]/div[2]/div[1]/form/div[5]/div[1]/div[1]/div/button")
tipodeorgano.click()
time.sleep(1)
tipodeorgan = driver.find_element(By.XPATH, "/html/body/section/div/div/section/section/div[1]/div[2]/div[1]/form/div[5]/div[1]/div[1]/div/ul/li[35]/a/label")
tipodeorgan.click()
time.sleep(1)
search_field = driver.find_element(By.ID, "frmBusquedajurisprudencia_TEXT")
search_field.send_keys("VIOLENCIA SOBRE LA MUJER")
search_field.send_keys(Keys.ENTER)

main_list = []
for x in range(19): # Assuming there are 20 pages of result
    print("Now mining page ", x)
    soup = BeautifulSoup((driver.page_source), "html.parser") # Obtain page_source
    results = soup.find_all("div", class_="row searchresult doc")  # We find all boxes with results
    for result in results: # We loop
        title = result.find("div", class_="title").text.strip()
        metadata = result.find("div", class_="metadatos").text.strip() # Either get the whole text and later mine this metadata, or extract it at that stage - your choice
        url = result.find("a").get("data-link")
        elsummary = result.find("div", class_="hidden hddnsummary")# Summary
        elsummary2 = result.find("div", class_="summary")
        if elsummary is not None:
            summary = elsummary
        else:
            summary = elsummary2
        sublist = [title, metadata, url, summary] # Initiate a sublist to go into the main list
        main_list.append(sublist)

    try:
        el2 = driver.find_element(By.XPATH, ".//*[@data-original-title='Página siguiente']") # This should be the arrow to go to the next page
        el2.click()
    except:
        time.sleep(2)
        el2 = driver.find_element(By.XPATH, ".//*[@data-original-title='Página siguiente']") # This should be the arrow to go to the next page
        el2.click()

    time.sleep(2)

df = pd.DataFrame(main_list, columns=["title", "metadata", "url", "summary"])

main_list2 = []
for index, row in df.iterrows():
    ECLI = re.search("ECLI.*?\n", row["metadata"], re.S|re.I).group() if re.search("ECLI.*?\n", row["metadata"], re.S|re.I) else ""
    N_Resolucion = re.search("Nº de Resolución.*?\n", row["metadata"], re.S|re.I).group() if re.search("Nº de Resolución.*?\n", row["metadata"], re.S|re.I) else ""
    Municipio = re.search("Municipio.*?\n", row["metadata"], re.S|re.I).group() if re.search("Municipio.*?\n", row["metadata"], re.S|re.I) else ""
    Ponente = re.search("Ponente.*?\n", row["metadata"], re.S|re.I).group() if re.search("Ponente.*?\n", row["metadata"], re.S|re.I) else ""
    N_Recurso_match = re.search(r"Nº Recurso:\s*(\d+)/(\d{4})", row["metadata"], re.S | re.I)
    N_Recurso = f"Nº Recurso: {N_Recurso_match.group(1)}/{N_Recurso_match.group(2)}" if N_Recurso_match else ""

    sublist2 = [row["title"], ECLI, N_Resolucion, Municipio, Ponente, N_Recurso, row["url"], row["summary"]]
    main_list2.append(sublist2)

df2 = pd.DataFrame(main_list2, columns=["Title", "ECLI", "N_Resolucion", "Municipio", "Ponente", "N_Recurso", "URL", "Summary"])

print(df2)

with pd.ExcelWriter('/Users/lisamilani/Desktop/Data Base LDA Final.xlsx', engine='openpyxl', if_sheet_exists='new', mode='a') as writer:
    df2.to_excel(writer, sheet_name='Judgements', index=False)


