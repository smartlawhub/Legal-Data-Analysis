import spacy
import requests
from bs4 import BeautifulSoup
from bertopic import BERTopic  # We import the module
import pandas as pd
import plotly.io as pio  # This is another plot module in Python
pio.renderers.default = "browser"  # We set it up so that figure appears in a browser
import regex as re
from collections import defaultdict


# First, we get the dataset, which in this case are

url = "https://www.courdecassation.fr/recherche-judilibre?sort=date-desc&items_per_page=30&search_api_fulltext=&expression_exacte=&date_du=2016-12-01&date_au=2022-10-17&judilibre_chambre=&judilibre_type=&judilibre_publication=&judilibre_solution=&judilibre_juridiction=cc&judilibre_formation=&judilibre_zonage=&judilibre_doctype=&judilibre_siege_ca=&judilibre_nature_du_contentieux=&judilibre_type_ca=&op=Trier&page="
nlp = spacy.load('fr_core_news_md', disable=["tok2vec", "tagger", "parser", "attribute_ruler", "ner", "textcat"])

main_list = []
dds = []  # a container for the defaultdicts from the decisions
types = [] # keeping track of all categories of text in the database
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

        dd = defaultdict(str)
        current_type = ""
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