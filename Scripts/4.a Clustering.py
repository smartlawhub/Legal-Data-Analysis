from sklearn.cluster import KMeans, DBSCAN  # clustering algorithms
from sklearn.decomposition import TruncatedSVD  # dimensionality reduction
from sklearn.metrics import silhouette_score  # used as a metric to evaluate the cohesion in a cluster
from sklearn.neighbors import NearestNeighbors  # for selecting the optimal eps value when using DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
# plotting libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import regex as re
import spacy

nlp = spacy.load('en_core_web_md', disable=["tok2vec", "tagger", "parser", "attribute_ruler", "ner", "textcat"])


def spacy_process(text):  # We first prepare the text by using spacy's token elements to remove stop words and punctuation
    doc = nlp(re.sub("\(\)", " ", text))   # We transform the text with spacy
    filtered_sentence = []   # Empty list for the tokens we'll want to keep
    punctuations = ["?",":","!",".",",",";","-", "(", ")", "[", "]"]  # A list of punctuation
    banned_words = ["ARTICLE", "CODE", "\d+"]  # A list of words we are not interested in, because they are very frequent
    for token in doc:
        if token.is_stop is False and token.lemma_ not in punctuations and re.search("|".join(banned_words), token.text.upper()) is None:  # We append tokens to the list only if they are not a stop word or in our list of punctuations, and if the banned terms (which here includes any number) are out
            filtered_sentence.append(token.lemma_)

    return " ".join(filtered_sentence)


df = pd.read_csv("BIT Data.csv", header="infer", encoding="utf8")  # We open the file
df = df.fillna("")  # We fill empty values with an empty string, easier to check

newdf = []  # We first need to create the dataset, given that in BIT Data.csv, each line is an entire treaty, yet we need to work on a dataset that is one clause per line
for index, row in df[:500].iterrows():
    for x in range(1,11):  # Focusing only on the first ten clauses, but of course we could do it over the whole dataset (some treaties have 54 clauses)
        sublist = row.values.tolist()[:4]  # We initiate a list that keeps the basic value of the treaty: name, party 1, party 2, date
        if row["Article " + str(x)].strip() != "":  # We check that the cell is not empty
            sublist.append(row["Article " + str(x)].strip())  # We append the full article to compare ...
            sublist.append(spacy_process(row["Article " + str(x)]))  # ... with the processed text
            newdf.append(sublist)
        else:
            break

newdf = pd.DataFrame(newdf, columns=["Treaty", "Country 1", "Country 2", "Date", "Text", "CText"])


tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1,3), max_features=250, min_df=10)  # We initialise the tf-idf  algorithms, asking it to keep ngrams (compound words) into account (max 3), to keep only the 250 most important words (max_features), and only if these words are present in at least 10 entries (min_df)
df_tfidf = tfidf.fit_transform(newdf["CText"])

svd = TruncatedSVD(n_components=10, random_state=42)  # This creates a very big matrix, so we'll reduce it to 10 dimensions with the Truncated SVD algorithm
df_svd = svd.fit_transform(df_tfidf)

kmeans = KMeans(n_clusters=20, init="k-means++", random_state=42)  # k-means initialised to look for 20 clusters; random_state is a "seed", to reproduce the results later
clause_label = kmeans.fit_predict(df_svd)  # This returns a list of label in the same order as the data you gave it
newdf["cluster"] = clause_label  # We then assign this list of labels to our original dataset

newdf.to_clipboard()  # We can them have a look at the clusters in an excel spreadsheet

Kcolor_palette = sns.color_palette('hls', clause_label.max() + 1)  # We initialise a palette of colors based on the number of labels
Kcluster_colors = [Kcolor_palette[x] for x in clause_label]  # And then a list of colors for each label
plt.scatter(df_svd[:,0], df_svd[:,1], c=Kcluster_colors)  # We create the scatter plot, based on the (x, y) location of each data point, and the list of colors (which represent labels) - note that this are only two dimensions of the 10 in df_svd, but it works ok

Markers = ["$" + str(x) + "$" for x in range(0, clause_label.max() + 1)]  # We take the labels and create markers for our plot
for e, i in enumerate(kmeans.cluster_centers_):  # For each centroid, we take the first dimension (x) and second (y) to plot it, in line with the relevant marker
    plt.scatter([i[0]], [i[1]],  marker=Markers[e], s=169, linewidths=3, color='black', zorder=8)