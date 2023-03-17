import regex as re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver  # Instead, we'll use Selenium
# (remember to use pip install X if you don't have module X)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys as KeysBrowser
import pandas as pd
import time
from matplotlib import pyplot as plt

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# This launches the browser
driver.get("https://www.bailii.org/cgi-bin/lucy_search_1.cgi?datehigh=&highlight=1&sort=rank&datelow=&mask_path=/eu/cases+/ew/cases+/ie/cases+/nie/cases+/scot/cases+/uk/cases+/ae/cases+/qa/cases+/sh/cases+/je/cases&query=(%22section%20172%20of%20the%20Companies%20Act%202006%22)&method=boolean") # We go to the CE's database

soup = BeautifulSoup(driver.page_source)
ol = soup.find("ol")  # Collect the <ol> element from the page.

#print(ol)

soup = BeautifulSoup(driver.page_source)
ol = soup.find("ol")  # Collect the <ol> element from the page.

lis = ol.find_all("li")  # Find all the <li> elements within the <ol>
print(ol)

 
With loop:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Open Chrome browser and go to the URL
url = "https://www.bailii.org/cgi-bin/lucy_search_1.cgi?query=(%22section%20172%20of%20the%20Companies%20Act%202006%22)&datehigh=&mask_path=/eu/cases+/ew/cases+/ie/cases+/nie/cases+/scot/cases+/uk/cases+/ae/cases+/qa/cases+/sh/cases+/je/cases&highlight=1&method=boolean&sort=rank&datelow="
driver = webdriver.Chrome()
driver.get(url)

citations = []

# loop through all the pages
while True:
    soup = BeautifulSoup(driver.page_source)
    ol = soup.find_all("ol")[0]  # Collect the ol element from the page
    for li in ol.find_all("li"):
        citation = li.text
        citations.append(citation)
    try:
        # Check if the "Next 10" button exists
        next_button = driver.find_element(By.XPATH, "//tb[contains(name = text(), 'Next 10')]")
    except NoSuchElementException:
        # If the button is not found, break out of the loop
        break
    next_button.click()  # Click the "Next 10" button
    time.sleep(2)  # Wait for the next page to load

# close the browser
driver.quit()

# display the dataframe
print(df.head())

# Create a Pandas dataframe from the list of citations
df = pd.DataFrame(citations)

# Print the dataframe
print(df)

# CODE POUR ALLER PLUS LOIN

# Allez sur la page avec les résultats qui vous intéressent
soup = BeautifulSoup(driver.page_source)
aas = soup.find_all("a", href=re.compile("^/[a-z]+/cases/"))  # Liste de decisions, le regex ne prenant que les
# URLs des décisions sans highlight

# Second boucle sur les decisions
L = []
for a in aas:
    ll = []
    url = "https://www.bailii.org" + a.get("href")
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    TT = soup.getText()
    sea = re.search("sections? 172|ss? 172", TT, re.S)
    if sea:
        seabis = re.search("Companies Act 2006", TT[sea.start() - 200:sea.start() + 200], re.S)
        if seabis:
            ll.append(url)
            # Trouver Data
            ll.append(len(TT))
            L.append(ll)
