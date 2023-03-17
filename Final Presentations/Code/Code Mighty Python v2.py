import re
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys as KeysBrowser

data_scrapped = []

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(“https://www.wipo.int/amc/en/domains/search/legalindex/”)  # Get to WIPO’s main page

categories = soup.find(“div”, class_="ui-fancytree fancytree-container fancytree-plain")
print(len([x for x in categories.descendants]))

driver.find_element(By.XPATH, “/html/body/div[2]/div/div/form/div[1]/div[1]/div/ul/li[1]/span/span[2]”).click()  # Click on the checkbox



driver.find_element(By.XPATH, “/html/body/div[2]/div/div/form/div[2]/input[1]”).click()  # Click on the “Search” button at the bottom of the page

driver.find_element(By.XPATH, “/html/body/div[2]/div/div/div/table/tbody/tr[2]/td[2]/a”).click()

# To start

soup = BeautifulSoup(driver.page_source) # Correspondra à la landing page
lis = soup.find_all("li", id=re.compile("^fancytree-"))
DFS = []
for li in lis:
    url = "https://www.wipo.int/amc/en/domains/search/legalindex/results.jsp?ids1=" + li.get("id").split("-")[-1]
    df = pd.read_html(url)[0]
    driver.get(url)
    subsoup = BeautifulSoup(driver.page_source)
    aas = subsoup.find_all("a", text=re.compile("[A-Z]+\d+-\d+"))
    dd = {}
    for a in aas:
        dd[a.text] = a.get("href")
    df["URL"] = df["Case Details"].map(dd)
    for a in aas:
        driver.get(a.get("href"))
        # Add code to add those elements to the dataframe
    DFS.append(df)
    
df = pd.concat(df)
