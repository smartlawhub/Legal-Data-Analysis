import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from time import sleep
from selenium.common.exceptions import NoSuchElementException


def extract_directive_info(parent_element): #define a function to scrap for celex number, looking at two positions
    try:
        celex_number_candidate1 = parent_element.find_element(By.XPATH, ".//div[1]/dl/dd[1]").text
        if re.match(r'3\d{4}L', celex_number_candidate1):
            celex_number = celex_number_candidate1
        else:
            celex_number_candidate2 = parent_element.find_element(By.XPATH, ".//div[1]/dl/dd[2]").text
            if re.match(r'3\d{4}L', celex_number_candidate2):
                celex_number = celex_number_candidate2
            else:
                celex_number = "N/A"
    except NoSuchElementException: #in case there is no celex, the code does not brake
        pass
    #we do the same for the publication date and subject
    try:
        publication_date = parent_element.find_element(By.XPATH, ".//div[2]/dl/dd[2]").text.split(";")[0]
    except NoSuchElementException:
        publication_date = "Unknown"
    
    subjects = ''
    try:
        subjects_elements = parent_element.find_elements(By.XPATH, ".//dl/dd[4]/ul/li/a") + parent_element.find_elements(By.XPATH, ".//dl/dd[5]/ul/li/a")
        subjects = ', '.join([elem.text for elem in subjects_elements]) #there are sometimes more than oen subject, separated by comma
    except NoSuchElementException:
        pass
    
    return celex_number, publication_date, subjects

service = Service(executable_path=GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)

# URL for directives, the code will append the page number
directive_base_url = "https://eur-lex.europa.eu/search.html?SUBDOM_INIT=ALL_ALL&DB_TYPE_OF_ACT=directive&DTS_SUBDOM=ALL_ALL&typeOfActStatus=DIRECTIVE%2COTHER&or0=DN%3D3*%2CDN-old%3D3*&type=advanced&date0=ALL%3A01022020%7C.&qid=1711414697566&DTC=false&orFM_CODEDGroup=FM_CODED%3DDIR&DTS_DOM=ALL&FM_CODED=&lang=fr&excConsLeg=true&page="

#URL for transposed acts, the code will append the page number
transposed_act_base_url = "https://eur-lex.europa.eu/search.html?SUBDOM_INIT=MNE&DTS_SUBDOM=MNE&sortOneOrder=desc&sortOne=IDENTIFIER_SORT&lang=en&type=advanced&qid=1711241216437&page="

# Scraping 
with open('directives.csv', 'w', newline='', encoding='utf-8') as directives_file, open('transposed_act.csv', 'w', newline='', encoding='utf-8') as transposed_file:
    directives_writer = csv.writer(directives_file)
    transposed_writer = csv.writer(transposed_file)
    directives_writer.writerow(['CELEX', 'Date', 'Subjects'])
    transposed_writer.writerow(['Transposed act', 'Country', 'Date', 'Date nature'])

    # Scraping directives
    page_number = 1
    while True:
        current_page_url = f"{directive_base_url}{page_number}"
        driver.get(current_page_url)
        sleep(5)  
        if page_number == 1:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "link-change-metadata_top"))).click() #click to personalize results
            sleep(2) #giving some time to load information
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "simple_c31classificationsCT"))).click() #click on the checkbox for subject
            sleep(2)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nbResultPerPage']"))).click()  #☻change the number of displayed result for 20 by page
            sleep(2)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/form[2]/fieldset/div[1]/div[1]/div/div[2]/select/option[3]"))).click()
            sleep(1)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button.apply"))).click() #click to apply changes
            sleep(5)
            driver.get(current_page_url)
            sleep(5)

        parent_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[starts-with(@id, 'MoreSR_')]")))
        if not parent_elements:
            print(f"End of pages or no data found at page {page_number} for directives.")
            break
        for parent in parent_elements:
            celex_number, publication_date, subjects = extract_directive_info(parent)
            directives_writer.writerow([celex_number, publication_date, subjects]) #allows to write in a new row of the csv, each element is in a column
            print(f"Directive CELEX: {celex_number}, Date: {publication_date}, Subjects: {subjects}")
        page_number += 1

    # Reset page number for transposed acts
    page_number = 1
    while True:
        current_page_url = f"{transposed_act_base_url}{page_number}"
        driver.get(current_page_url)
        sleep(2)
        
        if page_number == 1:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "link-change-metadata_top"))).click() #click to personalize results
                sleep(2) #giving some time to load information
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='nbResultPerPage']"))).click()  #☻change the number of displayed result for 20 by page
                sleep(2)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/form[2]/fieldset/div[1]/div[1]/div/div[2]/select/option[3]"))).click()
                sleep(1)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button.apply"))).click() #click to apply changes
                sleep(5)
                driver.get(current_page_url)
                sleep(5)
        parent_elements = driver.find_elements(By.XPATH, "//*[starts-with(@id, 'MoreSR')]")
        if not parent_elements:
            print(f"End of pages or no data found at page {page_number} for transposed acts.")
            break

        for parent in parent_elements:
            transposed_acts_elements = parent.find_elements(By.XPATH, ".//dl/dd[3]//a")
            country = parent.find_element(By.XPATH, ".//div[2]/dl/dd[1]").text.strip()
            date_text = parent.find_element(By.XPATH, ".//div[2]/dl/dd[2]").text.strip()
            date, date_nature = (date_text.split("; ") + [""])[:2] #scraping output gives date;nature of the date, so we split by the ; and get a list of two elements, we put additional "" in case the split gives only one element and [:2] to get only two elements in case there are more than one ; (or zero)

            if transposed_acts_elements:
                for act_element in transposed_acts_elements:
                    transposed_act = act_element.text.strip()
                    transposed_writer.writerow([transposed_act, country, date, date_nature])
                    print(f"Transposed act: {transposed_act}, Country: {country}, Date: {date}, Date nature: {date_nature}")
            else:
                transposed_writer.writerow(['N/A', country, date, date_nature])
                print(f"Transposed act: N/A, Country: {country}, Date: {date}, Date nature: {date_nature}")
        
        page_number += 1

driver.quit()
                                               
