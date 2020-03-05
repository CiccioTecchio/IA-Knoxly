# data una frase presente nel dataset restituisce le frasi simili
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os, sys, pandas, pickle
from sklearn.metrics.pairwise import cosine_similarity


# get cosine similairty matrix
def cos_sim(input_vectors):
    similarity = cosine_similarity(input_vectors)
    return similarity

    # get topN similar sentences
def get_top_similar(sentence, sentence_list, similarity_matrix, topN):
    # find the index of sentence in list
    index = sentence_list.index(sentence)
    # get the corresponding row in similarity matrix
    similarity_row = np.array(similarity_matrix[index, :])
    # get the indices of top similar
    indices = similarity_row.argsort()[-topN:][::-1]
    return [sentence_list[i] for i in indices]

filename = "src/dataset.csv"
colnames = ['text', 'tipo']
data = pandas.read_csv(filename, encoding='utf8', skiprows=1, names=colnames)
X_embed = pickle.load(open("src/dump/X_embed", "rb"))

sentences_list = data.text.tolist()

similarity_matrix = cos_sim(np.array(X_embed))

sentence = "My latimesopinion oped on historic California Senate race First time an elected woman senator succeeds anothernhttpstcocbjQTK0Q1V" #0
top_similar = get_top_similar(sentence, sentences_list, similarity_matrix, 3)

# printing the list using loop 
for x in range(len(top_similar)): 
    print(top_similar[x])