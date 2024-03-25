# We import necessary libraries
import re
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# We initialize empty lists for data storage
Data_scrap = [] # Store scraped data
url_list = [] # Store URLs of articles

# We define the URL parameters for web scraping
url_beginning = "https://www.legifrance.gouv.fr/search/cetat?tab_selection=cetat&searchField=ALL&query=article+L.64+du+livre+des+proc%C3%A9dures+fiscales&searchType=ALL&dateVersement=01%2F01%2F1990+%3E+01%2F01%2F2024&juridiction=COURS_APPEL&sortValue=DATE_DESC&pageSize=100&page="
url_ending = "&tab_selection=cetat"
to_add_url = "https://www.legifrance.gouv.fr/"

# We define the range of pages to scrape
r = range(15)
# We set up Selenium WebDriver for Chrome
chromedriver_path = "/Users/kenza/Desktop/chromedrivermac"
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chromedriver_path
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.legifrance.gouv.fr/")

# We make a loop to go through each page to scrape articles
for i in r:
    a = i + 1
    url_tot = url_beginning + str(a) + url_ending
    driver.get(url_tot)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    set_articles = soup.find_all("article")
    
    # We extract URLs and titles of articles
    for article in set_articles:
        article_url = article.find(href=True)
        url_list.append(to_add_url + article_url["href"])
        title = article.find("h2").get_text()  
        Data_scrap.append(title)
# We close the Selenium WebDriver
driver.close()

# We save the scraped data to a CSV file
df = pd.DataFrame(Data_scrap, columns=["Title"])
df.to_csv("codepython.csv", encoding="utf-8-sig")

# We read the CSV file into a DataFrame
file_path = "codepython.csv"
data = pd.read_csv(file_path)

# We extract the city and date from the titles using regular expressions
data["City"] = data["Title"].str.extract(r'CAA de (\w+),')
data["Date"] = pd.to_datetime(data["Title"].str.extract(r', (\d{2}/\d{2}/\d{4}),')[0], dayfirst=True)
data["Year"] = data["Date"].dt.year

# We regroup the data by city and year and count occurrences
grouped_data = data.groupby(["City", "Year"]).size().reset_index(name="Counts")
print(grouped_data)

# We pivot the grouped data for better visualization
pivot_data = grouped_data.pivot(index="Year", columns="City", values="Counts").fillna(0)
print(pivot_data)

# We plot bar charts for occurrences by city for each year
years = grouped_data["Year"].unique()

for year in sorted(years):
    data_for_year = grouped_data[grouped_data["Year"] == year]

    data_for_year_sorted = data_for_year.sort_values(by="Counts", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.bar(data_for_year_sorted["City"], data_for_year_sorted["Counts"], color="skyblue")
    plt.title(f"Occurrences by City in {year}")
    plt.xlabel("City")
    plt.ylabel("Occurrences")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

