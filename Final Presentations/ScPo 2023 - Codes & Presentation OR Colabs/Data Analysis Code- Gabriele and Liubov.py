# -*- coding: utf-8 -*-
"""
@author: Gabriele and Liubov

"""

#Our project focuses on what articles of the ECHR are most likely to be cited together or violated together in case law. 

import pandas as pd
import re

#First step: Collecting of the data
#We already had a file with many ECHR cases, however, we needed to update it with the most recent cases
extra_1 = pd.read_csv("ECHR_extra_1.csv")
extra_2 = pd.read_csv("ECHR_extra_2.csv")
data_full = pd.read_csv("EchrBaseFull.csv")

extra_1.rename(columns={'Application Number': 'Ids'}, inplace=True)
extra_2.rename(columns={'Application Number': 'Ids'}, inplace=True)
data_full.rename(columns={"Application Number":"Ids", "Conclusions":"Conclusion"}, inplace=True)


data_full = data_full.drop(columns=['Nb',"State"])
extra_1 = extra_1.drop(columns = ["Document Title","Document Type","Originating Body"])
extra_2 = extra_2.drop(columns = ["Document Title","Document Type","Originating Body"])


combined_full = pd.concat([data_full, extra_1, extra_2], axis=0, ignore_index=True)

combined_full = combined_full.fillna("")
for index, row in combined_full.iterrows():
    if row["Articles violated"] == "":
        violation_now = re.findall("Violation of Article \d+-?\d?", row["Conclusion"])
        violation_now = [a[13:] for a in violation_now]
        violation_now = pd.DataFrame(violation_now).drop_duplicates(keep="first").values.tolist()
        combined_full.at[index, "Articles violated"] = ["".join(inner_list) for inner_list in violation_now]
        
        no_violation_now = re.findall("No violation of Article \d+-?\d?", row["Conclusion"])
        no_violation_now = [a[16:] for a in no_violation_now]
        no_violation_now = pd.DataFrame(no_violation_now).drop_duplicates(keep="first").values.tolist()
        combined_full.at[index, "Articles not violated"] = ["".join(inner_list) for inner_list in no_violation_now]


final_df= combined_full.drop_duplicates(subset="Ids",keep="first") 

final_df.to_csv('echr_final_data.csv', index=False)

#Final data frame came out to 25807 cases. We made sure that none of them repeat by comparing them using the Ids column 
#the columns in our final data frame are: Ids, Date, Conclusion, Articles Violated, Articles not violated

#Second step: Finding the article combinations of article violations 
from itertools import combinations
from collections import Counter

chunk_size=1000 #had to add a chunk size as the code was crashing 

def generate_combinations_in_entries_violated(data):
    for _, row in data.iterrows():
        articles_violated = row["Articles violated"]
        
        if isinstance(articles_violated, list):
            articles_violated = ' '.join(articles_violated)

        extracted_articles = [article.strip() for article in re.findall(r'Article \d+(?: of Protocol No. \d+)?', articles_violated)]

        combinations_two_articles = combinations(extracted_articles, 2)
        yield from combinations_two_articles

combination_counts = Counter(generate_combinations_in_entries_violated(final_df))
for combination, count in combination_counts.most_common():
    print(f"Combination (Violated): {combination}, Count: {count}")
    
#Third step: making a graph to see the results 
import matplotlib.pyplot as plt

df_combinations = pd.DataFrame(list(combination_counts.items()), columns=["Combination", "Count"])

plt.figure(figsize=(10, 6))
df_combinations.sort_values(by="Count", ascending=False).head(15).plot(kind="bar", x="Combination", y="Count", color='skyblue')
plt.title("Top Articles Cited Together in ECHR case law")
plt.xlabel("Combination of Articles")
plt.ylabel("Count")
plt.show()

# Fourth step: find the frequency of individual articles
def generate_individual_article_frequency(data):
    all_extracted_articles = []

    for _, row in data.iterrows():
        articles_violated = row["Articles violated"]
        articles_not_violated = row["Articles not violated"]

        if isinstance(articles_violated, list):
            articles_violated = ' '.join(articles_violated)
        if isinstance(articles_not_violated, list):
            articles_not_violated = ' '.join(articles_not_violated)

        all_articles = articles_violated + articles_not_violated

        extracted_articles = [article.strip() for article in re.findall(r'Article \d+(?: of Protocol No. \d+)?', all_articles)]
        
        all_extracted_articles.extend(extracted_articles)

    df_all_articles = pd.DataFrame({"Articles": all_extracted_articles})
    article_counts = df_all_articles["Articles"].value_counts()
    
    return article_counts

def print_individual_article_frequency(data):
    article_counts = generate_individual_article_frequency(data)
    
    for article, count in article_counts.items():
        print(f"Article: {article}, Count: {count}")

print_individual_article_frequency(final_df)

# Fifth step: making a graph of the fequencies of individual articles
def plot_individual_article_frequency(data):
    article_counts = generate_individual_article_frequency(data)
    df_article_counts = pd.DataFrame(list(article_counts.items()), columns=["Article", "Count"])

    plt.figure(figsize=(10, 6))
    df_article_counts.sort_values(by="Count", ascending=False).head(15).plot(kind="bar", x="Article", y="Count", color='skyblue')
    plt.title("Most Cited Individual Articles in ECHR case law")
    plt.xlabel("Article")
    plt.ylabel("Count")
    plt.show()

plot_individual_article_frequency(final_df)
