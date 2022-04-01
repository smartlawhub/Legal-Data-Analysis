import pandas as pd
import regex as re
import matplotlib.pyplot as plt
import seaborn as sns

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
