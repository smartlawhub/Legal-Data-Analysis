# Todo: add import of titles and chapters

import dateparser
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from collections import Counter, defaultdict
import pandas as pd
import time

codes = {"Code civil": "codes/texte_lc/LEGITEXT000006070721?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF"}

data_scrapped = []

def get_relative_links(relative_name):
    list_links = []
    ul = driver.find_element_by_xpath(".//*[contains(text(), '" + relative_name + "')]/../following-sibling::ul")
    for li in ul.find_elements_by_xpath(".//li"):
        try:
            href = li.find_element_by_xpath(".//a").get_attribute("href")
        except:
            href = "No URL"
        list_links.append(li.text + " : " + href)
    return list_links

for code in codes.keys():
    print(code)
    driver = webdriver.Chrome(executable_path=r"C:\Users\damie\PycharmProjects\Civil_Law\venv\chromedriver.exe")
    driver.get("https://www.legifrance.gouv.fr/" + codes[code])
    soup = BeautifulSoup(driver.page_source)
    set_articles = soup.find_all("a", text=re.compile("^Article"))
    for e, article in enumerate([x for x in set_articles if "Abrogated" not in x.get("href")]):  # Necessary otherwise stumbles on abrogated articles
        legiarti = re.search("LEGIARTI.*?#", article.get("href")).group()[:-1]
        driver.get("https://www.legifrance.gouv.fr/codes/article_lc/" + legiarti)
        driver.find_elements_by_xpath(".//button[@data-articleid='" + legiarti + "']")[0].click()
        time.sleep(1)
        article_num = driver.find_element_by_class_name("name-article").text
        version_urls = [x.get_attribute("href") for x in driver.find_elements_by_class_name("version")]
        count_version = len(version_urls)
        for version_url in [x for x in version_urls if x is not None]:
            driver.get(version_url)
            legiver = re.search("LEGIARTI.*?/", version_url).group()[:-1]
            driver.find_elements_by_xpath(".//button[@data-articleid='" + legiver + "']|.//button[@data-num='" + article_num.split(" ")[-1] + "']")[0].click()  # Alternative is necessary here as sometimes button does not track the correct LegiArti
            try:
                origin = driver.find_element_by_class_name("date").text
            except:
                origin = ""
            article_text = driver.find_elements_by_class_name("content")[2].text
            temp_list = [code, article_num, driver.current_url, version_url.split("/")[-2], count_version, article_text, origin, "", "", "", ""]
            if len(driver.find_elements_by_xpath( ".//button[@data-articleid='" + legiver + "']")) > 1:
                driver.find_elements_by_xpath(".//button[@data-articleid='" + legiver + "']")[1].click()
                time.sleep(1)
            relatives = driver.find_elements_by_xpath(".//h5")
            for relation in relatives:
                spl = re.sub("<.*?>", "", relation.get_attribute("innerHTML"))
                if re.search("Cit. par", spl):
                    temp_list[-4] = get_relative_links(spl)
                elif re.search("Cite", spl):
                   temp_list[-3] = get_relative_links(spl)
                elif re.search("^Nouveaux", spl):
                    temp_list[-2] = get_relative_links(spl)
                elif re.search("^Anciens", spl):
                    temp_list[-1] = get_relative_links(spl)

            count_version -= 1
            data_scrapped.append(temp_list)
    driver.close()

df = pd.DataFrame(data_scrapped, columns=["Code", "Art", "URL", "Date", "version", "Text", "Created", "Cited_by", "Cite_to", "New", "Old"])
df["ID"] = df["Code"] + "_" + df["Art"] + "_" + df["version"].astype(str)

df["Cut"] = False
for index, row in df.iterrows():
    if len(row["Text"]) > 20000:
        df.at[index, "Text"] = row["Text"][:20000]
        df.at[index, "Cut"] = True
    if len(row["Cited_by"]) > 140:
        df.at[index, "Cited_by"] = row["Cited_by"][:140]
        df.at[index, "Cut"] = True
    if len(row["Cite_to"]) > 140:
        df.at[index, "Cite_to"] = row["Cite_to"][:140]
        df.at[index, "Cut"] = True

df.to_csv("Data.csv", encoding="utf8")
