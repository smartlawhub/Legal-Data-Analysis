import re
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from collections import Counter, defaultdict
import pandas as pd
import time

codes = {"Code de l'action sociale et des familles": '/codes/texte_lc/LEGITEXT000006074069?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'artisanat": '/codes/texte_lc/LEGITEXT000006075116?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des assurances': '/codes/texte_lc/LEGITEXT000006073984?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'aviation civile": '/codes/texte_lc/LEGITEXT000006074234?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code du cinéma et de l'image animée": '/codes/texte_lc/LEGITEXT000020908868?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code civil': '/codes/texte_lc/LEGITEXT000006070721?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la commande publique': '/codes/texte_lc/LEGITEXT000037701019?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de commerce': '/codes/texte_lc/LEGITEXT000005634379?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des communes': '/codes/texte_lc/LEGITEXT000006070162?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des communes de la Nouvelle-Calédonie': '/codes/texte_lc/LEGITEXT000006070300?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la consommation': '/codes/texte_lc/LEGITEXT000006069565?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de la construction et de l'habitation": '/codes/texte_lc/LEGITEXT000006074096?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la défense': '/codes/texte_lc/LEGITEXT000006071307?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de déontologie des architectes': '/codes/texte_lc/LEGITEXT000006074232?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code disciplinaire et pénal de la marine marchande': '/codes/texte_lc/LEGITEXT000006071188?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code du domaine de l'Etat": '/codes/texte_lc/LEGITEXT000006070208?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code du domaine de l'Etat et des collectivités publiques applicable à la collectivité territoriale de Mayotte": '/codes/texte_lc/LEGITEXT000006074235?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code du domaine public fluvial et de la navigation intérieure': '/codes/texte_lc/LEGITEXT000006074237?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des douanes': '/codes/texte_lc/LEGITEXT000006071570?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des douanes de Mayotte': '/codes/texte_lc/LEGITEXT000006071645?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'éducation": '/codes/texte_lc/LEGITEXT000006071191?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code électoral': '/codes/texte_lc/LEGITEXT000006070239?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'énergie": '/codes/texte_lc/LEGITEXT000023983208?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'entrée et du séjour des étrangers et du droit d'asile": '/codes/texte_lc/LEGITEXT000006070158?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'environnement": '/codes/texte_lc/LEGITEXT000006074220?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'expropriation pour cause d'utilité publique": '/codes/texte_lc/LEGITEXT000006074224?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de la famille et de l'aide sociale": '/codes/texte_lc/LEGITEXT000006072637?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code forestier (nouveau)': '/codes/texte_lc/LEGITEXT000025244092?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code général de la fonction publique': '/codes/texte_lc/LEGITEXT000044416551/2022-03-01?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code général de la propriété des personnes publiques': '/codes/texte_lc/LEGITEXT000006070299?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code général des collectivités territoriales': '/codes/texte_lc/LEGITEXT000006070633?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code général des impôts': '/codes/texte_lc/LEGITEXT000006069577?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code général des impôts, annexe 1': '/codes/texte_lc/LEGITEXT000006069568?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code général des impôts, annexe 2': '/codes/texte_lc/LEGITEXT000006069569?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code général des impôts, annexe 3': '/codes/texte_lc/LEGITEXT000006069574?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code général des impôts, annexe 4': '/codes/texte_lc/LEGITEXT000006069576?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des instruments monétaires et des médailles': '/codes/texte_lc/LEGITEXT000006070666?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des juridictions financières': '/codes/texte_lc/LEGITEXT000006070249?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de justice administrative': '/codes/texte_lc/LEGITEXT000006070933?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de justice militaire (nouveau)': '/codes/texte_lc/LEGITEXT000006071360?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la justice pénale des mineurs': '/codes/texte_lc/LEGITEXT000039086952?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de la Légion d'honneur, de la Médaille militaire et de l'ordre national du Mérite": '/codes/texte_lc/LEGITEXT000006071007?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Livre des procédures fiscales': '/codes/texte_lc/LEGITEXT000006069583?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code minier': '/codes/texte_lc/LEGITEXT000006071785?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code minier (nouveau)': '/codes/texte_lc/LEGITEXT000023501962?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code monétaire et financier': '/codes/texte_lc/LEGITEXT000006072026?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la mutualité': '/codes/texte_lc/LEGITEXT000006074067?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'organisation judiciaire": '/codes/texte_lc/LEGITEXT000006071164?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code du patrimoine': '/codes/texte_lc/LEGITEXT000006074236?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code pénal': '/codes/texte_lc/LEGITEXT000006070719?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des pensions civiles et militaires de retraite': '/codes/texte_lc/LEGITEXT000006070302?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des pensions de retraite des marins français du commerce, de pêche ou de plaisance': '/codes/texte_lc/LEGITEXT000006074066?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code des pensions militaires d'invalidité et des victimes de guerre": '/codes/texte_lc/LEGITEXT000006074068?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des ports maritimes': '/codes/texte_lc/LEGITEXT000006074233?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des postes et des communications électroniques': '/codes/texte_lc/LEGITEXT000006070987?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de procédure civile': '/codes/texte_lc/LEGITEXT000006070716?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de procédure pénale': '/codes/texte_lc/LEGITEXT000006071154?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code des procédures civiles d'exécution": '/codes/texte_lc/LEGITEXT000025024948?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la propriété intellectuelle': '/codes/texte_lc/LEGITEXT000006069414?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la recherche': '/codes/texte_lc/LEGITEXT000006071190?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code des relations entre le public et l'administration": '/codes/texte_lc/LEGITEXT000031366350?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la route': '/codes/texte_lc/LEGITEXT000006074228?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code rural (ancien)': '/codes/texte_lc/LEGITEXT000006071366?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code rural et de la pêche maritime': '/codes/texte_lc/LEGITEXT000006071367?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la santé publique': '/codes/texte_lc/LEGITEXT000006072665?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la sécurité intérieure': '/codes/texte_lc/LEGITEXT000025503132?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la sécurité sociale': '/codes/texte_lc/LEGITEXT000006073189?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code du service national': '/codes/texte_lc/LEGITEXT000006071335?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code du sport': '/codes/texte_lc/LEGITEXT000006071318?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code du tourisme': '/codes/texte_lc/LEGITEXT000006074073?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code des transports': '/codes/texte_lc/LEGITEXT000023086525?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code du travail': '/codes/texte_lc/LEGITEXT000006072050?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code du travail applicable à Mayotte': '/codes/texte_lc/LEGITEXT000006072052?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code du travail maritime': '/codes/texte_lc/LEGITEXT000006072051?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 "Code de l'urbanisme": '/codes/texte_lc/LEGITEXT000006074075?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF',
 'Code de la voirie routière': '/codes/texte_lc/LEGITEXT000006070667?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF'}  # A list of codes with their URLs; below we'll focus only on private law codes

data_scrapped = []  # The main list that will be filled with the data you'll scrap (put into their own lists, so that it becomes a list of list - i.e., a Dataframe)

codes_private_law = ['Code civil', 'Code de commerce', "Code de l'environnement", 'Code de la consommation', 'Code de la route', 'Code des transports', 'Code du sport', 'Code du tourisme', 'Code monétaire et financier',"Code de l'artisanat", 'Code des assurances', 'Code de la propriété intellectuelle', "Code minier (nouveau)", 'Code du travail']


def get_relative_links(relative_name):  # A functionto get links to cited and citing texts (the "Liens Relatifs" tab in any article page)
    list_links = []   # Empty list to collect relevant links
    ul = driver.find_element(By.XPATH, ".//*[contains(text(), '" + relative_name + "')]/../following-sibling::ul")  # Given the kind of links we are interested in (relative name), look for the element that contains this name, then move to the parent element, and check the siblings that are <ul> elements
    for li in ul.find_elements(By.XPATH, ".//li"):
        try:  # This is some exception handling: the find_element method will throw an error if you cannot find an "a" element in it, or "href" attribute, so you need to tell Python what to do if it gets an error
            href = li.find_element(By.XPATH, ".//a").get_attribute("href")  # Get the URL from the link being cited
        except:
            href = "No URL"
        list_links.append(li.text + " : " + href)  # What we are looking for: the text of the relative link, plus URL
    return list_links


for code in codes_private_law:  # I am iterating through all codes, but be sure to change that to a single one if you are only interested in one
    print(code)  # Print to keep track of what code is being parsed
    driver = webdriver.Chrome(executable_path=r"C:\Users\damie\PycharmProjects\Civil_Law\venv\chromedriver.exe")  # Open browser
    driver.get("https://www.legifrance.gouv.fr/" + codes[code])  # Get the specific law code we are interested, using the dict defined above
    soup = BeautifulSoup(driver.page_source)  # Read HTML, pass it to a soup object
    set_articles = soup.find_all("a", text=re.compile("^Article"))  # Find all articles in the code, by looking for all links whose text starts with Article
    for article in set_articles:  # Iterate over articles one by one
        legiarti = re.search("LEGIARTI.*?#", article.get("href")).group()[:-1]   # Each article has a single page that you can get to using the LEGIARTI code found in an article's URL
        driver.get("https://www.legifrance.gouv.fr/codes/article_lc/" + legiarti)  # Go to that URL
        driver.find_element(By.XPATH, ".//button[@data-articleid='" + legiarti + "']|.//button[@data-articlecid='" + legiarti + "']").click()   # Click on the "Versions" tab
        time.sleep(1)  # Wait a bit
        article_num = driver.find_element(By.CLASS_NAME, "name-article").text  # Look for the full name of the article, which is an element of class "name-article"
        version_urls = [x.get_attribute("href") for x in driver.find_elements(By.CLASS_NAME, "version")]  # A list comprehension to get all links to all versions of the article
        count_version = len(version_urls)  # A count for the versions
        for version_url in [x for x in version_urls if x is not None]:  # The list comprehension to make sure you are not stumbling on a fake or empty URL (which would be None)
            driver.get(version_url)  # go to the page for that article's version
            legiver = re.search("LEGIARTI.*?/", version_url).group()[:-1]  # Find the LEGIARTI Code for that version
            driver.find_element(By.XPATH, ".//button[@data-articleid='" + legiver + "']|.//button[@data-num='" + article_num.split(" ")[-1] + "']").click()  # Try to open the "Versions" tab; there are two xPath searches here (separated by |), as sometimes button does not track the correct LegiArti
            try:  # Another exception handler, to try to get the date of origin of the article; errors sometimes occur because page does not have that field
                origin = driver.find_element(By.CLASS_NAME, "date").text
            except:
                origin = ""
            article_text = driver.find_elements(By.CLASS_NAME, "content")[2].text  # The content of the article, we know from the inspector that this is the third element of class "content"
            temp_list = [code, article_num, driver.current_url, version_url.split("/")[-2], count_version, article_text, origin, "", "", "", ""]  # We create our first list with all data collected so far, put some placeholders for types of citations
            if len(driver.find_elements(By.XPATH, ".//button[@data-articleid='" + legiver + "']")) > 1:  # Looking for the "Liens Relatifs" tab, by counting number of tabs; if more than 1 (the "Versions" tab), then there is a "Lien Relatifs" tab
                driver.find_elements(By.XPATH, ".//button[@data-articleid='" + legiver + "']")[1].click()  # We then click on it
                time.sleep(1)  # And wait a bit
            relatives = driver.find_elements(By.XPATH, ".//h5")  # We know that titles for types of citations are in h5 elements, so we collect them all
            for relation in relatives:  # Then we loop over these titles
                spl = re.sub("<.*?>", "", relation.get_attribute("innerHTML"))  # We get the name of the title from the html (sometimes .text doesn't work)
                if re.search("Cit. par", spl):  # And then we assign responsive data to their correct place in the temporary list depending on type, using the function defined above
                    temp_list[-4] = get_relative_links(spl)
                elif re.search("Cite", spl):
                    temp_list[-3] = get_relative_links(spl)
                elif re.search("^Nouveaux", spl):
                    temp_list[-2] = get_relative_links(spl)
                elif re.search("^Anciens", spl):
                    temp_list[-1] = get_relative_links(spl)

            count_version -= 1  # Every time we finished collecting data from a version, we remove 1 from counter (so that version 0 will be the last in the list, i.e., the oldest
            data_scrapped.append(temp_list)  # final step is to add the temporary list to big list, to create a list of lists
    driver.close()

df = pd.DataFrame(data_scrapped, columns=["Code", "Art", "URL", "Date", "version", "Text", "Created", "Cited_by", "Cite_to", "New", "Old"])
df.to_csv("YourCSVName.csv", encoding="utf8")
