import pandas as pd
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from sklearn.base import BaseEstimator
from sklearn import utils as skl_utils
from tqdm import tqdm
from scipy.spatial.distance import cosine
from sklearn.neural_network import MLPRegressor
import multiprocessing
import numpy as np

df = pd.read_csv()  # Put any data you want in that


def key_consine_similarity(tupple):
    return tupple[1]


def get_computed_similarities(ddf, vectors, predicted_vectors, reverse=False):
    data_size = len(ddf)
    cosine_similarities = []
    for i in range(data_size):
        cosine_sim_val = (1 - cosine(vectors[i], predicted_vectors[i]))
        cosine_similarities.append((i, cosine_sim_val))

    return sorted(cosine_similarities)


def display_top_n(ddf, sorted_cosine_similarities, n=15):
    for i in range(n):
        index, consine_sim_val = sorted_cosine_similarities[i]
        print(ddf.iloc[index]["Text"])
        print('Cosine Sim Val :', consine_sim_val)
        print('---------------------------------')


#  We'll use a transformer, fine-tuned here for your data, copied from https://medium.datadriveninvestor.com/unsupervised-outlier-detection-in-text-corpus-using-deep-learning-41d4284a04c8
class Doc2VecTransformer(BaseEstimator):

    def __init__(self, vector_size=100, learning_rate=0.02,  epochs=20):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self._model = None
        self.vector_size = vector_size
        self.workers = multiprocessing.cpu_count() - 1

    def fit(self, df_x, df_y=None):
        tagged_x = [TaggedDocument(str(row['CText']).split(),  [index]) for index, row in df_x.iterrows()]
        model = Doc2Vec(documents=tagged_x, vector_size=self.vector_size, workers=self.workers)

        for epoch in range(self.epochs):
            model.train(skl_utils.shuffle([x for x in tqdm(tagged_x)]), total_examples=len(tagged_x), epochs=1)
            model.alpha -= self.learning_rate
            model.min_alpha = model.alpha

        self._model = model
        return self

    def transform(self, df_x):
        return np.asmatrix(np.array([self._model.infer_vector(str(row['CText']).split()) for index, row in df_x.iterrows()]))


dicsimil = {}
for group in df.groupby("cluster"):
    print(group[0])
    print(group[1].iloc[0]["Text"])
    doc2vec_tr = Doc2VecTransformer(vector_size=300)
    doc2vec_tr.fit(group[1])
    doc2vec_vectors = doc2vec_tr.transform(group[1])

    auto_encoder = MLPRegressor(hidden_layer_sizes=(600, 150, 600,))
    auto_encoder.fit(doc2vec_vectors, doc2vec_vectors)
    predicted_vectors = auto_encoder.predict(doc2vec_vectors)
    auto_encoder.score(predicted_vectors, doc2vec_vectors)

    cosine_similarities = get_computed_similarities(group[1], vectors=doc2vec_vectors,predicted_vectors=predicted_vectors)
    display_top_n(group[1], sorted_cosine_similarities=sorted(cosine_similarities, key=key_consine_similarity, reverse=False), n=5)
    for e, i in enumerate(cosine_similarities):
        dicsimil[group[1].index[e]] = i[-1]

print(df.groupby("Date").simil.mean().sort_values())
