import pandas, random, pickle, os
import numpy as np
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

def rndSentences(topicIndex, X_embed, n):
    tr = []
    l = len(topicIndex)
    for i in range(n):
        rnd = random.randrange(l)
        #print(str(i)+": "+str(rnd))
        tr.append(X_embed[rnd])
    return tr

def singleTopicMatrix(rnd_emb):
    l = len(rnd_emb)
    m = []
    for j in range(l):
        riga = []
        m.append(riga)
        for k in range(l):
            corr = np.inner(rnd_emb[j], rnd_emb[k])
            riga.append(round(corr, 3))
    return m

def writeSingleMtr(file, M):
    fp = open(file, "w")
    fp.write(str(np.matrix(M)))
    fp.close()

path = "src/dump"
colnames = ['text', 'tipo']
data = pandas.read_csv("src/dataset.csv", encoding='utf8', skiprows=1, names=colnames)
text = data.text.tolist()
tipo = data.tipo.tolist()
X_embed = pickle.load(open(path+"/X_embed", "rb"))
classificatore = pickle.load(open(path+"/classificatore", "rb"))
y = pickle.load(open(path+"/y", "rb"))

index_pol = getIndexOfTopic(text, tipo, 0)
index_health = getIndexOfTopic(text, tipo, 1)
index_work = getIndexOfTopic(text, tipo, 2)
index_fly = getIndexOfTopic(text, tipo, 3)

rnd_pol = rndSentences(index_pol, X_embed, 8)
rnd_health = rndSentences(index_health, X_embed, 8)
rnd_work = rndSentences(index_work, X_embed, 8)
rnd_fly = rndSentences(index_fly, X_embed, 8)

mtr_pol = singleTopicMatrix(rnd_pol)
mtr_health = singleTopicMatrix(rnd_health)
mtr_work = singleTopicMatrix(rnd_work)
mtr_fly = singleTopicMatrix(rnd_fly)

path = "src/matrix/single"
files = [path+"/pol.txt", path+"/health.txt", path+"/work.txt", path+"/fly.txt"]
writeSingleMtr(files[0], mtr_pol)
writeSingleMtr(files[1], mtr_health)
writeSingleMtr(files[2], mtr_work)
writeSingleMtr(files[3], mtr_fly)