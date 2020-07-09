import pandas as pd
import numpy as np
import tensorflow as tf
import tensorflow_text
import tensorflow_hub as hub

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")
colnames = ['text', 'tipo']
filename='ds1000.csv'
data = pd.read_csv(filename, encoding='utf8', skiprows = 1, names = colnames)

X_text = data.text.tolist()
Y_tipo = data.tipo.tolist()

list_p = []
list_h = []
list_j = []
list_t = []
list_g = []
listEmbed = []

NUM_EL = 20

def embedList(lista):
	for i in lista:
		listEmbed.extend(embed(i))


i = 0
l = len(X_text)
l_g = len(list_g)

while i < l and l_g < NUM_EL:
	if(Y_tipo[i] == 1 and len(list_h) < NUM_EL):
		list_h.append(X_text[i])
	elif(Y_tipo[i] == 0 and len(list_p) < NUM_EL):
		list_p.append(X_text[i])
	elif(Y_tipo[i] == 2 and len(list_j) < NUM_EL):
		list_j.append(X_text[i])
	elif(Y_tipo[i] == 3 and len(list_t) < NUM_EL):
		list_t.append(X_text[i])
	elif(Y_tipo[i] == 4 and len(list_g) < NUM_EL):
		list_g.append(X_text[i])
	i+=1

embedList(list_p)
embedList(list_h)
embedList(list_j)
embedList(list_t)
embedList(list_g)

l = len(listEmbed)
m = []
listCorr = []
for i in range(l):
	riga = []
	m.append(riga)
	for j in range(l):
		corr = np.inner(listEmbed[i], listEmbed[j])
		riga.append(round(corr,3))
	listCorr.extend(riga)
	
for i in listCorr:
	print(i)


