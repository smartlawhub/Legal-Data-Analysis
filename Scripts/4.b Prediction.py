from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from collections import Counter
import pandas as pd
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
import matplotlib.pyplot as plt

nlp = spacy.load("fr_core_news_md", disable=["ner", "textcat"])


def spacy_process(text):  # We reuse the function we used in clustering, to clean the texts from stop words and get lemmas
    doc = nlp(text)
    filtered_sentence = []
    punctuations = "?:!.,;()[]\n"
    for token in doc:
        if token.is_stop is False and token.lemma_ not in punctuations:
            filtered_sentence.append(token.lemma_)
    return " ".join(filtered_sentence)


# 1.  This dataset was scraped in 4d. Topic Modelling
df = pd.read_csv("Data/CSVs/CassTexts.csv", header="infer", encoding="latin1")  # This is a dataset of decisions from the Cour de cassation involving a "contract" in 2021; there are 818
df = df.loc[df.Solution.isin(["Cassation", "Rejet"])]  # We focus only on the binary classification between Cassation and Rejet
df = df.fillna("")

# 2.

key = "Dispositif"
df["CText"] = df[key].apply(spacy_process)  # We clean the moyens with the function used above - It's already done in the dataset you have, but just so you can redo it if necessary
subdf = df[:600].copy()  # We'll work with a subsample, and check the results over the rest of the sample
predict_df = df[600:].copy()  # Which we call predict_df
x = subdf['CText'].values  # We collect moyens from the subdf
y = subdf['Solution'].values  # As well as values representing the result
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=1000)   # This function splits the sample into a train and test
tfidf = TfidfVectorizer(stop_words=fr_stop, ngram_range=(1,3), max_features=250, min_df=10)  # This will be the algorithm to transform the text data in mathematical format, using the tf-idf method we mentioned in Clustering, using a list of French stopwords from Spacy
tfidf.fit(df['CText'].values )  # We train that algorithm with the existing data, so that it know what's the weight of any given word ("feature") in the dataset
X_train = tfidf.transform(x_train)  # We then use the trained model to transform our subset of training data
X_test = tfidf.transform(x_test)  # Likewise with testing data
classifier = LogisticRegression()  # This is the method we'll be using, but there are many others ! This one is a basic regression
classifier.fit(X_train, y_train)  # We then feed that model with our training data
score = classifier.score(X_test, y_test)  # And try it over the test data to have a first idea of the accuracy
print("Accuracy:", score)  # Which is not bad !

#  And now we apply the model to the rest of the data

subpredictdf = tfidf.transform(predict_df["CText"])  # Then we test again, a second time, over the rest of the dataset. Likewise, we need to transform this bit of the dataset to mathematical values
val = classifier.predict(subpredictdf)  # We use the .predict function of the classifier to make predictions, this returns a list of labels
predict_df["Predict"] = val.tolist()  # Which we pass to the original dataframe (together with the original solution for the subdf we did not predict)
predict_df["Correct"] = predict_df.apply(lambda x: x["Solution"] == x["Predict"], axis=1)  # We then create a column that tracks done if prediction is equal to reality
print(predict_df.Correct.value_counts(normalize=True))  # And focusing only on those values we predicted, we look for the amount that we got right - this is in line with accuracy score

print(predict_df.groupby("Formation").Correct.value_counts(normalize=True).unstack())  # We can then compare

# To rebalance the model, we can oversample it - i.e., create fake data that corresponds to the existing one
from imblearn.over_sampling import RandomOverSampler  # This is a module you can dl with "pip install imbalanced-learn"
over_sampler = RandomOverSampler(random_state=42)
X_res, y_res = over_sampler.fit_resample(X_train, y_train)
print(f"Training target statistics: {Counter(y_res)}")
classifier.fit(X_res, y_res)  # We feed the model with this new data
score = classifier.score(X_test, y_test)  # And try it again over the test data to have a first idea of the accuracy
print("Accuracy:", score)

# 3.
from sklearn.model_selection import cross_val_score, StratifiedKFold  # We import a cross-validation method

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=17)  # We initialise the k-fold model, looking for 5 validations
print(cross_val_score(classifier, X_train, y_train, cv=skf, scoring='f1_micro'))

import eli5
data = eli5.show_weights(estimator=classifier, feature_names=list(tfidf.get_feature_names()), top=(50,5))
with open("data.html", "w") as file:
    file.write(data.data)


# 4

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

models = [RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0), DecisionTreeClassifier(max_depth=3),
    LinearSVC(), SVC(), LogisticRegression(random_state=0), GaussianNB(), XGBClassifier()]

CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))

entries = []
for model in models:
    model_name = model.__class__.__name__
    if model_name in ["GaussianNB"]:  # Some models require differently formatted data
        accuracies = cross_val_score(model, X_train.todense(), y_train, scoring='accuracy', cv=CV)
    elif model_name in ['XGBClassifier']:  # Some models require differently formatted data
        hot = {"Cassation": 0, "Rejet": 1}
        accuracies = cross_val_score(model, X_train, [hot[x] for x in y_train], scoring='accuracy', cv=CV)
    else:
        accuracies = cross_val_score(model, X_train, y_train, scoring='accuracy', cv=CV)
    for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name, fold_idx, accuracy))
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

import seaborn as sns
sns.boxplot(x='model_name', y='accuracy', data=cv_df)
sns.stripplot(x='model_name', y='accuracy', data=cv_df,
              size=8, jitter=True, edgecolor="gray", linewidth=2)
plt.show()
# Accuracy score
cv_df.groupby('model_name').accuracy.mean()
