import pandas, random, pickle
import numpy as np

def singleTopic(text, tipo, topic):
    topicList = []
    i, l = 0, len(text)
    while i < l and tipo[i] != topic:
        i+=1
    while i < l and tipo[i] == topic:
        topicList.append(text[i])
        i+=1
    return topicList
    


def create_SingleMatrix(topicArray, nsen):
    tr = np.array([[],[]])
    for i in range(nsen):
        for j in range(nsen):
            rng =random.randrange(len(topicArray)-1)
            tr[i][j] = topicArray[rng]
    return tr
    

colnames = ['text', 'tipo']
data = pandas.read_csv("src/dataset.csv", encoding='utf8', skiprows=1, names=colnames)
text = data.text.tolist()
tipo = data.tipo.tolist()
#mtx = create_matrix(text, tipo, 4)#2frasi per ognuno dei 4 topic
politics = singleTopic(text, tipo, 0)
#print(len(singleTopic(text, tipo, 1)))
#print(len(singleTopic(text, tipo, 2)))
#print(len(singleTopic(text, tipo, 3)))
print(create_SingleMatrix(politics, 8))