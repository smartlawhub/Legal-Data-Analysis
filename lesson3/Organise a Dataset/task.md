## Organise a Dataset

<b>1. </b> Before working on the data you collected, let's turn to an existing dataset, which you can find on data.
gouv.fr. <a href="https://www.data.gouv.fr/fr/datasets/avis-et-conseils-de-la-cada/">here</a>.

This is a heavy file - we'll downsize it a bit later -, which collects all decisions by the CADA since its creation 
until November 2011, nearly 50,000 in total. We'll clean and perform basic analyses of this file. 

<b>2. </b> CSV cells have a character limit (exactly 32,767 for a single cell, the same as in Excel, although the 
latter also have row and columns limits), and it's quite frequent that this is exceeded when dealing with 
texts. 
Sure enough, this one has an error at some point, which is clearly visible when you open the file on Excel, but can 
also be guessed due to higher-than-expected number of columns in the pandas df (all those "Unnamed" columns).

Although we could clean this quickly in Excel, we can also do it with `pandas`. Notice that overflowing text will often 
be stored on a new row, and then use columns that are not meant to receive text. For instance, the first column of 
the dataframe here is `Numéro de dossier`, and it's always a number following a specific format.

Once we know this, it's easy enough to locate rows that are corrupted. Here is one way

```python
import pandas as pd

df = pd.read_csv("cada-2021-11-10.csv", header="infer", encoding="utf8")

df["Len"] = df["Numéro de dossier"].str.len()  # We compute the length of every string in the first column, and store the result in a new column
df["Len"].value_counts()
```

This will identify the rows that are corrupted. Although we did that by focusing on the `.len` of some entries, there 
are plenty of other ways to go about it. You could for instance check which cells in the first column can't be expressed as a number, which row 
does not have all columns correctly filled (assuming they all should), etc.

<b>2. </b> Once it's cleaned, we can investigate it. One question you migh ask is: how did the number of decision 
vary through the years. 
