from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import pandas as pd

nlp = spacy.load("fr_core_news_md", disable=["ner", "textcat"])


def spacy_process(text):  # We reuse the function we used in clustering, to clean the texts from stop words and get lemmas
    doc = nlp(text)
    filtered_sentence = []
    punctuations = "?:!.,;()[]\n"
    for token in doc:
        if token.is_stop is False and token.lemma_ not in punctuations:
            filtered_sentence.append(token.lemma_)
    return " ".join(filtered_sentence)


df = pd.read_csv("Moyens.csv", header="infer", encoding="utf8")  # This is a dataset of decisions from the Cour de cassation involving a "contract" in 2021; there are 818

df["CText"] = df.moyen.apply(spacy_process)  # We clean the moyens with the function used above - It's already done in the dataset you have, but just so you can redo it if necessary
subdf = df[:600].copy()  # We'll work with a subsample, and check the results over the rest of the sample
predict_df = df[600:].copy()  # Which we call predict_df

x = subdf['CText'].values  # We collect moyens from the subdf
y = subdf['solution'].values  # As well as values representing the result
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=1000)   # This function splits the sample into a train and test
tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1,3), max_features=250, min_df=10)  # This will be the algorithm to transform the text data in mathematical format, using the tf-idf method we mentioned in Clustering
tfidf.fit(x)  # We train that algorithm with the existing data, so that it know what's the weight of any given word ("feature") in the dataset
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
predict_df["Correct"] = predict_df.apply(lambda x: x["solution"] == x["Predict"], axis=1)  # We then create a column that tracks done if prediction is equal to reality
print(predict_df.Correct.value_counts(normalize=True))  # And focusing only on those values we predicted, we look for the amount that we got right - this is in line with accuracy score

print(predict_df.groupby("chamber").Correct.value_counts(normalize=True).unstack())  # We can then compare by chamber
