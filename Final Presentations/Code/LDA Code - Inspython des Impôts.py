import pandas as pd
import regex as re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


CREATE_CSV = False

if __name__ == '__main__':
    if CREATE_CSV:
        # Setup du driver et initialisation : 
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("https://www.conseil-etat.fr/arianeweb/#/recherche")

        # Application des paramètres de recherche : 
        el = driver.find_element(By.XPATH, r'.//*[contains(text(), "Décisions du Conseil")]')
        el.click()

        el2 = driver.find_element(By.XPATH, r'.//*[@ng-model="search.currentSearch.query"]')
        el2.click()
        el2.send_keys("vérification de comptabilité")

        # Lancement de la recherche : 
        button = driver.find_element(By.XPATH, ".//button[@class='btn btn-primary']")
        button.click()

        # ----------------------- Récupération des données trouvées -----------------------------------------------

        # Définition du dataframe qui va contenir les résultats : 
        declarations_df = pd.DataFrame()

        # Des xpaths réutilisés plusieurs fois : 
        next_page = "//table/tbody/tr[2]/td[1]/div[2]/ul/li/a[@ng-click='selectPage(page + 1)']"
        next_page_disabled = "//table/tbody/tr[2]/td[1]/div[2]/ul/li[@class='ng-scope disabled']"


        # Fonction qui, pour chaque page du tableau de résultat extrait les lignes, ouvre le document associé et essaye de récupérer la CAA et la décision prise :
        # Vu que le tableau affiche 50 résultats par page sur Ariane, cete fonction ajoute à chaque fois 50 lignes au dataframe de résultats, declarations_df. 

        def compute_and_append_page_results_to_df(df):
        
            # Récupération des déclarations du tableau principal : 
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, next_page)))
            declarations = driver.find_element(By.XPATH, '(//table)[2]').get_attribute('outerHTML')
            soup = BeautifulSoup(declarations, 'html.parser')

            # Liste des colonnes: ['id', 'Fonds', 'Juridiction', 'Formation de jugement', 'Date de lecture', "Numéro d'affaire", 'Code de publication']
            columns = [th.getText().rstrip(' ') for th in soup.find_all('th')]  # Colonnes du tableau de résultat
            columns[0] = 'id'
            columns.extend(['Cour', 'Décision'])

            # Page de départ du driver
            main_window = driver.current_window_handle

            # Rows est une liste qui va contenir tous les résultats trouvés, construite par la boucle suivante : 
            rows = []
            for tr in soup.find_all('tr', {"ng-repeat-start": 'result in results'}):  # Pour chaque ligne du tableau
                # La ligne suivante lis le contenu de la ligne du tableau : 
                row_soup = BeautifulSoup(''.join(str(el) for el in tr.contents), features='lxml')

                # Pour chaque ligne on fait une liste qui va contenir les éléments des colonnes : 
                row = []
                for td in row_soup.find_all('td', {'ng-repeat': 'field in result'}):  # Pour chaque élément de la ligne : 
                    row.append(td.getText())

                # On ouvre la fenêtre qui contient les documents associés aux lignes juste pour le premier résultat : 
                if row[0] == '1':
                    id_element = driver.find_element(By.XPATH, "(//table)[2]/tbody/tr/td[text()=" + row[0] + "]")
                    id_element.click()
                    time.sleep(5)
                    # Le click du dessus fait pop une nouvelle fenêtre avec le document associé
                    driver.switch_to.window(driver.window_handles[1])
                    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))
                else:  # Sinon la popup est déjà ouverte, on passe au doc d'après
                    driver.switch_to.window(driver.window_handles[1])
                    driver.find_element(
                        By.XPATH,
                        "//button[@title='document suivant']"
                    ).click()
                    time.sleep(0.1)
                    driver.switch_to.frame(driver.find_element(By.XPATH, '//iframe'))

                # Extraction des infos importantes : 

                # Premièrement, on essaye de récupérer la CAA, qu'on va garder dans la variable : 
                doc_source = driver.page_source.replace('\n', '')
                caa_re = re.compile(r".*cour administrative d'appel (de |d')(?P<caa>\w+).*")  # Regex de base
                cours_des_comptes_re = re.compile(r'.*(?P<cdc>(C|c)our des (C|c)omptes).*')  # Regex cour des comptes
                caa = caa_re.match(doc_source)
                cours_des_comptes = cours_des_comptes_re.match(doc_source)
                cour = ''
                if caa:  # On a trouvé une cour administrative d'appel
                    cour = caa.group('caa')
                elif cours_des_comptes:  # Trouvé cour des comptes
                    cour = cours_des_comptes.group('cdc')
                else:  # On a rien trouvé
                    cour = None

                # On fait la même chose pour les décisions : 
                doc_source_rows = driver.page_source.split('\n')  # On fait du document une liste de lignes
                decision_re = re.compile(r"(?i)^.*article 1er\s*[:\-;].*\s(?P<decision>(annul(é|e)|rejet(é|e))e?s?).*$")
                decision = ''

                for doc_source_row in doc_source_rows:  # On veut trouver un match en essayant ligne par ligne
                    decision = decision_re.match(doc_source_row)
                    if decision:
                        decision = decision.group('decision')
                        if decision.startswith(('A', 'a')): 
                            decision = 'annulé' 
                        else:
                            decision = 'rejeté'
                        break  # On a trouvé une décision, on sort de la boucle
                    else:
                        decision = None

                # Ajout des résultats trouvés à la ligne : 
                row.append(cour)
                row.append(decision)

                # Ajout de la ligne au dataframe : 
                rows.append(row)
                
            # Retour à la fenêtre d'ariane avec le tableau de résultats : 
            driver.switch_to.window(main_window)

            # Ajout des nouvelles lignes au dataframe : 
            df = pd.concat((df, pd.DataFrame(data=rows, columns=columns)), ignore_index=True)
            return df
            declarations_df = compute_and_append_page_results_to_df(declarations_df)

        # Passage à la page d'après : 
        element = driver.find_element(By.XPATH, next_page)
        driver.execute_script("arguments[0].click();", element)
        time.sleep(0.5) 

        # On crée ensuite une boucle sur toutes les autres pages sauf la dernière, qui s'arrête quand le bouton pour passer à la prochaine page n'est plus cliquable
        while not driver.find_elements(By.XPATH, next_page_disabled):
            declarations_df = compute_and_append_page_results_to_df(declarations_df)
            element = driver.find_element(By.XPATH, next_page)
            driver.execute_script("arguments[0].click();", element)
            time.sleep(0.5)

        # Ajout des résultats de la dernière page : 
        declarations_df = compute_and_append_page_results_to_df(declarations_df)

        # --------------------------------------------------------------------------------------------------------------

        # Export en csv : 
        declarations_df.to_csv('results.csv', index=False)

        # --------------------------Fin de la création du CSV-----------------------------------------------------------

    # Chargement du dataframe :
    declarations_df = pd.read_csv('results.csv', index_col=0)

    # Analyse : 
    df_of_interest = declarations_df[['Formation de jugement', 'Date de lecture', "Numéro d'affaire", 'Code de publication', 'Cour', 'Décision']]
    df_of_interest['Date de lecture'] = pd.to_datetime(df_of_interest['Date de lecture'], format="%d/%m/%Y")

   
