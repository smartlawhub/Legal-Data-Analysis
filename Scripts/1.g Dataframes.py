import os
from matplotlib.pyplot import plot
import pandas as pd
import regex as re

os.chdir("./Data/CSVs")

df = pd.read_csv("Conseil Etat Novembre 2011.csv", header="infer")

# First, some data investigation
df.head(5)
print(df.columns)
print(df["Type_Recours"] ) # You access a particular column by indexing it this way (we'll see further indexing in a few weeks)
df["Type_Recours"].unique()  # Functions such as Unique renders a list of all possible values in a given column
df["Type_Recours"].value_counts()  # One of the most useful functions returns a count of all values

df["Type_Recours"].value_counts().plot(kind='barh')  # And now we can plot it with a bar chart

df.loc[df.Formation_Jugement == "Juge des référés"]  # Filtering the dataframe to focus on all rows where the formation of judgment is the "Juge des Référées
df.at[10, "Avocat_Requerant"]

for index, row in df.iterrows():
    print(row["Formation_Jugement"], row["Avocat_Requerant"])


df["New_Col"] = ""  # Creating new column with empty values
df["New_Col"] = df["Formation_Jugement"].str.replace("jugeant seule", "").str.strip()  # Filling that column with data from another column, except we changed all strings (str) with empty text, and then stripping

df.to_clipboard(index=False)
