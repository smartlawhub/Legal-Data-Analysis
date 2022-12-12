import re
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import pandas as pd
import time
import locale
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import  Keys as KeysBrowser
from matplotlib import pyplot as plt
from datetime import datetime
import dateparser 
import numpy as np
import spacy
import requests
from bertopic import BERTopic  # We import the module
import plotly.io as pio  # This is another plot module in Python
pio.renderers.default = "browser"  # We set it up so that figure appears in a browser
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud



data_scrapped = []

lien_ivresse = "https://www.legifrance.gouv.fr/search/all?tab_selection=all&searchField=ALL&query=ivresse&page=1&init=true"
lien_part1 = "https://www.legifrance.gouv.fr/search/all?tab_selection=all&searchField=ALL&query=ivresse&searchProximity=&searchType=ALL&isAdvancedResult=&isAdvancedResult=&typePagination=DEFAULT&pageSize=10&page="
lien_part2 = "&tab_selection=all"

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

entry_list = []
list_of_lists = []
base_link = "https://www.legifrance.gouv.fr"

for i in range(1,160):  
    print(i)  
    lien = lien_part1 + str(i) + lien_part2
    time.sleep(1)
    driver.get(lien_part1 + str(i) + lien_part2)  # Get the specific law code we are interested, using the dict defined above
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, features = "lxml")  # Read HTML, pass it to a soup object
    results= soup.find_all(class_= "result-item")  
    for result in results:  # Iterate over articles one by one 
        # EXTRACT LINK AND GET TEXT ON PAGE 
        if(result.find("a")["href"]):
            entity_link = base_link + result.find("a")["href"] 
            driver.get(entity_link)
            """
            try:
                our_text = driver.find_elements(By.CLASS_NAME, 'content-page').text
            except:
                try:
                    our_text = driver.find_elements(By.XPATH, '//*[@id="main"]/div/div/div[2]/div[4]/div').text   
                except:
                    our_text = "No text found"""     
        else:
            entity_link ="NA"
           
        # EXTRACT TITLE 
        if len(result.find_all("a", class_ = "name-result-item")) != 0:
            title = result.find_all("a", class_ = "name-result-item")[0].text 
        else:
            title = "NA"
        
        # EXTRACT CATEGORY 
        if result.find_all("a"):
            catégorie = result.find_all("a")[0].text
        
        # EXTRACT DATE : either in title or in category
        if re.search("\d{2}/\d{2}/\d{4}",title):
            date = re.findall("\d{2}/\d{2}/\d{4}",title)[0]    
        
        elif re.search("\d{1,2}\s[a-zà-ü]{3,9}\s\d{4}",title): 
            date = re.findall("\d{1,2}\s[a-zà-ü]{3,9}\s\d{4}", title)[0]
       
        elif re.search("\d{1,2}\s[a-zà-ü]{3,9}\s\d{4}",catégorie):
            
            date = re.findall("\d{1,2}\s[a-zà-ü]{3,9}\s\d{4}",catégorie)[0] 
        else:
            date = "NA"
        # CREATE LIST WITH EXTRACTED DATA 
        our_list = [catégorie, entity_link, title, date] # our text removed at end
        list_of_lists.append(our_list)
driver.close()
df = pd.DataFrame(list_of_lists, columns=["Category", "Link", "Title", "Date"]) # text removed at end 
df.to_csv("ivresse.csv", encoding="utf8")


#==============================================================================
# DATA CLEANING 
#==============================================================================

df = pd.read_csv("ivresse.csv", encoding = "utf8", header = "infer")
print(df.head())

# We also delete the empty columns. 
df = df.drop(["Unnamed: 0"], axis=1) 

df = df.dropna(how = 'all') 


# TRANSFORM DATES INTO DATE TIME OBJECTS !!
format_data = "%d/%m/%Y"
for index, el in df["Date"].items():
    if type(el) == str: 
        if re.search("\d{1,2}/\d{2}/\d{4}",el):
            df["Date"][index] = datetime.strptime(el, format_data).date()
           
        else:
            df["Date"][index] = dateparser.parse(el).date()
            #el = datetime.strptime(el, format_data)


df["Year"] = 0 # default number
# Add a column with year : 
for index, el in df["Date"].items():
    if(type(el) != float):
        df["Year"][index] = el.year




#===========================================================
#PART 2 = TIME ANALYSIS -- THE EVOLUTION 
#===========================================================

# create larger categories 

new_df = pd.DataFrame()
new_list = []

for index, el in df["Category"].items():
    print(el)
    sublist = []
    if "jurisprudence" in el.lower() or "décision" in el.lower():
        print('yes')
        sublist.append("Jurisprudence")
        sublist.append(df["Year"][index])

    elif "loi" in el.lower(): 
        sublist.append("Laws")
        sublist.append(df["Year"][index])
    else:
        pass
    new_list.append(sublist)


new_df = pd.DataFrame(new_list, columns=["Category", "Year"])
print(new_df.head())

new_df = new_df.dropna() 


# Filter by jurisprudence or loi : 

jp_filter = (new_df["Category"] == "Jurisprudence")
jp_df = new_df[jp_filter]

laws_filter = (new_df["Category"] == "Laws")
laws_df = new_df[laws_filter]


jp_df.groupby("Year").size().plot(kind = 'bar') 

plt.show()

laws_df.groupby("Year").size().plot(kind = 'bar') 
plt.show()








