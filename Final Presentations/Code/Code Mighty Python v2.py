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