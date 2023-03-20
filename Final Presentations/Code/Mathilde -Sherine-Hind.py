import regex as re
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as KeysBrowser
from webdriver_manager.chrome import ChromeDriverManager
from matplotlib import pyplot as plt
import json
import os
import csv

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Load the search page
driver.get("https://www.bailii.org/form/search_cases.html")
# Find the search box element by name and enter the search query for "Companies Act 2006"
search_box = driver.find_element(By.NAME, "phrase")
search_box.send_keys("Companies Act 2006")
search_box.send_keys(KeysBrowser.RETURN)

# Define search terms and patterns
search_terms = ["Section 172", "Sections 172", "section 172", "sections 172", "ss 172", "SS 172"]
keywords_pattern = re.compile("|".join(search_terms))
context_pattern = re.compile(r"(?s)(.{0,200})(Companies Act 2006)(.{0,200})")


# Collect the URLs for all the search results
citation_urls = []

# Test if citations_url already exists, and load it if true
doCitationsUrlResearch = True
if os.path.exists("citations_urls.json"):
    with open('citations_urls.json') as user_file:
        citation_urls = json.loads(user_file.read())
else:  
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ol = soup.find_all("ol")[0]  # Collect the ol element from the page
        if not ol:
            print("No ol elements found")
            break
        for li in ol.find_all("li"):
            citation_link = li.find("a")
            if citation_link:
                citation_url = "https://www.bailii.org/" + citation_link["href"]
                citation_urls.append(citation_url)
        try:
            # Check if the "Next 10" button exists
            next_button = driver.find_element(By.XPATH, "//input[@value='Next 10 >>>']")
        except:
            # If the button is not found, break out of the loop
            break
        next_button.click()  # Click the "Next 10" button
        time.sleep(1)  # Wait for the next page to load
        
    with open("citations_urls.json","w") as write_file:
        json.dump(citation_urls, write_file, indent=4)


# Collect the URLs for the relevant search results
relevant_urls = []

if os.path.exists("relevant_urls.json"):
    with open('relevant_urls.json') as user_file:
        relevant_urls = json.loads(user_file.read())
else:
    for url in citation_urls:
        # Load the page for each URL
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = soup.get_text()
        # Search for the relevant keywords and context within a specific range of characters
        matches = context_pattern.finditer(text)
        for match in matches:
            if match and (keywords_pattern.search(match.group(1)) or keywords_pattern.search(match.group(3))):
                relevant_urls.append(url)
                break
    # Print the relevant URLs and the total number of relevant URLs
    #print(relevant_urls)
    #print(len(relevant_urls))

    with open("relevant_urls.json","w") as write_file:
        json.dump(relevant_urls, write_file, indent=4)


##Second path

dates = []
jurisdictions = []
judges = []
citations = []
# Loop through each relevant URL
for url in relevant_urls:
    # Load the page for each URL
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    text = soup.get_text()
    # Extract the date from the page
    date = re.search("\(\d+ \w+ \d\d\d\d\)", soup.find("small").text.strip())
    if date:
        dates.append(date.group())
    else:
        dates.append(None)
    # Extract the jurisdiction from the page
    jurisdiction = soup.find("small").find_all("a")[-1]
    if jurisdiction:
        jurisdictions.append(jurisdiction.text.strip())
    else:
        jurisdictions.append(None)
    # Extract the judge(s) from the page
    judge = soup.find("panel")
    eljudge = soup.find("span", text = re.compile("^Before\s*?\:?$"))
    if judge:
        judges.append(judge.text.strip())
    elif eljudge:
        for p in eljudge.parent.parent.fetchNextSiblings("p"):
            if len(p.text.strip()) > 4:
                judges.append(p.text)
                break
    else:
        judges.append(None)
    # Extract the citations from the page
    citation_text= soup.find("citation")
    elcitation = soup.find("p", text=re.compile("(Citation Number|Neutral Citation)"))
    if citation_text:
        citations.append(citation_text.text.strip())
    elif elcitation:
        citations.append(elcitation.text.strip())
    else:
        citations.append(None)
# Create a Pandas DataFrame to store the extracted information
df = pd.DataFrame({
    "Date": dates,
    "Jurisdiction": jurisdictions,
    "Judge": judges,
    "Citation": citations
})
# Display the DataFrame

df.to_csv("result.csv")

import pandas as pd
import datetime
# Read the CSV file into a pandas DataFrame
df = pd.read_csv("result.csv")
# Extract the year from the "Date" column and create a new column called "Year"
df["Year"] = df["Date"].apply(lambda x: datetime.datetime.strptime(x.strip("()"), "%d %B %Y").year)
# Group the DataFrame by year and count the number of rows in each group
decisions_per_year = df.groupby("Year").size()
# Print the result
print(decisions_per_year)

df["Year"] = df["Date"].apply(lambda x: datetime.datetime.strptime(x.strip("()"), "%d %B %Y").year)
import pandas as pd
# Read the data from the CSV file
df = pd.read_csv("result.csv")
# Extract the year from the Date column
df["Year"] = df["Date"].apply(lambda x: datetime.datetime.strptime(x.strip("()"), "%d %B %Y").year)
# Group the data by year and jurisdiction, and count the number of rows in each group
count_by_year_jurisdiction = df.groupby(["Year", "Jurisdiction"]).size().reset_index(name="Count")
# Display the result
print(count_by_year_jurisdiction)


data = pd.read_csv('result.csv')
# group the data by judge name and decision ID, and count the number of occurrences
counts = data.groupby(['Judge']).size().reset_index(name='count')
# group the counts by judge name and count the number of decisions each judge tried more than once
multiple_counts = counts[counts['count'] > 1]
# print the results
print(multiple_counts)
    
