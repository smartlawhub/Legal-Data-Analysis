# Part 1 : Scraping

import re
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import pandas as pd
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys as KeysBrowser

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # Opening browser
driver.get(“https://www.wipo.int/amc/en/domains/search/legalindex/”)  # Get to WIPO’s main page
 
page_source = “https://www.wipo.int/amc/en/domains/search/legalindex/”
 
soup = BeautifulSoup(driver.page_source) # BeautifulSoup loads the page source
lis = soup.find_all(“li”, id=re.compile(“^fancytree-Cb1-”)) #list of the numbers that are part of the link of each category
del lis[3] #deleting industry and commerce category
DFS = []

#now we get to the case details

links=[]
for li in lis: #creation of a loop in order to open the wanted pages
url = “https://www.wipo.int/amc/en/domains/search/legalindex/results.jsp?ids1=” + li.get(“id”).split(“-”)[-1] #splitting the list lis so that we get only the number we are interested in and we add it to the wipo address
print(url)
links.append(url) #creates a list with the links to all the categories

for link in links:
	df= pd.read_html(link)
	driver.get(link)
subsoup = BeautifulSoup(driver.page_source) 
aas = subsoup.find_all(“a”, string=re.compile(“[A-Z]+\d+-\d+”)) # We extract subdivision of the pages on WIPO’s site
dd = {}
data_rows = [] 
for a in aas:
href = "https://www.wipo.int/amc/en/domains/search/" + a.get("href")[2:] #the complement of the link of each case’s details can be found in href
dd[a.text] = href
driver.get(href) #opening the page with case details
case_soup = BeautifulSoup(driver.page_source)
table = case_soup.find("table")
for tr in table.find_all("tr"): #iterating through table in table rows
tds = tr.find_all("td") #creating cells that contain the wanted elements
if len(tds) == 2:
data_rows.append(tds[1].text.strip())
	
result_list=[]
for i in range(12,len(data_rows),7): #7 is the number of elements of each decision
	if isinstance(data_rows[i],str) and len(data_rows[i])==10:
		continue
	else: 
		data_rows.insert(i,”NA”) #if every 7th element is not a date then write NA
		result_list.append(i)

DFS=[data_rows[i:i+7] for i in range (0,len(data_rows),7)]
uniqueDFS= []

for sublist in DFS: #to delete duplicates
	if sublist not in uniqueDFS:
		uniqueDFS.append(sublist)

frameDFS=pd.DataFrame(uniqueDFS, columns=[“Case Number”, “Domain Name”, “Complainant”, “Respondent”, “Panelist”, “Decision Date”, “Decision”])
frameDFS.to_clipboard(index=False)


# PART 2: Statistical analysis

import matplotlib
import matplotlib.pyplot as plt

frameDFS.describe() #allows to analyze statistically each column 

#Displaying a chart that shows the evolution of the number of decisions throughout the years

frameDFS[“Decision Date”]=pd.to_datetime(frameDFS[“Decision Date”], errors= “coerce”)
mask= frameDFS[“Decision Date”].notna()
df=frameDFS.loc[mask, [“Decision Date”]]
df[“Decision Date”]=pd.to_datetime(df[“Decision Date”])
fig, ax= plt.subplots()
ax.plot(decisions_per_year.index, decisions_per_year.values)
ax.set_xlabel(“Year”)
ax.set_ylabel(“Number of Decisions”)
ax.set_title(“Decisions per Year”)
plt.show()


# displaying the success rate of decisions per panelist

# Count the number of decisions and favorable decisions per panelist
decisions_per_panelist = frameDFS['Panelist'].value_counts()
favorable_decisions_per_panelist = frameDFS[frameDFS['Decision'] == 'Transfer']['Panelist'].value_counts()

# Calculate the success rate per panelist
success_rate_per_panelist = favorable_decisions_per_panelist / decisions_per_panelist

# Sort the panelists by success rate
success_rate_per_panelist = success_rate_per_panelist.sort_values(ascending=False)

# Create a bar plot of the success rate per panelist
plt.figure(figsize=(10, 6))
plt.bar(success_rate_per_panelist.index, success_rate_per_panelist.values)
plt.title('Success Rate per Panelist')
plt.xlabel('Panelist')
plt.ylabel('Success Rate')
plt.xticks(rotation=90)
plt.show()

#creating a pie chart showing the proportion of transferred decisions compared to the total number of decisions made

# Counting the number of transferred decisions
transferred_count = sum(frameDFS['Decision'] == 'Transfer')

# Calculating the proportion of transferred decisions
total_count = len(frameDFS)
transferred_proportion = transferred_count / total_count

# Calculating the proportion of non-transferred decisions
non_transferred_proportion = 1 - transferred_proportion

# Creating labels for the pie chart
labels = ['Transferred', 'Non-Transferred']

# Creating values for the pie chart
values = [transferred_proportion, non_transferred_proportion]

# Creating the pie chart
plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title('Proportion of Transferred Decisions')

# Displaying the chart
plt.show()


