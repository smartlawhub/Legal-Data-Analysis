import os
import pandas as pd
import regex as re
import pandas
import spacy
from collections import Counter
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


nlp = spacy.load("fr_core_news_md", disable=["ner", "textcat"])  # We download spacy in a nlp object; the disable function is for efficiency purposes (some bits of Spacy are slow and useless for our purposes). Models need to be downloaded from the terminal

# 1

df = pd.read_csv("./Data/CSVs/Code civil versions.csv", header="infer")  # Working with a dataset of versions of the Code civil since 1804

text = "\n".join(df.loc[df.version == 1]["Text"].values.tolist())
doc = nlp(text)
words_doc = [tok.text for tok in doc if tok.is_alpha and not tok.is_punct]
CW = Counter(words_doc)
plt.figure(figsize=(20,20))  #to increase the plot resolution
plt.ylabel("Frequency")
plt.xlabel("Words")
plt.xticks(rotation=90)    #to rotate x-axis values
for word , freq in CW.most_common(30):
    plt.bar(word, freq)
plt.show()

# Now Benford's law

numbers = re.findall("[1-9](?=\d|\-|$)", "".join(df.Art.values.tolist()))
CC = Counter(numbers)
plt.figure(figsize=(20,20))  #to increase the plot resolution
plt.ylabel("Frequency")
plt.xlabel("Number")
plt.xticks(rotation=90)    #to rotate x-axis values

for key, value in CC.most_common(9):
    plt.bar(key, value)
plt.show()

# 5

roi = nlp("roi")

def close_words_from_vector(vec):  # A function I found online that returns the 10 most similar words compared to "vec"
    ms = nlp.vocab.vectors.most_similar(np.array([vec]), n=10)
    return [nlp.vocab.strings[w] for w in ms[0][0]]

close_words_from_vector(roi.vector)

analogie = nlp("roi").vector - nlp("homme").vector + nlp("femme").vector  # We find the vector that corresponds to roi, minus homme, plus femme
print(close_words_from_vector(analogie))  # Works only with large model

# 6

# We create two variables representing famous articles from the Code civil
article_1382 = "Tout fait quelconque de l'homme, qui cause à autrui un dommage, oblige celui par la faute duquel il est arrivé à le réparer."
article_1383 = "On est responsable non seulement du dommage que l'on cause par son propre fait, mais encore de celui qui est causé par le fait des personnes dont on doit répondre, ou des choses que l'on a sous sa garde. Toutefois, celui qui détient, à un titre quelconque, tout ou partie de l'immeuble ou des biens mobiliers dans lesquels un incendie a pris naissance ne sera responsable, vis-à-vis des tiers, des dommages causés par cet incendie que s'il est prouvé qu'il doit être attribué à sa faute ou à la faute des personnes dont il est responsable. Cette disposition ne s'applique pas aux rapports entre propriétaires et locataires, qui demeurent régis par les articles 1733 et 1734 du code civil. Le père et la mère, en tant qu'ils exercent l'autorité parentale, sont solidairement responsables du dommage causé par leurs enfants mineurs habitant avec eux. Les maîtres et les commettants, du dommage causé par leurs domestiques et préposés dans les fonctions auxquelles ils les ont employés ; Les instituteurs et les artisans, du dommage causé par leurs élèves et apprentis pendant le temps qu'ils sont sous leur surveillance. La responsabilité ci-dessus a lieu, à moins que les père et mère et les artisans ne prouvent qu'ils n'ont pu empêcher le fait qui donne lieu à cette responsabilité.En ce qui concerne les instituteurs, les fautes, imprudences ou négligences invoquées contre eux comme ayant causé le fait dommageable, devront être prouvées, conformément au droit commun, par le demandeur, à l'instance."

doc = nlp(article_1382)  # We transform the text in a spacy object
for tok in doc:  # Iterating through each token in the text
    if tok.is_stop is False and tok.is_punct is False:  # We check that the token is not a "stop word", and is not pure punctuation
        print(tok, tok.lemma_, tok.dep_, tok.pos_)  # In that case, we print the token text, its lemma, its place in text, etc
    else:
        print(tok.text)  # Otherwise we just print the text

doc2 = nlp(article_1383)  # This article has several sentences, so we can use Spacy to split them; each sentence become a full list of tokens, but keeps attributes from full text (like when does it start)
for sent in doc2.sents:
    print(sent, sent.start)  # We print each sentence
    verbs = []
    for tok in sent:  # For each sentence, we go token by token
        if tok.pos_ == "VERB":  # We check if that token is a subject, and then we print it
            verbs.append(tok.text + "=" + tok.lemma_)
    print("VERBS: ", verbs)

    nouns = []
    for chunk in sent.noun_chunks:  # We print the groupe nominaux
        nouns.append(chunk)
    print("NAME GROUPS: ", nouns)

# 7

df = pd.read_csv("Code civil versions.csv", header="infer", encoding="utf8")  # We load again the dataset
df.index = pd.to_datetime(df.Date)  # Change the index to the date of the article, so as to do time series


def spacy_process(text):  # We first prepare the text by using spacy's token elements to remove stop words and punctuation
    doc = nlp(text)   # We transform the text with spacy
    filtered_sentence = []   # Empty list for the tokens we'll want to keep
    punctuations = ["?",":","!",".",",",";","-", "(",")"]  # A list of punctuation
    banned_words = ["ARTICLE", "CODE"]  # A list of words we are not interested in, because they are very frequent
    for token in doc:
        if token.is_stop is False and token.lemma_ not in punctuations and token.text.upper() not in banned_words:  # We append tokens to the list only if they are not a stop word or in our list of punctuations
            filtered_sentence.append(token.lemma_)

    return " ".join(filtered_sentence)


df["CText"] = df.Text.map(lambda x: spacy_process(x))  # We apply it to our dataframe, so as to have a new column with cleaned text, rid of stop words and punctuations


def get_code_by_date(db, end):  # The idea is to sort by version (higher number > newer text) as the dictionary will take the last result
    data = []
    tempdict = db[:end].set_index("Art").sort_values(by="version", ascending=True).to_dict()["version"]
    for index, row in db[:end].iterrows():
        if row.Art in tempdict and row["version"] == tempdict[row["Art"]]:
            data.append(row.values)
    return pd.DataFrame(data, columns=db.columns)

fig, ax = plt.subplots(2,2)  # We initialise a set of subplots
fig.suptitle('Most common words for given years of Code civil')  # Which we entitle
for e, year in enumerate(["1805", "1950", "2000", "2021"]):  # A selection of years
    print(year)
    ax.ravel()[e].set_title("Most Common - " + year)
    aggregate_counter = Counter()  # We initialise a counter object (which counts stuff and allows you to get the most common items
    db = get_code_by_date(df, year)  # We get our limited code civil updated by date
    for index, row in db.iterrows():   # We iterate over every article
        c = Counter(row['CText'].split())   # Split into words, and count them
        aggregate_counter += c  # And then them to the main counter

    common_words = []
    common_words_counts = []
    for el in aggregate_counter.most_common(25):  # For the 25 most common items in our counter, we print the name of the item (at index 0), and the count (at index 1)
        print(el[0], el[1])
        common_words.append(el[0])  # We also add this data to lists that will be used to create a plot
        common_words_counts.append(el[1])

    bar_plt = sns.barplot(ax=ax.ravel()[e], x = common_words, y = common_words_counts)  # We then create a bar plot with seaborn, this takes two inputs: the names of the words, and a count

    for item in bar_plt.get_xticklabels():
        item.set_rotation(45)
        if item._text in ["héritier", "créancier", "propriétaire"] :
            item.set_fontweight("bold")

plt.show()

# And now for something more complicated...


def get_sents(db):  # First we cut articles in sentences. Note that this could also be done using NLP, but I don't find the performance better in this case
    data = []
    ii = 0
    prev = ""
    for index, art in db.iterrows():
        sents = re.split(r"\.\n|\. (?=[A-Z])", art.Text)
        for sent in sents:
            ii = ii + 1 if art["ID"] == prev else 0
            l = [art["Code"], art["Art"], art["ID"], art["ID"] + "_" + str(ii), art["Date"], sent + ".", len(sent)]
            data.append(l)
            prev = art["ID"]
    return pd.DataFrame(data, columns=["Code", "Art", "ID", "Al", "origin_date", "Text", "lenText"])


def get_subj(doc):
    pastsub = ""
    real_subj = "NoSubj"  # We initialise a variable with subject; it will return "NoSubj" if there aren't any subject
    for subj in [x for x in doc if "nsubj" in x.dep_]:  # We iterate through all possible subjects in the sentence
        real_subj = subj
        if subj.pos_ == "PRON":  # If this is a pronoun, however, we say that the pronoum is the previous subject
            real_subj = pastsub
        else:
            pastsub = subj
    if type(real_subj) == spacy.tokens.token.Token:  # Added to provide full noun chunk
        chunks = [x for x in doc.noun_chunks if real_subj in x]
        full_subj = chunks[0] if len(chunks) == 1 else real_subj.lemma_
    else:
        full_subj = ''
    return [real_subj, full_subj]

# Same code as above, but focusing on subjects per sentence thanks to the functions above
fig, ax = plt.subplots(2, 2)
fig.suptitle('Most common subjects for given years of Code civil')
for e, year in enumerate(["1805", "1950", "2000", "2021"]):  # A selection of years
    print(year)
    ax.ravel()[e].set_title("Most Common Subject - " + year)
    aggregate_counter = Counter()  # We initialise a counter object (which counts stuff and allows you to get the most common items
    db = get_code_by_date(df, year)  # We get our limited code civil updated by date
    db = get_sents(db)
    db["Subj"] = ""
    for index, row in db.iterrows():
        doc = nlp(row["Text"])
        db.at[index, "Subj"] = get_subj(doc)[0]
    bar_plt f= sns.barplot(ax=ax.ravel()[e], x=db.Subj.astype(str).value_counts()[1:20].index,y=db.Subj.astype(str).value_counts()[1:20].values)  # We then create a bar plot with seaborn, this takes two inputs: the names of the words, and a count
    for item in bar_plt.get_xticklabels():
        item.set_rotation(45)
