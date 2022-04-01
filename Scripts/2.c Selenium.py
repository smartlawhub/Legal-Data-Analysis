import regex as re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time



webpage = requests.get("https://www.conseil-etat.fr/ressources/decisions-contentieuses/arianeweb2")    # We try to get the conseil d'Etat research page
soup = BeautifulSoup(webpage.content)  # We create a soup element on that basis

table = soup.find("table")  # We look for the table with documents to download
print(table)  # Uh oh

from selenium import webdriver  # Instead, we'll use Selenium (remember to use pip install X if you don't have module X)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import  Keys as KeysBrowser

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.conseil-etat.fr/ressources/decisions-contentieuses/arianeweb2")  # Even on this page, the search tool, while it displays in the robot browser, can't be reached with the Code Source; but you can see in page source that the search tool is fetched from a "recherche" webpage, and we'll start from this

driver.get("https://www.conseil-etat.fr/arianeweb/#/recherche")
soup = BeautifulSoup(driver.page_source)  # Putting the first page result in soup, because it's easier to analyse the HTML that way
soup.find_all("div", class_="checkbox")  # We look for the checkbos we are interested in, but there are too many
soup.find("input", attrs={"ng-change":"sources.selectSource('AW_DCE')"})  # Instead, we look for the one we are interested in particular, noticing (in Chrome's Inspect Tool) that the relevant checkbox comes with an input el, with a unique data point for attribute: this AW_DCE thing
print(BeautifulSoup(driver.page_source))  # However we don't only need to know it's here, we also need to click on it with driver, so let's look at what the .html around looks like
el = driver.find_element(By.XPATH, r'.//*[contains(text(), "Décisions du Conseil")]')  # We ultimately realise that the relevant checkbox has this unique text, so we use xPath to get button
el.click()  # We click on the element we are interested in

button = driver.find_element(By.XPATH, ".//button[@class='btn btn-primary']")  # Next we need to click on "Rechercher"; Inspect tool tells us that this is how to find it
button.click()  # and then on the button, which discloses the table

table = BeautifulSoup(driver.page_source).find_all("table")[-1]  # Collect tables from the page; there are two of them in the page source (and find_all returns a list), and we are interested in the last one, with results. -1  indexing is not ideal, though, we should sort by length maybe

df = pd.read_html(str(table))[-1]  # To make things easier, we convert the table in a panda dataframe, with each row storing data about one decision. Note the 'str' command: it's because the original table is an object (and not a string). This method returns a list of dataframes, so make sure to select the last one
df.head(10)  # Always a good idea to see what the dataframe look like

for index, row in df.iterrows():  # For each row, we'll make the browser click on the element and collect the judgment
    num = re.search(r"\d+", row["Numéro d'affaire"]).group()  # Taking only the number because the (...) messes up xPath
    row_el = driver.find_element(By.XPATH, ".//td[contains(text(), '" + num + "')]")  # With that num, we look for the relevant element in browser
    row_el.click()  # load page with judgment
    time.sleep(2)  # Giving the page time (2s) to load before changing focus with function time.sleep (imported above)
    driver.switch_to.window(driver.window_handles[-1])  # Switch the driver's focus to the window you just opened, with method "switch to", and argument the relevant window from the list of window_handles (latest loaded window will be -1)
    ave_el = driver.find_element(By.CSS_SELECTOR, "button[title='enregistre le document']")  # Find the download button, using CSS selector here so as to rely on the unique 'title'
    ave_el.click()  # Downloading the judgment, in html format; it will end up in your normal Download folder
    driver.switch_to.window(driver.window_handles[0])  # Important to return to main window, or the next search for rowel won't work

# We could add another loop to go over the various pages of result tables. And then it's a question of opening the 50+ files you just downloaded, and work on them
