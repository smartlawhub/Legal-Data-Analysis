import spacy
import requests
from bs4 import BeautifulSoup
from bertopic import BERTopic  # We import the module
import pandas as pd
import plotly.io as pio  # This is another plot module in Python
pio.renderers.default = "browser"  # We set it up so that figure appears in a browser
import regex as re


# First, we get the dataset, which in this case are

url = "https://www.courdecassation.fr/recherche-judilibre?sort=date-desc&items_per_page=30&search_api_fulltext=&expression_exacte=&date_du=2016-12-01&date_au=2022-10-17&judilibre_chambre=&judilibre_type=&judilibre_publication=&judilibre_solution=&judilibre_juridiction=cc&judilibre_formation=&judilibre_zonage=&judilibre_doctype=&judilibre_siege_ca=&judilibre_nature_du_contentieux=&judilibre_type_ca=&op=Trier&page="
nlp = spacy.load('fr_core_news_md', disable=["tok2vec", "tagger", "parser", "attribute_ruler", "ner", "textcat"])

main_list = []
for x in range(1, 20):
    print(x)
    webpage = requests.get(url + str(x))
    soup = BeautifulSoup(webpage.content)
    aas = soup.find_all("div", class_="decision-item")
    for a in aas:
        href = a.find("a").get("href")
        sublist = [href]
        title = a.find("h3").text.split("-\n")
        formation = a.find("p", class_="decision-item-header--secondary").text.split("-")[0]
        solution = a.find("p", class_="decision-item-header--secondary solution").text
        for x in title + [formation, solution]:
            sublist.append(x.strip())

        webpage = requests.get("https://www.courdecassation.fr" + href)
        soup = BeautifulSoup(webpage.content)
        text = soup.find("div", class_="decision-content decision-content--main").getText()
        peuple = re.search("AU NOM DU PEUPLE", text)
        sublist.append(text[peuple.start():6000]) if peuple is not None else sublist.append(text[:5000])
        main_list.append(sublist)

cassdf = pd.DataFrame(main_list, columns=["URL", "Date", "Cour", "ID", "Formation", "Solution", "Text"])


def spacy_process(text):  # We first prepare the text by using spacy's token elements to remove stop words and punctuation
    doc = nlp(re.sub(r"\(\)", " ", text))   # We transform the text with spacy
    filtered_sentence = []   # Empty list for the tokens we'll want to keep
    punctuations = ["?",":","!",".",",",";","-", "(", ")", "[", "]"]  # A list of punctuation
    for token in doc:
        if token.is_stop is False and token.lemma_ not in punctuations and token.is_alpha:  # We append tokens to the list only if they are not a stop word or in our list of punctuations, and if the banned terms (which here includes any number) are out
            filtered_sentence.append(token.lemma_)

    return " ".join(filtered_sentence)

cassdf["CText"] = cassdf.Text.apply(spacy_process)

topic_model = BERTopic(embedding_model=nlp, n_gram_range=(1, 3), min_topic_size=3, nr_topics="auto")  # We set up the topic model
topics, probs = topic_model.fit_transform(cassdf.CText.values.tolist())
topic_model.get_topic_info()  # We visualise the top terms for each topics
cassdf["Topic"] = topics
cassdf.to_clipboard(index=False, encoding="utf8")

fig = topic_model.visualize_topics()
pio.show(fig)



##########################################################################################################################################
# CAS.5 python program
# Date: 05.11.2022
# By M.Tournier & D. Biddine
# Scope of the progrom: scrap the web site  jurispridence.tas-cas.org, in order to detrmine what is the most frequent sport in "Upheld" cases
##########################################################################################################################################
import requests
import re
import time
from bs4 import BeautifulSoup
# We use the pandas library for Dataframe
import pandas as pd
# We use the selenium library to find element in web page
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# Function to find most frequent element in a list

def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num, counter;

# Get the first page of the web site and find the "next" arrow at the bottom of the page

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://jurisprudence.tas-cas.org/Shared%20Documents/Forms/AllDecisions.aspx")  # Get the first page
page=1
el = driver.find_elements(By.XPATH, '//*[@id="bottomPagingCellWPQ2"]//a')[-1] # Find the "next" arrow, which is always the last <a> element under the element with that id
pages_visited = []  # A list to keep track of URLs visited, to make sure we don't enter an infinite loop


#Loops continue to execute the code as long as the condition is true, so as long as "el" is not None - but can therefore easily create an infinite loop, hence the break if we find an URL we already visited

SportList =[]
ll = []
while el:
    # Get the dataframe in page and process the data
    print ("--------------------")
    print ("page number : " + str (page))
    # We upload the "current URL into a dataframe
    dataframe = pd.read_html(driver.current_url)
    #print(dataframe)
    # We start from the second row - as the first contains the title of the columns
    my_list = dataframe[1]
    ll.append(my_list)
    #print(list)
    row=my_list.shape[0] #We need to get the number of row in the dataframe as it varies in some pages
    print ("row = " + str(row))

    # We create loop to go through all rows and in case of Upheld case we store the sport in a list
    for x in range(0, row):
        element = my_list.values[x]
        # We select from the element the data we need for our analysis: status, sport and appeallant name
        status = element[12]
        sport = element[8]
        name = element[6]
        # If the status = Upheld we store the sport name in a List
        if status == "Upheld":
            #Test if name is a person
            print ("Name is "+str(name))
            if re.search('Club', name): #We exclude names whre the String "club" appears
                    print('Club in name ' + str(name))
            else:
                    if re.search('[A-Z]{2}',name): #We exclude names where we find 2 consecutive Uppercase
                        print('double CAPS in name ' + str(name))
                    else:
                        (print('it is a person ' + str (name)))
                        SportList.append(sport)

    # Go to next page by clicking on the "next button" at bottom of page
    time.sleep(1) # Just to slow things down and make sure you can fetch every page
    el = driver.find_elements(By.XPATH, '//*[@id="bottomPagingCellWPQ2"]//a')[-1]
    el.click()
    if driver.current_url in pages_visited:  # We check that we have not already visited that URL
        break
    else:
        pages_visited.append(driver.current_url)
        page= page + 1

# Now that our  list is complete, we call the above function to determine the most frequent upheld sport
List = SportList
num, counter = most_frequent(List)
print ('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
print ('The most frequent upheld Sport is ', num)
print ('It is counted ', counter, ' times')
print ('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
