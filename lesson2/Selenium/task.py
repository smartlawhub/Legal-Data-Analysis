import regex as re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import  Keys as KeysBrowser


webpage = requests.get("https://www.conseil-etat.fr/ressources/decisions-contentieuses/arianeweb2")
soup = BeautifulSoup(webpage.content)

table = soup.find("table")

driver = webdriver.Chrome(executable_path="../windows-webdriver.exe")
driver.get("https://www.conseil-etat.fr/ressources/decisions-contentieuses/arianeweb2") # Even on this page, the search tool, while it displays in the robot browser, can't be reached with the Code Source; but you can see in page source that the search tool is fetched from a "recherche" webpage, and we'll start from this

driver.get("https://www.conseil-etat.fr/arianeweb/#/recherche")

el = driver.find_element_by_xpath(r'.//*[contains(text(), "Décisions du Conseil")]') # After a lot of trial and error, we were able to locate the required element, and from this to check the radio box
el.click()  # We click on the category we are interested in

button = driver.find_element_by_xpath(".//button[@class='btn btn-primary']")  # This one was easier
button.click()  # and then on the button, which discloses the table

table = BeautifulSoup(driver.page_source).find_all("table")[-1]  # Collect tables from the page; there are two of them in the page source, and we are interested in the last one, with results

df = pd.read_html(str(table))[-1]  # To make things easier, we convert the table in a panda dataframe. Not the 'str' command: it's because the original table is an object (and not a string). This returns a list of dataframes, so make sure to select only one, most often the last one
df.head(10)  # Always a good idea to see what the dataframe look like

for index, row in df.iterrows():  # For each row, we'll make the browser click on the element and collect the judgment
    num = re.search("\d+", row["Numéro d'affaire"]).group()  # Taking only the number because the (...) messes up xPath
    rowel = driver.find_element_by_xpath(".//td[contains(text(), '" + num + "')]")
    rowel.click()  # load page with judgment
    time.sleep(2)  # Giving the page time to load before changing focus
    driver.switch_to_window(driver.window_handles[-1])  # Switch the driver's focus to the window you just opened
    ave_el = driver.find_element_by_css_selector("button[title='enregistre le document']") # Find the download button, using CSS selector here so as to rely on the unique 'title'
    ave_el.click() # Downloading the judgment, in html format; it will end up in your normal Download folder
    driver.switch_to_window(driver.window_handles[0])  # Important to return to main window, or the next search for rowel won't work

# We could add another loop to go over the various pages of result tables. And then it's a question of opening the 50+ files you just downloaded, and work on them
