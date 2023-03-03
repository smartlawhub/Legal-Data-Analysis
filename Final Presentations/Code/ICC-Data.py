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
from lxml import etree

PARTIE I

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://iccwbo.org/dispute-resolution-services/arbitration/icc-case-information/")
soup=BeautifulSoup(driver.page_source)

ICC=soup.find("div", class_="content__pad arbitration__pad")
nom_arbitres =[]
for child in ICC.findAll("li"):
    nom_arbitres = nom_arbitres + [child.text]
print(nom_arbitres)

set_tribunaux = soup.find_all("a", text=re.compile("Case ID")) # Dijzdoincouzhenouazhc
Case_ID = [] #dezduonzfeounz
Case_Statut = []
Date = []
Sector_Industry = []
df_list = []
for compo in set_tribunaux:
    sublist = []
    sublist.append(compo.get("href"))
    arbitration = re.search("case-id-\d{5}", compo.get("href")).group()
    driver.get("https://iccwbo.org/dispute-resolution-services/arbitration/icc-case-information/" + arbitration)     
    soup2=BeautifulSoup(driver.page_source)
    test=soup2.find("div", class_ ="page__intro-content")
    h1 = soup.fing(xxx)
    Case_ID = Case_ID + [h1.text]
    sublist.append(h1.text)
    for child in test.findAll("h1"): 
        Case_Statut = Case_Statut + [child.next.next.next.next.next.next.next.next.next.text]
    for child in test.findAll("h1"): 
        Date = Date + [child.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text]
    for child in test.findAll("h1"):
        Sector_Industry = Sector_Industry + [child.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text]
    df_list.append(sublist)
print(Case_ID)
print(Case_Statut)
print(Date)
print(Sector_Industry)


PARTIE II (PAS UTILE POUR LE MOMENT) 

brute = [nom_arbitres, Date, Case_ID, Case_Statut, Sector_Industry]
my_df=pd.DataFrame(df_list)
my_df.T


A REPRENDRE 

set_tribunaux = soup.find_all("a", text=re.compile("Case ID"))
Case_ID = []
Case_Statut = []
Date = []
Sector_Industry = []
Fin = False 

for x in range(214):  # A better way to do it
    url = "https://iccwbo.org/dispute-resolution-services/arbitration/icc-case-information/?fwp_paged=" + str(x)
    driver.get(url)


while Fin == False : 
    for compo in set_tribunaux:
        arbitration = re.search("case-id-\d{5}", compo.get("href")).group()
        driver.get("https://iccwbo.org/dispute-resolution-services/arbitration/icc-case-information/" + arbitration)     
        soup2=BeautifulSoup(driver.page_source)
        test=soup2.find("div", class_ ="page__intro-content")
        Page_Suivante = "https://iccwbo.org/dispute-resolution-services/arbitration/icc-case-information/?fwp_paged=2"
        if Page_Suivante != "":
            driver.get(Page_Suivante)
            time.sleep(1)
        else:
            Fin = True
        for child in test.findAll("h1"):
            Case_ID = Case_ID + [child.next.text]
        for child in test.findAll("h1"): 
            Case_Statut = Case_Statut + [child.next.next.next.next.next.next.next.next.next.text]
        for child in test.findAll("h1"): 
            Date = Date + [child.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text]
        for child in test.findAll("h1"):
            Sector_Industry = Sector_Industry + [child.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text]
print(Case_ID)
print(Case_Statut)
print(Date)
print(Sector_Industry)

