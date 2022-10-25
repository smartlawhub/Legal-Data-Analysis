import pandas as pd
import regex as re
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('fivethirtyeight')

df = pd.read_csv("", header="infer", encoding="utf8")

df.groupby("Admin").Result.value_counts(normalize=True).unstack()  # As you can see, it's a bit harder to get a document from a Central administration, and a bit easier to get them from municipalities

# TODO We then check that the differences are statistically significant

ax = df.loc[df.Admin == "Central"].resample("1M").Result.value_counts(normalize=True).unstack()["Favourable"].rolling(3).sum().plot()   # Next we look at the number of decisions per month, focusing on Favourable results, and a rolled average of three months. We pass it to an object ax that will represent our plot
ax.axvline("2017-04-23", color="red")  # We add a line to indicate the presidential election

df.loc[df.Admin == "Department"].resample("1M").Result.value_counts(normalize=True).unstack()["Favourable"].rolling(3).sum().plot()    # Now the same for departmental elections
plt.axvline("2015-03-29", color="red")
plt.axvline("2021-06-29", color="red")

df.loc[df.Admin == "Regional"].resample("1M").Result.value_counts(normalize=True).unstack()["Favourable"].rolling(3).sum().plot()    # Now the same for regional elections
plt.axvline("2015-12-10", color="red")
plt.axvline("2021-06-29", color="red")


sns.set_style("dark")  # Change style of plots with sns
sns.countplot(x="Admin", hue="Result", data=df)   # Seaborn has great plot types such as this simple countplot

# Second analysis: the average length to get a CADA decision

import locale
locale.setlocale(locale.LC_ALL, "fr_FR")  # Depending on your OS, you may not be set to work with French data and format - such as dates - so we first need to set that

df["Séance"] = pd.to_datetime(df["Séance"], format="%Y-%m-%d")
df["Saisine"] = df.Avis.astype(str).str.extract("(\d\d? [a-z]+ \d{4})")  # We create a new column by looking into the text and extracting a date; we see that

df.Saisine.value_counts()  # We check, and this is not ideal, many false dates have inserted themselves
df["Saisine"] = df.Avis.astype(str).str.extract("le (\d\d? [a-z]{3,} \d{4})")  # One better way is to check for dates starting by "le", since most avis refer to a courrier "envoyé le"


df["DateS"] = pd.to_datetime(df["Saisine"], format="%d %B %Y", errors="coerce")  # Then we can convert the dates found to a datetime object; we "coerce" to ignore errors (wrong format, etc.)

df["Delta"] = df["Séance"] - df["DateS"]  # We obtain the delta between the two dates
df["Days"] = df.Delta.apply(lambda x: x.days)  # And then fetch the number of days from the datetime values in the delta column

df.loc[(df.Days > 0) & (df.Days < 300)].resample("3M").Days.mean().plot()  # Finally, we plot