import gender_guesser.detector as gender
import pandas as pd
import regex as re
from collections import Counter, defaultdict
from matplotlib import pyplot as plt

d = gender.Detector()


def guess_gender(details): # We first create a function to automate gender guessing
    results = []
    for e, name in enumerate(details[0].split(" ")):
        if len(details) > 1:
            for country in details[1].split("; "):
                county = re.sub(r"\s\(.*?\)\s?", "", details[1]).lower().replace(" ", "_")
                if county in d.COUNTRIES:
                    results.append(d.get_gender(name.capitalize(), county))
                elif len(results) == e:
                    results.append(d.get_gender(name.capitalize()))
        else:
            results.append(d.get_gender(name.capitalize()))
    return Counter([x for x in results if x != "unknown"]).most_common(1)


# We then load the dataset
df = pd.read_csv("Data/CSVs/ICCData.csv", header="infer")
df = df.fillna("")
#TODO get only last name
new_df = []  # And modify it to get a dataframe with
for index, row in df.iterrows():
    for x in range(1, 5):
        if row["Arbitrator_" + str(x)] != "":
            details = row["Arbitrator_" + str(x)].split(" | ")
            name = re.sub('\=HYPER.*?\s\"', "", details[0]).upper()
            if len(details) > 1 and name not in [x[4] for x in new_df[-3:]]:
                sublist = [index, row["Date"], row["Status"], row["Case_Number"]] + [name, details[1]] + details[-2:]  # Some details are longer because they indicate role
            else:
                sublist = [index, row["Date"], row["Status"], row["Case_Number"]] + [name, "", "", ""]
            gg = guess_gender(details)
            sublist.append(gg[0][0]) if gg != [] else sublist.append("unknown")
            new_df.append(sublist)

df = pd.DataFrame(new_df, columns=["CID", "Date", "Status", "Number", "Name", "Nationality", "Appointment", "X", "Gender"])

# We first have a broad look at the data, for instance gender stats

df.Gender.value_counts()
df.Gender = df.Gender.str.replace("mostly_", "")  # We remplace guesses by certain data
df.Gender.value_counts(normalize=True) * 100


# We also check the distribution, realise it's a power law
df.Name.value_counts().hist(bins=10)
plt.show()

import networkx as nx
from networkx.algorithms import community

node_list = []
edge_list = []
colors = {"United Kingdom (of Great Britain and Northern Ireland)": "blue", "France": "red", "Brazil": "green", "Switzerland": "grey", "United States of America": "gold", "Germany": "black", "Mexico": "purple", "Spain": "yellow"}
gender = {"male": "blue", "female": "pink", "andy": "purple", "unknown": "grey"}
for arb in df.groupby("Name"):
    cids = arb[1]["CID"].values.tolist()  # All common IDs
    subdf = df.loc[(df.CID.isin(cids)) & (df.Name != arb[0])]
    if len(subdf): # Filtering to remove sole arbs that are never on a tribunal with someone else
        nation = arb[1].iloc[0]["Nationality"]  # Any row would go, since nation is always the same for a given individual
        common_manager = Counter([x.split("/")[-1] for x in arb[1]["Number"].values.tolist()]).most_common(1)[0][0]  # Case manager is indicated from case number
        main_appointment = Counter(arb[1]["Appointment"]).most_common(1)[0][0]
        node_list.append((arb[0], {"gender": arb[1].iloc[0]["Gender"], "nationality": nation, "manager": common_manager, "appointment": main_appointment}))
        if nation not in colors.keys():
            colors[nation] = "blue"
        for cid in cids:
            subdf = df.loc[(df.CID == cid) & (df.Name != arb[0])]
            for index, row in subdf.iterrows():
                edge_list.append([arb[0], row["Name"], cid])
df_edge = pd.DataFrame(edge_list, columns=["Source", "Target", "Case"])
df_edge['weight'] = df_edge.groupby(['Source', 'Target'])['Source'].transform('size')
G = nx.from_pandas_edgelist(df_edge, 'Source', 'Target', create_using=nx.Graph(), edge_attr='weight')
G.add_nodes_from(node_list)  # We re-add the nodes to be sure they come with wanted data
degree = dict((x,y) for x, y in G.degree)  # A dict to get the number of connections for names

# Checking some basic metrics

nx.density(G)  # How dense is your network ?
nx.attribute_assortativity_coefficient(G, "gender")  # How much do your nodes create edges between themselves based on some common characteristics ?
nx.attribute_assortativity_coefficient(G, "nationality")
nx.attribute_assortativity_coefficient(G, "manager")
nx.attribute_assortativity_coefficient(G, "appointment")

print(nx.number_connected_components(G)) # How many "components" in the network, i.e., self-standing communities of nodes-edges


# We can draw that network, based on an algorithm that would highlight hubs around central nodes

nx.draw(G, pos=nx.spring_layout(G), node_color=[colors[x[1]["nationality"]] for x in G.nodes(data=True)._nodes.items()], node_size=[degree[x[0]] for x in G.nodes(data=True)._nodes.items()], with_labels=False)

# Good idea to ignore islands and focus on what's called the principal/giant component

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
G0 = G.subgraph(Gcc[0])
nx.draw(G0, pos=nx.spring_layout(G0), node_color=[colors[x[1]["nationality"]] for x in G0.nodes(data=True)._nodes.items()], node_size=[degree[x[0]] * 4 for x in G0.nodes(data=True)._nodes.items()], with_labels=False)


# Calculate some scores for a given arbitrator

df_nodes = pd.DataFrame([[x[0], degree[x[0]], x[1]["nationality"], x[1]["appointment"]] for x in node_list], columns=["Name", "Degree", "Nationality", "Appointment"])

df_nodes["ec"] = df_nodes.Name.map(nx.eigenvector_centrality(G, weight="weight"))  # centrality measures the importance of a given node based on the importance of its neighbours: having 300 low-value friends do not make you high-value
df_nodes["page_rank"] = df_nodes.Name.map(nx.pagerank(G, weight="weight"))  #A variant measure is Pagerank, which you can think as the  prestige of given nodes in a network
df_nodes["betweenness_centrality"] = df_nodes.Name.map(nx.betweenness_centrality(G)) # Betweenness centrality indicates which nodes are the most central in terms of conveying information - how often a node is on the shorter path between two other nodes

c0 = community.greedy_modularity_communities(G0)
map = {}
for e, x in enumerate(c0):
    for arb in x:
        map[arb] = e
df_nodes["Community"] = df.Name.map(map)
df_nodes.to_clipboard()
