import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

data_scrapped = []
codes = {'Code civil': '/affichCode.do?cidTexte=LEGITEXT000006070721', "Code de l'action sociale et des familles": '/affichCode.do?cidTexte=LEGITEXT000006074069',
 "Code du cinéma et de l'image animée": '/affichCode.do?cidTexte=LEGITEXT000020908868',
 'Code de la commande publique': '/affichCode.do?cidTexte=LEGITEXT000037701019&idSectionTA=&dateTexte=20190401',
 'Code de commerce': '/affichCode.do?cidTexte=LEGITEXT000005634379',
 'Code des communes de la Nouvelle-Calédonie': '/affichCode.do?cidTexte=LEGITEXT000006070300',
 'Code de la consommation': '/affichCode.do?cidTexte=LEGITEXT000006069565',
 "Code de la construction et de l'habitation": '/affichCode.do?cidTexte=LEGITEXT000006074096&dateTexte=20190901',
 'Code de la défense': '/affichCode.do?cidTexte=LEGITEXT000006071307',
 "Code de l'éducation": '/affichCode.do?cidTexte=LEGITEXT000006071191',
 "Code de l'énergie": '/affichCode.do?cidTexte=LEGITEXT000023983208',
 "Code de l'environnement": '/affichCode.do?cidTexte=LEGITEXT000006074220',
 'Code forestier': '/affichCode.do?cidTexte=LEGITEXT000025244092',
 'Code général des collectivités territoriales': '/affichCode.do?cidTexte=LEGITEXT000006070633',
 'Code général de la propriété des personnes publiques': '/affichCode.do?cidTexte=LEGITEXT000006070299',
 'Code des juridictions financières': '/affichCode.do?cidTexte=LEGITEXT000006070249',
 'Code de justice administrative': '/affichCode.do?cidTexte=LEGITEXT000006070933',
 'Code de justice militaire': '/affichCode.do?cidTexte=LEGITEXT000006071360',
 'Code de la justice pénale des mineurs': '/affichCode.do?cidTexte=LEGITEXT000039086952&idSectionTA=&dateTexte=20201001',
 'Code monétaire et financier': '/affichCode.do?cidTexte=LEGITEXT000006072026',
 'Code du patrimoine': '/affichCode.do?cidTexte=LEGITEXT000006074236',
 "Code des pensions militaires d'invalidité et des victimes de guerre": '/affichCode.do?cidTexte=LEGITEXT000006074068',
 "Code des procédures civiles d'exécution": '/affichCode.do?cidTexte=LEGITEXT000025024948',
 'Code de la recherche': '/affichCode.do?cidTexte=LEGITEXT000006071190',
 "Code des relations entre le public et l'administration": '/affichCode.do?cidTexte=LEGITEXT000031366350&idSectionTA=',
 'Code de la route': '/affichCode.do?cidTexte=LEGITEXT000006074228',
 'Code rural et de la pêche maritime': '/affichCode.do?cidTexte=LEGITEXT000006071367',
 'Code de la santé publique': '/affichCode.do?cidTexte=LEGITEXT000006072665',
 'Code de la sécurité intérieure': '/affichCode.do?cidTexte=LEGITEXT000025503132',
 'Code du sport': '/affichCode.do?cidTexte=LEGITEXT000006071318',
 'Code du tourisme': '/affichCode.do?cidTexte=LEGITEXT000006074073',
 'Code des transports': '/affichCode.do?cidTexte=LEGITEXT000023086525',
 'Code du travail': '/affichCode.do?cidTexte=LEGITEXT000006072050',
 "Code de l'urbanisme": '/affichCode.do?cidTexte=LEGITEXT000006074075',
 'Code de la voirie routière': '/affichCode.do?cidTexte=LEGITEXT000006070667',
 'Code general de la propriété des personnes publiques': '/affichCode.do?cidTexte=LEGITEXT000006070299', "Code de l'entrée et du séjour des étrangers et du droit d'asile": "/affichCode.do?cidTexte=LEGITEXT000006070158&dateTexte=20191011", "Code de l'expropriation pour cause d'utilité publique": "/affichCode.do?cidTexte=LEGITEXT000006074224&dateTexte=20191011", "Code minier": "/affichCode.do?cidTexte=LEGITEXT000006071785&dateTexte=20191011", "Code minier (nouveau)": "/affichCode.do?cidTexte=LEGITEXT000023501962&dateTexte=20191011", "Code de l'artisanat":"/affichCode.do?cidTexte=LEGITEXT000006075116&dateTexte=20191116", "Code des assurances": "/affichCode.do?cidTexte=LEGITEXT000006073984&dateTexte=20191116", "Code de la propriété intellectuelle": "/affichCode.do?cidTexte=LEGITEXT000006069414&dateTexte=20191116",
         "Code de la consommation (ancien)": "/affichCode.do?cidTexte=LEGITEXT000006069565&dateTexte=20091216"}

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


for code in codes:
    driver = webdriver.Chrome(executable_path=r"C:\Users\damie\PycharmProjects\Civil_Law\venv\chromedriver.exe")
    driver.get("https://www.legifrance.gouv.fr/" + codes[code])
    soup = BeautifulSoup(driver.page_source)
    set_articles = soup.find_all("a", text=re.compile("^Article"))
    for article in set_articles:
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
            driver.find_elements_by_xpath(".//button[@data-articleid='" + legiver + "']")[0].click()
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


for index, row in df.iterrows():
    if len(row["Text"]) > 20000:
        df.at[index, "Text"] = row["Text"][:20000]
    if len(row["cited"]) > 140:
        df.at[index, "cited"] = row["cited"][:140]
    if len(row["citing"]) > 140:
        df.at[index, "citing"] = row["citing"][:140]

df.to_csv("Data.csv", encoding="utf8")
