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
from openpyxl import Workbook
from gender_guesser.detector import Detector
DG = Detector()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
Case_ID = []
Case_Statut = []
Date = []
Sector_Industry = []
df_list = []
inter = []
Nationality = []
aha = []
All_Names=[]
Genre=[]
for x in range(1,216):
    url= "https://iccwbo.org/dispute-resolution-services/arbitration/icc-case-information/?fwp_paged=" + str(x)
    driver.get(url)
    soup=BeautifulSoup(driver.page_source)
    ICC=soup.find("div", class_="content__pad arbitration__pad")
    set_tribunaux = soup.find_all("a", text=re.compile("Case ID"))
    Name = []
    for child_ul in soup.find_all("ul"):
        for child in child_ul.find_all("li"):
            Name = Name + [child.text]
            break
    Name = Name[5:-2]
    for x in range(len(Name)):
        All_Names = All_Names + [Name[x]]
    for x in range(len(Name)):
        Genre = Genre + [DG.get_gender(Name[x].split(" ")[-1])]
    df_list.append(Genre)
    for compo in set_tribunaux:
        sublist = []
        sublist.append(compo.get("href"))
        arbitration = re.search("case-id-\d{5}", compo.get("href")).group()
        driver.get("https://iccwbo.org/dispute-resolution-services/arbitration/icc-case-information/" + arbitration)
        soup2=BeautifulSoup(driver.page_source)
        test=soup2.find("div", class_ ="page__intro-content")
        h1 = soup2.find("h1", class_="page__title arbitration__low")
        Case_ID = Case_ID + [h1.text]
        sublist.append(h1.text)
        for child in test.findAll("h1"):
            Case_Statut = Case_Statut + [child.next.next.next.next.next.next.next.next.next.text]
        sublist.append(Case_Statut)
        for child in test.findAll("h1"):
            Date = Date + [child.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text]
        sublist.append(Date)
        for child in test.findAll("h1"):
            Sector_Industry = Sector_Industry + [child.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text]
        sublist.append(Sector_Industry)
        df_list.append(sublist)
df_list.append(All_Names)
for x in range(1,216):
    a = []
    aha =[]
    Nationality =[]
    url= "https://iccwbo.org/dispute-resolution-services/arbitration/icc-case-information/?fwp_paged=" + str(x)
    driver.get(url)
    soup=BeautifulSoup(driver.page_source)
    divs = soup.find_all("div", class_="arbitration__entry-section")  # We get all the relevant divs on the page
    for div in divs:
        a = a + [div.find("a")]
    for i in range(len(a)):
        if i%3 ==2 :
            aha = aha + [a[i]]
    for compo in aha :
        if compo is not None :
            arbitration = re.search("arbitration/icc-arbitral-tribunals/[a-z-]+", compo.get("href")).group()
            driver.get("https://iccwbo.org/dispute-resolution-services/" + arbitration)
            soup5= BeautifulSoup(driver.page_source)
            test = soup5.find("div", class_= "page__intro-content")
            for child in test.findAll("p"):
                Nationality = Nationality + [child.next.text]
        else :
            Nationality = Nationality + ["No arbitrator"]
    for i in range(len(Nationality)):
        if i % 2 == 1:
            inter = inter + [Nationality[i][:-5]]
df_list.append(inter)
df1=pd.DataFrame(Case_ID)
df2=pd.DataFrame(Case_Statut)
df3=pd.DataFrame(Date)
df4=pd.DataFrame(Sector_Industry)
df5=pd.DataFrame(All_Names)
df6=pd.DataFrame(Genre)
df7=pd.DataFrame(inter)
merged_df=pd.concat([df1, df2],axis=1)
merged_df=pd.concat([merged_df, df3], axis=1)
merged_df=pd.concat([merged_df, df4], axis=1)
merged_df=pd.concat([merged_df, df5], axis=1)
merged_df=pd.concat([merged_df, df6], axis=1)
merged_df=pd.concat([merged_df, df7], axis=1)
final_df=merged_df.set_axis(["ID","Statut", "Date", "Secteur","Name", "Genre", "Nationality"], axis=1)
df = pd.DataFrame(final_df,columns=["ID","Statut", "Date", "Secteur","Name", "Genre", "Nationality"])
df.to_excel("document.xlsx")

