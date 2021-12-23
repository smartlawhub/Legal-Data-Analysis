import pandas as pd
import regex as re

df = pd.read_csv("", header="infer", encoding="utf8")

df["Sens et motivation"].value_counts()  # Value_counts is one of the most helpful commands to have a good sense of the dataset

df["Result"] = ""  # We want to create a column that gives us the result, there are several ways to do it

for index, row in df.iterrows():  # the first is to iterate over each row and check that the condition is met
    if re.search("défavorable", row["Sens et motivation"], re.S|re.I):
        df.at[index, "Result"] = "Unfavourable"
    elif re.search("favorable", row["Sens et motivation"], re.S|re.I):
        df.at[index, "Result"] = "Favourable"
    else:
        df.at[index, "Result"] = "Unfavourable"


def apply_result(value):  # Or we can just use a function that will do the same, and apply it to the dataframe with ".apply"
    if re.search("défavorable", value, re.S|re.I):
        return "Unfavourable"
    elif re.search("favorable", value, re.S|re.I):
        return "Favourable"
    else:
        return "Unfavourable"


df["Result"] = df["Sens et motivation"].apply(lambda x: apply_result(x))  # This allows you to apply a function to a value

df.Result.value_counts(normalize=True) * 100  # We obtain percent of favourable decisions

df.groupby("Année").Result.value_counts(normalize=True).unstack().plot()  # And then we plot it. See that the low number of entries for earlier years makes it harder to draw conclusions. It will help you to think of the commands here as every time creating a new output.

dict = {"[Mm]airie": "Municipal", "[Rr]égion": "Regional", "[dD]epartment": "Department",
        "[Mm]inist|[Pp]réfec?t": "Central"}  # Using a dict to keep the function shorter
def apply_type(value):
    for key in dict:
        if re.search(key, value.strip(), re.S|re.I):
            return dict[key]
            break
    return "Other"


df["Admin"] = df.Administration.apply(lambda x: apply_type(x))

df.loc[df.Admin == "Other"].Administration.value_counts()[:20]  # Locating with Python using a condition. You'll note for instance that acronymes with a number are often departemental admins, whereas the use of the term "national" indicate central administration

dict = {"[Mm]airie|agglom|commune": "Municipal", "[Rr]égion": "Regional", "[dD]epartment|\d\d\)?$": "Department",
        "[Mm]inist|[Pp]réfec?t|[Ddirection [Gg]énérale|[Nn]ational|[Ff]rançais|[Uu]niversit|[A-Z-]+\)?$": "Central"}

df.Admin.value_counts().to_dict()["Other"]
