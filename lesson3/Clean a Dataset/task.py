import pandas as pd
import regex as re
import matplotlib.pyplot as plt
from collections import Counter

# 1

df = pd.read_csv("cada-2021-11-10.csv", header="infer", encoding="utf8")

len(df)
df.head(15)  # We check that it is well-loaded
print(df.columns)

# Need to recreate corrupt file since they cleaned it on 14 December
df["Len"] = df["Numéro de dossier"].str.len()  # We compute the length of every string in the first column, and store the result in a new column.
df["Len"].value_counts()  # We check the distribution

df = df.drop(df[df.Len > 9].index)  # And then we pass the index of the rows that have a Len > 9 (for the first column) to the drop function
df = df.drop('Len', axis=1)  # We also delete the Len column, which now serves no purpose. Notice the axis = 1 argument to the drop function: it's to indicate that you are dropping columns, not rows

for x in range(10, 13):  # We also delete the empty columns. We could be lazy and merely copy and paste the columns' names, but that's more methodical
    col_to_del = "Unnamed: " + str(x)
    df = df.drop(col_to_del, axis=1)

df = df.dropna()  # We also try to drop the empty rows, if any are left. This is important to deal with datatypes

df["Année"] = df.Année.astype(int)  # For instance, because of the corruption, the columns "Années" is indicated as "object", while it should be an "int"

# 2

df.Type.value_counts(normalize = True)  # We can also multiply by * 100 to get proper percentages
df.groupby("Année").size().plot()  # We group by years, and then use plot the have an idea of the distribution

df.groupby("Année").Type.value_counts().unstack()   # We combine both tools to get a broader type of chart, and then we unstack

# 3

keys = df["Mots clés"].values.tolist()  # It's sometimes helpful to convert the data in another format, such as columns into a list, which will be ordered just as the dataframe was
Counter(re.split(", |\$", "$".join(keys))).most_common(10)  # Then we find the most common elements  in the Mot Clés


df.iloc[10]  # Compared to your Excel, pandas are shifted two indexes below, to account for 1. the headers, and 2. the fact that Python indexes start at 0

df.loc[df.Année == "1999"]  # You specify a condition, and then obtain a smaller dataframe if you do not care for a particular column; notice that the type is important
df.loc[df.Année == 1999][["Type", "Objet"]]  # You get more than one columns by using a double list

