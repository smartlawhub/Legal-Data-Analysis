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
df = pd.read_csv("ICCData.csv", header="infer")
df = df.fillna("")

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

#TODO Fix issue with weight
import networkx as nx

G = nx.Graph()
node_list = []
details_list = []  # A list of the same size as node_list, for graphs purposes
edge_list = []
for arb in df.groupby("Name"):
    subdf = df.loc[(df.CID == cid) & (df.Name !=arb[0])]
    if len(subdf): # We don't care about sole arbs that are never on a tribunal with someone else
        nation = arb[1].iloc[0]["Nationality"]
        node_list.append((arb[0], {"gender": arb[1].iloc[0]["Gender"], "nationality": nation}))
        details_list.append([arb[0], len(arb[1]), "blue"])
        for cid in arb[1]["CID"].values.tolist():
            for index, row in subdf.iterrows():
                new_edge = (arb[0], row["Name"])
                num_edges = Counter(edge_list)[new_edge] + 1
                edge_list.append((new_edge, {"weight": num_edges}))
G.add_nodes_from(node_list)
G.add_edges_from(edge_list)
df_nodes = pd.DataFrame(details_list, columns=["Name", "Degree", "Nationality"])
df_nodes["page_rank"] = df_nodes.Name.map(nx.pagerank(G))
df_nodes["betweennessè_centrality"] = df_nodes.Name.map(nx.betweenness_centrality(G))

nx.draw_networkx(G, node_color=[x[1] for x in details_list], node_size=[x[0] for x in details_list])