# 1

import networkx as nx
from operator import itemgetter
from networkx.algorithms import community
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from networkx.algorithms import community

cc, nodes, edges = pd.DataFrame(), [], []  # Don't input this, it's only for the script to be correct; use the variables from the last task

# 2

G = nx.Graph()  # Create a graph
G.add_nodes_from(nodes)
G.add_edges_from(edges)

nx.draw_networkx(G, with_labels=False)  # We initialise the graph

print(nx.info(G))  # Basic data points about your network

cc.Livre = cc.Livre.replace(" :.*", "", regex=True)  # We make it easier to work with
nx.set_node_attributes(G, cc.set_index("Art").to_dict()["Livre"], "Livre")  # Next we add attributes to our nodes to be able to differentiate them

# 3

nx.draw_spring(G, with_labels=False)
smaller_G = G.remove_nodes_from(list(nx.isolates(G)))

colors_dict = {"Livre Ier": "blue", "Livre II": "red",
               "Livre III": "yellow", "Livre IV": "black",
               "Livre V": "green",
               "Titre prÃ©liminaire": "white"}
colors = []
for node in G.nodes:
    colors.append(colors_dict[G.nodes[node]["Livre"]])

nx.draw_spring(smaller_G, with_labels=False, node_color=colors)

# 4

nx.density(G)  # How dense is your network when compared with the total number of edges possible ?

nx.diameter(G)  # How large is your network ? Throws an error because some bits are not connected to each other
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

# 5

# Assign each to an attribute in your network
nx.set_node_attributes(G, nx.betweenness_centrality(G), 'betweenness')
nx.set_node_attributes(G, nx.eigenvector_centrality(G), 'eigenvector')

sorted([(x, G.nodes[x]["eigenvector"]) for x in G.nodes], key=itemgetter(1), reverse=True)[:10]  # Find the most important articles in terms of hubs
sorted([(x, G.nodes[x]["betweenness"]) for x in G.nodes], key=itemgetter(1), reverse=True)[:10]  # Find the most important articles in terms of hubs


# 6

parts = community.greedy_modularity_communities(G)
print(len(parts))  # We can see that the greedy methord returned a lot of communities, which is not surprising given how sparse the network is
