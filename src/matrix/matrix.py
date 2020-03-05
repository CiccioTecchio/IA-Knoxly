import pandas, random, pickle, os
import numpy as np
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#enable log of tf
def getIndexOfTopic(text, tipo, topic):
    tr, i = [], 0
    l = len(text)
    while i<l and tipo[i]!=topic:
        i+=1
    while i<l and tipo[i] == topic:
        tr.append(i)
        i+=1
    return tr

def rndSentences(topicIndex,text, X_embed, n, fp):
    tr = []
    first, last = topicIndex[0], topicIndex[len(topicIndex)-1]
    for i in range(n):
        rnd = random.randrange(first,last)
        fp.write(str(i)+":"+str(rnd)+" "+text[rnd]+"\n")
        tr.append(X_embed[rnd])
    return tr

def topicMatrix(rnd_emb):
    l = len(rnd_emb)
    m = []
    for j in range(l):
        riga = []
        m.append(riga)
        for k in range(l):
            corr = np.inner(rnd_emb[j], rnd_emb[k])
            riga.append(round(corr, 3))
    return m

def writeMatrix(fp, M):
    fp.write(str(np.matrix(M)))
    fp.close()

def doubleTopicMatrix(listTopicsIndex, X_embed, text, fp):
    index, tr, c = [], [], 0
    for i in listTopicsIndex:
        end = len(i)-1
        rnd1, rnd2 = random.randrange(end), random.randrange(end)
        tmp = [i[rnd1], i[rnd2]]
        index.extend(tmp)
    for i in index:
        fp.write(str(c)+":"+str(i)+" "+text[i]+"\n")
        tr.append(X_embed[i])
        c+=1
    return tr 

def createMatrix(listTopicsIndex, X_embed, text, files):
    matrixList = []
    for i in range(len(listTopicsIndex)):
        fp = open(files[i], "w")
        rnd = rndSentences(listTopicsIndex[i], text, X_embed, 8, fp)
        mtr = topicMatrix(rnd)
        writeMatrix(fp, mtr) 
        matrixList.append(mtr)
    return matrixList
        
        
path = "src/dump"
colnames = ['text', 'tipo']
data = pandas.read_csv("src/dataset.csv", encoding='utf8', skiprows=1, names=colnames)
text = data.text.tolist()
tipo = data.tipo.tolist()
X_embed = pickle.load(open(path+"/X_embed", "rb"))
y = pickle.load(open(path+"/y", "rb"))

index_pol = getIndexOfTopic(text, tipo, 0)
index_health = getIndexOfTopic(text, tipo, 1)
index_work = getIndexOfTopic(text, tipo, 2)
index_fly = getIndexOfTopic(text, tipo, 3)

path = "src/matrix/single"
files = [path+"/pol.txt", path+"/health.txt", path+"/work.txt", path+"/fly.txt", path+"/double.txt"]

listTopicsIndex = [index_pol, index_health, index_work, index_fly]
matrixList = createMatrix(listTopicsIndex, X_embed,text, files)

fp = open(files[4],"w")
mixedList = doubleTopicMatrix(listTopicsIndex, X_embed,text, fp)
mixedMtr = topicMatrix(mixedList)
writeMatrix(fp, mixedMtr)