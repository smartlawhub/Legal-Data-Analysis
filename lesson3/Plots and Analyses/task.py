import pandas as pd
import regex as re
import matplotlib.pyplot as plt

df = pd.read_csv("", header="infer", encoding="utf8")



df.groupby("Admin").Result.value_counts(normalize=True).unstack()

df.index = pd.to_datetime(df.Séance)
df.loc[df.Admin == "Central"]["2011-01-01":].resample("1M").Result.value_counts().unstack().plot()  # Next we look at the number of decisions per month. We start in 2011 because there are few decisions before
plt.axvline("2017-04-23")  # We add a line to indicate the presidential election

df.loc[df.Admin == "Department"]["2011-01-01":].resample("1M").Result.value_counts().unstack().plot()  # Now the same for departmental elections
plt.axvline("2015-03-29")
plt.axvline("2021-06-29")

df.loc[df.Admin == "Department"]["2011-01-01":].resample("1M").Result.value_counts().unstack().plot()  # Now the same for departmental elections
plt.axvline("2015-12-10")
plt.axvline("2021-06-29")
