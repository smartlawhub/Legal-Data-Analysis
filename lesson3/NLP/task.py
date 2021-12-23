import os
import pandas as pd
import regex as re
import pandas
import spacy
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv()

nlp = spacy.load("en_core_web_trf", disable=["ner", "textcat"])


def spacy_process(text):  # We first prepare the text by using spacy's token elements to remove stop words and punctuation
    doc = nlp(text)

    filtered_sentence = []
    punctuations = "?:!.,;"
    for token in doc:
        if token.is_stop == False and token.lemma_ not in punctuations:
            filtered_sentence.append(token.lemma_)

    return " ".join(filtered_sentence)


df["cleaned_text"] = df.Text.map(lambda x: spacy_process(x))  # We apply it to our dataframe, so as to have a new column with cleaned text

aggregate_counter = Counter()
for row_index, row in df.iterrows():   # We then use this to count the words
    c = Counter(row['CText'].split())
    aggregate_counter += c

common_words = [word[0] for word in aggregate_counter.most_common(50)]
common_words_counts = [word[1] for word in aggregate_counter.most_common(50)]

bar_plt = sns.barplot(common_words, common_words_counts)  # We then create a bar plot with seaborn

for item in bar_plt.get_xticklabels():
    item.set_rotation(90)

plt.title("Most Common Words in Corpus")

# And now for something more complicated...


def get_sents(db):  # First we cut articles in sentences. Note that this could also be done using NLP, but I don't find the performance better in this case
    data = []
    ii = 0
    prev = ""
    for index, art in db.iterrows():
        sents = re.split(r"\.\n|\. (?=[A-Z])", art.Text)
        for sent in sents:
            ii = ii + 1 if art["ID"] == prev else 0
            l = [art["Code"], art["Art"], art["ID"], art["ID"] + "_" + str(ii), art["origin_date"], sent + ".", len(sent)]
            data.append(l)
            prev = art["ID"]
    return pd.DataFrame(data, columns=["Code", "Art", "ID", "Al", "origin_date", "Text", "lenText"])


def get_tense(tag):  # smaller function to get the tense of a verb
    tense = "Unknown"
    sea_tense = re.search(r"Tense=([a-zA-Z]*)($|\|)", tag)
    if sea_tense:
        tense = sea_tense.group(1)
    return tense


def get_subj(doc):  # smaller function to get a subject; return NoSubj if none
    pastsub = ""
    real_subj = "NoSubj"
    for subj in [x for x in doc if "nsubj" in x.dep_]:  #we iterate over the potential subjects in the parsed text
        real_subj = subj.lemma_
        if subj.pos_ == "PRON":  # Create exception for pronouns (former subject takes over)
            real_subj = pastsub
        else:
            pastsub = subj.lemma_
    return real_subj


def get_roots(rawtext):
    val = []  # We initiate a value that will receive the data
    doc = nlp(rawtext)
    for aux in [x for x in doc if x.lemma_ in ["pouvoir", "devoir"] and x.pos_ != "NOUN"]:  # we are looking for the two auxiliaries verb
        verbs = [x for x in doc[aux.i:] if "VerbForm=Inf" in x.tag_ or "VerbForm=Part" in x.tag_]  # Starting from the index of the auxilary, we look for the verb
        if len(verbs):  # If we find it, we append relevant data
            verb = verbs[0]
            val.append(verb.lemma_)
            val.append("inf")
            val.append(aux.lemma_)
            val.append("Neg") if doc[aux.i - 1].text == "ne" else val.append("Pos")
            val.append(get_tense(verb.tag_))
            val.append(get_subj(doc[:verb.i]))
        else:  # Otherwise, the verb is the auxiliary itself
            val.append(aux.lemma_)
            val.extend(["", ""])
            val.append("Neg") if doc[aux.i - 1].text == "ne" else val.append("Pos")
            val.append(get_tense(aux.tag_))
            val.append(get_subj(doc[:aux.i]))
        break
    if len(val) == 0:  # If the previous code had failed to populate val, we look for alternatives
        sea_pouvoir = re.search("(aur| )(a|ont) ((le )?droit|(la )?faculté)", rawtext)  # These are all alternatives ways to say "you can"
        sea_devoir = re.search("(est|sont|sera|seront) tenu", rawtext) # These are all alternatives ways to say "you must"
        if sea_pouvoir:
            val = ["", "droit de", "pouvoir"]
            verbs = [x for x in nlp(rawtext[sea_pouvoir.end():]) if "VERB" in x.tag_]
            val[0] = verbs[0].lemma_ if len(verbs) else ""
            val.append("Neg") if rawtext[sea_pouvoir.start() - 2:sea_pouvoir.start()] == "n'" else val.append("Pos")
            val.append("Pres") if re.search("est|sont|a droit", sea_pouvoir.group()) else val.append("Futur")
            subjs = [x for x in nlp(rawtext[:sea_pouvoir.start()]) if "nsubj" in x.pos_ or x.text == "Chacun"]  # Add an exception for chacun, since apparently spacy doesn't know it's a subject
            val.append(subjs[0].lemma_) if len(subjs) else val.append("")
        elif sea_devoir:
            val = ["", "tenu de", "devoir"]
            verbs = [x for x in nlp(rawtext[sea_devoir.end():]) if "VERB" in x.tag_]
            val[0] = verbs[0].lemma_ if len(verbs) else ""
            val.append("Neg") if rawtext[sea_devoir.start() - 2:sea_devoir.start()] == "n'" else val.append("Pos")
            val.append("Pres") if re.search("est|sont", sea_devoir.group()) else val.append("Futur")
            subjs = [x for x in nlp(rawtext[:sea_devoir.start()]) if "nsubj" in x.pos_]
            val.append(subjs[0].lemma_) if len(subjs) else val.append("")
    if len(val) == 0:  # If the alternatives above yet again have failed to populate val, look for other
        roots = [x for x in doc if re.search("VERB|AUX", x.tag_) and x.dep_ in ["ROOT", "cop"] and x.lemma_ != "être"]
        for verb in roots:
            val.append(verb.lemma_)
            if "VerbForm=Inf" in verb.tag_ or "VerbForm=Part" in verb.tag_:
                val.append("inf")
                auxs = [x for x in doc[:verb.i] if "aux" in x.dep_]
                if len(auxs):
                    aux = auxs[-1]
                    val.append(aux.lemma_)
                    val.append("Neg") if doc[aux.i - 1].text == "ne" else val.append("Pos")
                    val.append(get_tense(aux.tag_))
                    val.append(get_subj(doc[:aux.i]))
                    break
                else:
                    val = []
            else:
                val.extend(["", ""])
                val.append("Neg") if doc[verb.i - 1].text == "ne" else val.append("Pos")
                val.append(get_tense(verb.tag_))
                val.append(get_subj(doc[:verb.i]))
                break
    if len(val) == 0 and len([x for x in doc if re.search("VERB|AUX", x.tag_)]):
        verb = [x for x in doc if re.search("VERB|AUX", x.tag_)][0]
        val.append(verb.lemma_)
        val.append("NoRoot")
        val.append([x for x in doc[verb.i:] if not x.is_stop][0].lemma_)
        try: # Try because sometimes the script understand "A" in init of sentence as "avoir"
            val.append("Neg") if doc[verb.i - 1].text == "ne" or doc[:verb.i].text[-2] == "n'" else val.append("Pos")
        except:
            val.append("Error")
        val.append(get_tense(verb.tag_))
        val.append(get_subj(doc[:verb.i]))
    if len(val) == 0:
        val = ["", "Nothing", "", "", "", ""]
    return val


LL = get_sents(df)  # We then populate a dataFrame of alineas (sentences), and analyse them [don't do it, it can take time]
for index, row in LL.iterrows():
    LL.at[index, "verb"], LL.at[index, "inf"], LL.at[index, "aux"], LL.at[index, "Tone"], LL.at[index,"Tense"], LL.at[index, "Subj"] = get_roots(row.Text)
LL.loc[~LL.aux.isin(['', 'être', 'pouvoir', 'devoir', 'avoir']), "aux"] = ""
LL.index = pd.to_datetime(LL.origin_date)
LL["CodeArt"] = LL["Code"] + "_" + LL["Art"]
LL["version"] = LL.ID.apply(lambda x: x.split("_")[-1])


def get_code_by_date(db, end):  # The idea is to sort by version (lower number > newer text) as the dictionary will take the last result
    data = []
    tempdict = db[:end].set_index("CodeArt").sort_values(by="version", ascending=False).to_dict()["version"]
    for index, row in db[:end].iterrows():
        if row.CodeArt in tempdict and row["version"] == tempdict[row["CodeArt"]]:
            data.append(row.values)
    return pd.DataFrame(data, columns=db.columns)


for year in ["1950", "1990", "2000", "2010", "2020"]:  # And then we print the most common subjects per year
    print(year)
    db = get_code_by_date(LL, year)
    print(Counter(db.loc[~db.Subj.isin(["", "NoSubj"])]["Subj"]).most_common(10))
# TODO: convert into a bar chart
