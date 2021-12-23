import regex as re
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt


cc = pd.read_csv("Data.csv", header="infer", encoding="latin1")
cc = cc.loc[cc.Code == "Code civil"]

nodes = set(cc.Art.values.tolist())  # Potential nodes are all articles we know exist. This will also be helpful to chekh that citations are genuine
edges = set()  # This will take a tuple, as NetworkX needs that kind of input - though we could also create a df

count_article = 0

for index, row in cc.iterrows():  #We iterate over all articles
    text = row["Text"]
    sea = re.search(r"Article (?<num>[\d-]+) (?!de la loi)", text, re.S|re.I)  # Basic Search
    seas1 = re.search(r"Articles ([\d-]+[et, ]*)+", text, re.S|re.I)  # For list of articles
    seas2 = re.search(r"Articles (?<lower>[\d-]+) à (?<upper>[\d-]+)", text, re.S|re.I)  # For ranges of articles
    prec = re.search(r"articles? précédent", text, re.S|re.I)  # Relative Links
    suiv = re.search(r"articles? suivant", text, re.S|re.I) # Relative Links

    if sea:
        count_article += 1  # We count all times when an article is found, even when it's not from the Code civil
        if "Article " + sea.group("num") in nodes:
            edges.add((row["Art"], "Article " + sea.group("num")))

    if seas1:
        count_article += 1
        for num in re.findall("[\d-]+", text):
            if "Article " + num in nodes:
                edges.add((row["Art"], "Article " + num))

    if seas2:  # In the context of a range, two methods: we could transform the numbers in integers and add to them; or we can just leverage the existing dataset
        count_article += 1
        if "Article " + seas2.group("lower") in nodes and "Article " + seas2.group("upper") in nodes:
            lower_index = cc.loc[cc.Art == "Article " + seas2.group("lower")].index[0]
            upper_index = cc.loc[cc.Art == "Article " + seas2.group("upper")].index[0] + 1  # Don't forget that the upper range is not included in pandas indexing
            for val in cc[lower_index:upper_index].Art.values.tolist():
                edges.add((row["Art"], val))

    if prec: # No need to iterate count_article here
        edges.add((row["Art"], cc.iloc[index - 1]["Art"]))
    if prec:
        edges.add((row["Art"], cc.iloc[index + 1]["Art"]))
