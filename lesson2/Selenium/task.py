import regex as re
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time



webpage = requests.get("https://www.conseil-etat.fr/ressources/decisions-contentieuses/arianeweb2")
soup = BeautifulSoup(webpage.content)

table = soup.find("table")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import  Keys as KeysBrowser

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.conseil-etat.fr/ressources/decisions-contentieuses/arianeweb2")  # Even on this page, the search tool, while it displays in the robot browser, can't be reached with the Code Source; but you can see in page source that the search tool is fetched from a "recherche" webpage, and we'll start from this

driver.get("https://www.conseil-etat.fr/arianeweb/#/recherche")

soup.find_all("div", class_="checkbox")
soup.find("input", attrs={"ng-change":"sources.selectSource('AW_DCE')"})
print(BeautifulSoup(driver.page_source))
el = driver.find_element(By.XPATH, r'.//*[contains(text(), "Décisions du Conseil")]')  # After a lot of trial and error, we were able to locate the required element, and from this to check the radio box
el.click()  # We click on the category we are interested in

button = driver.find_element(By.XPATH, ".//button[@class='btn btn-primary']")  # Looking for the "Rechercher" Button
button.click()  # and then on the button, which discloses the table

table = BeautifulSoup(driver.page_source).find_all("table")[-1]  # Collect tables from the page; there are two of them in the page source, and we are interested in the last one, with results. -1  indexing is not ideal, though, we should sort by length maybe

df = pd.read_html(str(table))[-1]  # To make things easier, we convert the table in a panda dataframe. Not the 'str' command: it's because the original table is an object (and not a string). This returns a list of dataframes, so make sure to select only one, most often the last one
df.head(10)  # Always a good idea to see what the dataframe look like

for index, row in df.iterrows():  # For each row, we'll make the browser click on the element and collect the judgment
    num = re.search(r"\d+", row["Numéro d'affaire"]).group()  # Taking only the number because the (...) messes up xPath
    rowel = driver.find_element(By.XPATH, ".//td[contains(text(), '" + num + "')]")
    rowel.click()  # load page with judgment
    time.sleep(2)  # Giving the page time to load before changing focus
    driver.switch_to_window(driver.window_handles[-1])  # Switch the driver's focus to the window you just opened
    ave_el = driver.find_element(By.CSS_SELECTOR, "button[title='enregistre le document']") # Find the download button, using CSS selector here so as to rely on the unique 'title'
    ave_el.click() # Downloading the judgment, in html format; it will end up in your normal Download folder
    driver.switch_to_window(driver.window_handles[0])  # Important to return to main window, or the next search for rowel won't work

# We could add another loop to go over the various pages of result tables. And then it's a question of opening the 50+ files you just downloaded, and work on them
