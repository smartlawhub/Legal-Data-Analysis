import regex as re
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt


cc = pd.read_csv("Data.csv", header="infer", encoding="latin1")
cc = cc.loc[cc.Code == "Code civil"]

nodes = set(cc.Art.values.tolist())  # Potential nodes are all articles we know exist. This will also be helpful to chech that citations are genuine
edges = set()

count_article = 0

for index, row in cc.iterrows():
    text = row["Text"]
    sea = re.search(r"Article (?<num>[\d-]+) (?!de la loi)", text, re.S|re.I)
    seas1 = re.search(r"Articles ([\d-]+[et, ]*)+", text, re.S|re.I)
    seas2 = re.search(r"Articles (?<lower>[\d-]+) à (?<upper>[\d-]+)", text, re.S|re.I)
    prec = re.search(r"articles? précédent", text, re.S|re.I)
    suiv = re.search(r"articles? suivant", text, re.S|re.I)

    if sea:
        if "Article " + sea.group("num") in nodes:
            edges.add((row["Art"], "Article " + sea.group("num")))

    if seas1:
        for num in re.findall("[\d-]+", text):
            if "Article " + num in nodes:
                edges.add((row["Art"], "Article " + num))

    if seas2:  # In the context of a range, two methods: we could transform the numbers in integers and add to them; or we can just leverage the existing dataset
        if "Article " + seas2.group("lower") in nodes and "Article " + seas2.group("upper") in nodes:
            lower_index = cc.loc[cc.Art == "Article " + seas2.group("lower")].index[0]
            upper_index = cc.loc[cc.Art == "Article " + seas2.group("upper")].index[0] + 1  # Don't forget that the upper range is not included in pandas indexing
            for val in cc[lower_index:upper_index].Art.values.tolist():
                edges.add((row["Art"], val))

    if prec:
        edges.add((row["Art"], cc.iloc[index - 1]["Art"]))
    if prec:
        edges.add((row["Art"], cc.iloc[index + 1]["Art"]))


G = nx.Graph()  # Create a graph
G.add_nodes_from(nodes)
G.add_edges_from(edges)

nx.draw_networkx(G, with_labels=False)
