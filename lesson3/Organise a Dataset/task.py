import pandas as pd
import regex as re


df = pd.read_csv("cada-2021-11-10.csv", header="infer", encoding="utf8")

len(df)
df.head(15)  # We check that it is well-loaded
df.columns

df["Len"] = df["Numéro de dossier"].str.len()  # We compute the length of every string in the first column, and store the result in a new column
df["Len"].value_counts()  # We check the distribution

df = df.drop(df[df.Len > 9].index)  # And then we pass the index of the rows that have a Len > 9 (for the first column) to the drop function
df = df.drop('Len', axis=1)  # We also delete the Len column, which now serves no purpose. Notice the axis = 1 argument to the drop function: it's to indicate that you are dropping columns, not rows

df.columns # Check that it worked

for x in range(10, 13):  # We also delete the empty columns. We could be lazy and merely copy and paste the columns' names, but that's more methodical
    col_to_del = "Unnamed: " + str(x)
    df = df.drop(col_to_del, axis=1)

df = df.dropna()  # We also try to drop the empty rows, if any are left. This is important to deal with datatypes

df["Année"] = df.Année.astype(int)  # For instance, because of the corruption, the columns "Années" is indicated as "object", while it should be an "int"
