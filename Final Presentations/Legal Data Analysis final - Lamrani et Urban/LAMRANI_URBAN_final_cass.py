import spacy
import requests
from bs4 import BeautifulSoup
from bertopic import BERTopic  # We import the module
import pandas as pd
import plotly.io as pio  # This is another plot module in Python
pio.renderers.default = "browser"  # We set it up so that figure appears in a browser
import regex as re
from collections import defaultdict
import time
import locale
from matplotlib import pyplot as plt
from collections import Counter
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud



#=========================================================================================================================================
#                                      SCRAPPING THE COUR DE CASSATION 
#=========================================================================================================================================

url = "https://www.courdecassation.fr/recherche-judilibre?search_api_fulltext=ivresse&op=Rechercher"
nlp = spacy.load('fr_core_news_md', disable=["tok2vec", "tagger", "parser", "attribute_ruler", "ner", "textcat"])

main_list = []
dds = []  # a container for the defaultdicts from the decisions
types = [] # keeping track of all categories of text in the database

webpage = requests.get(url) # we connect on the page with docs urls, page by page
soup = BeautifulSoup(webpage.content)

for i in range(79): # we iterate through all the pages 
    print(i)
    if i != 0:
        new_url = "https://www.courdecassation.fr/recherche-judilibre?search_api_fulltext=ivresse&op=Rechercher&page=" + str(i)
        webpage = requests.get(new_url)
        soup = BeautifulSoup(webpage.content)

    decisions = soup.find_all("div", class_="decision-item")  # And we find the list of docs urls

    for d in decisions:
        # Add link 
        lien = d.find("a").get("href")
        sublist = [lien]
        
        # Add title 
        title = d.find("h3").text.split("-\n")  # We split to obtain the relevant subelements in the title
            
        formation = d.find("p", class_="decision-item-header--secondary").text.split("-")[0]
        solution = d.find("p", class_="decision-item-header--secondary solution").text

        for x in title + [formation, solution]:   # And we add all this to our sublist
            sublist.append(x.strip())

        # Navigate to every decision
        webpage = requests.get("https://www.courdecassation.fr" + lien)  
        
        soup = BeautifulSoup(webpage.content)
        textt = soup.find("div", class_="decision-content decision-content--main")
        
        text = soup.find("div", class_="decision-content decision-content--main").getText() # To fetch the text of the decision
        
        peuple = re.search("AU NOM DU PEUPLE", text)  # Cutting if text is too long, and we prefer to cut the entête rather than the text
        
        sublist.append(text[peuple.start():6000]) if peuple is not None else sublist.append(text[:5000])  # A 5000 max length is legit
        
        main_list.append(sublist)  # Adding to main_list, which is thus a list of lists, with each sublist corresponding to a case

        dd = defaultdict(str)  # We create a defaultdict to make sure that new entries will be an empty string
        current_type = "" # variable to keep track of the header
        
        for el in soup.find_all(["h3", "p"]):
            if el.name == "h3" and el.find("button") is not None:
                current_type = el.find("button").getText().strip()
                if current_type not in types:
                    types.append(current_type)
            elif el.name == "p" and "id" in el.attrs:  # We make sure this is a "p" element, as some h3 elements without button subels should not be taken into account
                dd[current_type] += el.getText().strip() + "\n-----\n"
        dds.append(dd)
        

for e, d in enumerate(dds):
    for tt in types:
        data = d[tt]
        main_list[e].append(data[:5000])

cassdf = pd.DataFrame(main_list, columns=["URL", "Date", "Cour", "ID", "Formation", "Solution", "Text"] + types)


print(cassdf["Text"].head())
#============================================================================================================
#                                              TOPIC MODELLING
#============================================================================================================

# STEP 1 : process text using spacy 

def spacy_process(text):  # We first prepare the text by using spacy's token elements to remove stop words and punctuation
    doc = nlp(re.sub(r"\(\)", " ", text))   # We transform the text with spacy
   
    filtered_sentence = []   # Empty list for the tokens we'll want to keep
    
    punctuations = ["?",":","!",".",",",";","-", "(", ")", "[", "]"]  # A list of punctuation
    banned_words = [ "publique", "palais", "justice", "base", "légale", "état", "ivresse", "alcoolique","avocat", "général", "peuple", "français", "débats", "article", "audience", "chambre", "conseiller", "cour", "président", "cour cassation", "arrêt", "code", "procédure", "juridiction", "moyen", "pourvoi", "cassation", "appel", "arret"]
    
    for token in doc:
        
        if token.is_stop is False and token.lemma_ not in punctuations and token.is_alpha and token.text.lower() not in banned_words:  # We append tokens to the list only if they are not a stop word or in our list of punctuations, and if the banned terms (which here includes any number) are out
            filtered_sentence.append(token.lemma_)

    return " ".join(filtered_sentence)


# Apply the function to the text and store in newly created column CText


cassdf["CText"] = cassdf.Text.apply(spacy_process)


# STEP 2 : visualize term frequency with word cloud 

long_string = ','.join(list(cassdf["CText"].values))
print(long_string)
wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='blue').generate(long_string) 

plt.imshow(wordcloud, interpolation = "bilinear")
plt.axis("off")
plt.show()


# STEP 3 : topic modeling with LDA. Source : https://medium.com/analytics-vidhya/modeling-with-latent-dirichlet-allocation-3b198f1a7bae
def lda_topic_model(cassdf):
    
    count = CountVectorizer(max_df=.1, max_features=5000)
    X = count.fit_transform(cassdf["CText"].values)

    lda = LatentDirichletAllocation(n_components=10,random_state=123, learning_method= "batch")
    X_topics = lda.fit_transform(X)

    n_top_words = 5
    feature_names = count.get_feature_names()
    
    for topic_idx, topic in enumerate(lda.components_):
        print("Topic %d:" % (topic_idx + 1))
        print(" ".join([feature_names[i]
        for i in topic.argsort()
            [:-n_top_words - 1:-1]]))


lda_topic_model(cassdf) # call the lda function


# STEP 4 : topic modeling with BERT. Source : class GitHub
def bert_topic_model(cassdf):

    topic_model = BERTopic(embedding_model=nlp, n_gram_range=(1, 3), min_topic_size=3, nr_topics="auto")  # We set up the topic model
    time.sleep(4)
    topics, probs = topic_model.fit_transform(cassdf.CText.values.tolist())

    topic_model.get_topic_info()  # We visualise the top terms for each topics
    cassdf["Topic"] = topics
    cassdf.to_clipboard(index=False, encoding="utf8")

    fig = topic_model.visualize_topics()
    pio.show(fig)


bert_topic_model(cassdf) # call the bert function 
