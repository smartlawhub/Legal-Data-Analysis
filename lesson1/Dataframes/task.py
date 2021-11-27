import pandas as pd
import regex as re
from pygal_maps_fr import maps

df = pd.read_csv("fromages.csv", header="infer")

# First, some data investigation
df.head(5)
df.columns
df["Lait"].unique()
df["Lait"].value_counts()

df["Lait"].value_counts().plot(style="x")  # And now we can plot it

df["New_Col"] = ""  # Creating new column with empty values

dep_reg = pd.read_csv("departements-region.csv", header="infer", encoding="utf8")
dep_reg.head(15)

dict_dep = dep_reg.set_index("dep_name").to_dict()["region_name"]   # We create a dictionary from the second dataframe; this requires us to set the index with the keys of the dict: the departments; regions will be the values
df["Region"] = df["Departement"].map(dict_dep)  # Then we map that dictionary on the basis of the values that represent the same key: the departments
df["Region"].value_counts()

dict_num_dep = dict_dep = dep_reg.set_index("dep_name").to_dict()["num_dep"]
df["num_dep"] = df["Departement"].map(dict_num_dep)
dict_num_by_dep = df.num_dep.value_counts().to_dict()


fr_chart = maps.Departments(human_readable=True)
fr_chart.title = 'Population by department'
fr_chart.add('Number of Cheese by Dep', dict_num_by_dep)
fr_chart.render_in_browser(encoding="utf8")
