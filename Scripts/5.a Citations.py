import networkx as nx
from operator import itemgetter
from networkx.algorithms import community
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from networkx.algorithms import community
import regex as re


cc = pd.read_csv("./Data/CSVs/CodeCivilChapters.csv", header="infer", encoding="utf8")  # A dataframe with articles from the code civil together with hierarchy
cc = cc.fillna("")
# Exercise : we need to replace the [Text] column with a better version of the articles, so you should iterate over the dataframe and scrap each url one by one


nodes = set(cc.Art.values.tolist())  # Potential nodes are all articles we know exist. This will also be helpful to check that citations are genuine
edges = set()  # This will take a tuple, as NetworkX needs that kind of input - though we could also create a df

count_article = 0

for index, row in cc.iterrows():  #We iterate over all articles
    text = row["Text"]
    sea = re.search(r"Article (?<num>[\d-]+)(?! de la loi)", text, re.S|re.I)  # Basic Search
    seas1 = re.search(r"Articles ([\d-]+[et, ]*)+", text, re.S|re.I)  # For list of articles
    seas2 = re.search(r"Articles (?<lower>[\d-]+) à (?<upper>[\d-]+)", text, re.S|re.I)  # For ranges of articles
    prec = re.search(r"articles? précédent", text, re.S|re.I)  # Relative Links
    suiv = re.search(r"articles? suivant", text, re.S|re.I)  # Relative Links

    if sea:
        count_article += 1  # We count all times when an article is found, even when it's not from the Code civil
        if "Article " + sea.group("num") in nodes:
            edges.add((row["Art"], "Article " + sea.group("num")))

    if seas1:
        count_article += 1
        for num in re.findall(r"[\d-]+", text):
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

# 3

G = nx.Graph()  # Create a graph
G.add_nodes_from(nodes)
G.add_edges_from(edges)

nx.draw_networkx(G, with_labels=False)  # We initialise the graph

print(nx.info(G))  # Basic data points about your network

cc.Livre = cc.Livre.replace(" :.*", "", regex=True)  # We make it easier to work with
nx.set_node_attributes(G, cc.set_index("Art").to_dict()["Livre"], "Livre")  # Next we add attributes to our nodes to be able to differentiate them

# 4

nx.draw_spring(G, with_labels=False)
smaller_G = G.remove_nodes_from(list(nx.isolates(G)))  # We can remove isolates, but there are none in this network

colors_dict = {"Livre Ier": "blue", "Livre II": "red",
               "Livre III": "yellow", "Livre IV": "black",
               "Livre V": "green",
               "Titre préliminaire": "white"}
colors = []
for node in G.nodes:
    colors.append(colors_dict[G.nodes[node]["Livre"]])

nx.draw_spring(G, with_labels=False, node_color=colors)

# 5

nx.density(G)  # How dense is your network when compared with the total number of edges possible ?

print(nx.is_connected(G))  # Indicates that the graph is not connected, which is not surprising since ...
print(nx.number_connected_components(G))  # There are many, many components ! Most of these, however, are solitary nodes
ii = 0
len_graphs = []
for comp in nx.connected_components(G):  # We can then have a look at components with more than one node, and see the distribution
    if len(comp) > 1:
        subgraph = G.subgraph(comp)
        len_graphs.append(
            [len(comp), nx.diameter(subgraph)])

sns.scatterplot([x[0] for x in len_graphs], [y[1] for y in len_graphs], legend='full')  # We can even plot it to see the distribution
plt.xlabel("Edges")
plt.ylabel("Nodes")

# 6

# Assign each to an attribute in your network

nx.set_node_attributes(G, nx.betweenness_centrality(G), 'betweenness')
nx.set_node_attributes(G, nx.eigenvector_centrality(G), 'eigenvector')

sorted([(x, G.nodes[x]["eigenvector"]) for x in G.nodes], key=itemgetter(1), reverse=True)[:10]  # Find the most important articles in terms of hubs
sorted([(x, G.nodes[x]["betweenness"]) for x in G.nodes], key=itemgetter(1), reverse=True)[:10]  # Find the most important articles in terms of hubs


# 6

parts = community.greedy_modularity_communities(G)
print(len(parts))  # We can see that the greedy methord returned a lot of communities, which is not surprising given how sparse the network is
