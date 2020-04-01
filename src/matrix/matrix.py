import pandas, random, pickle, os, time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
from pandas import DataFrame 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#enable log of tf
random.seed(0)
def getIndexOfTopic(topic):
    tr, i = [], 0
    l = len(text)
    while i<l and tipo[i]!=topic:
        i+=1
    while i<l and tipo[i] == topic:
        tr.append(i)
        i+=1
    return tr

def rndSentences(topicIndex, n, fp):
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

def doubleTopicMatrix(fp, n_sentences):
    index, tr, c = [], [], 0
    for i in listTopicsIndex:
        end = len(i)-1
        tmp = []
        for j in range(n_sentences):
            rnd = random.randrange(end)
            tmp.append(i[rnd])
        index.extend(tmp)
    for i in index:
        fp.write(str(c)+":"+str(i)+" "+text[i]+"\n")
        tr.append(X_embed[i])
        c+=1
    return tr 

def createMatrix(n_sentences):
    matrixList = []
    for i in range(len(listTopicsIndex)):
        fp = open(files[i], "w")
        rnd = rndSentences(listTopicsIndex[i], n_sentences, fp)
        mtr = topicMatrix(rnd)
        writeMatrix(fp, mtr) 
        matrixList.append(mtr)
    return matrixList

def switch(i):
    switcher = {
        0: "p",
        1: "h",
        2: "w",
        3: "f",
        4: "m"
    }
    return switcher.get(i, 'inalid topic')

def plotSingleMatrix(ml, n_sentences):
    path = "src/matrix/plot/"
    graph = ["politics", "health", "work", "fly", "movie"]
    cols = []
    lm = len(ml)
    for i in range(n_sentences):
        col = []     
        cols.append(col)
        for j in range(n_sentences):
            col.append(switch(i)+str(j))
    for i in range(lm):
        df = DataFrame(ml[i],columns=cols[i])
        ax = plt.axes()
        sn.heatmap(df, annot=True, annot_kws={"fontsize":4},ax = ax, yticklabels=cols[i])
        ax.set_title("Correlection matrix of "+graph[i])
        plt.savefig(path+graph[i]+".pdf")
        plt.close()

def plotMixedMatrix():
    path = "src/matrix/plot/mixed.pdf"
    col = []
    for i in range(5):#topic num
        for j in range(n_mix):#num frasi per singolo topic
            col.append(switch(i)+str(j))
    df = DataFrame(mixedMtr, columns=col)
    ax = plt.axes()
    sn.heatmap(df, annot=True, ax=ax, yticklabels=col, annot_kws={"fontsize":3})
    ax.set_title("Correlation matrix of mixed topic")
    plt.savefig(path)
    plt.close()

def getEmbedByTopic(indexTopic):
    a = []
    for i in indexTopic:
        a.append(X_embed[i])
    return a
    

def allProduct(embedTopic, threshold, n_sentences): #passa il vettore dei topic x ottenere la matrice dei singoli topic o X_embed per ottenere la mixed matrix
    l = len(embedTopic)
    m, thresholds = [], []
    maxC = threshold
    for j in range(l):
        riga = []
        m.append(riga)
        for k in range(l):
            corr = np.inner(embedTopic[j], embedTopic[k])
            if len(thresholds) < n_sentences and  corr >=maxC:
                maxC = corr
                thresholds.append([embedTopic[j], embedTopic[k]])
            riga.append(round(corr, 3))
    return m, thresholds

def matrixMax(thresholds):
    l = len(thresholds)
    A = []
    for i in range(l):
        riga = []
        A.append(riga)
        for j in range(l):
           if i == j:
               riga.append(round(np.inner(thresholds[i][0], thresholds[j][0]),3))
           elif i <j:
               riga.append(round(np.inner(thresholds[i][0], thresholds[j][1]),3))
           else:
               riga.append(round(np.inner(thresholds[i][1], thresholds[j][0]),3))
    return np.matrix(A) 

def higherProduct(matrix,threshold,n_sentences):
    i,j = 0,0
    A = []
    while len(A) < n_sentences:
        riga = []
        A.append(riga)
        while len(A[i]) < n_sentences:
            if matrix[i][j] >= threshold:
                riga.append(matrix[i][j])
            j+=1
        j = 0
        i+=1
    return A

path = "src/dump"
colnames = ['text', 'tipo']
filename = "src/dataset_nosense.csv"
data = pandas.read_csv(filename, encoding='utf8', skiprows=1, names=colnames)
dump_embed, dump_y = path, path

if filename == "src/dataset.csv":
    dump_embed+="/X_embed"
    dump_y+="/y"
else:
    dump_y+="/y_nosense"
    dump_embed+="/X_embed_nosense"

text = data.text.tolist()
tipo = data.tipo.tolist()
X_embed = pickle.load(open(dump_embed, "rb"))
y = pickle.load(open(dump_y, "rb"))

index_pol = getIndexOfTopic(0)
index_health = getIndexOfTopic(1)
index_work = getIndexOfTopic(2)
index_fly = getIndexOfTopic(3)
index_movie = getIndexOfTopic(4)

path = "src/matrix/report"
files = [path+"/pol.txt", path+"/health.txt", path+"/work.txt", path+"/fly.txt", path+"/movie.txt", path+"/mixed.txt"]

listTopicsIndex = [index_pol, index_health, index_work, index_fly, index_movie]
n_sentences = 20
matrixList = createMatrix(n_sentences)

fp = open(files[len(files)-1],"w")
n_mix = 5 #numero di frasi per topic
mixedList = doubleTopicMatrix(fp, n_mix)
mixedMtr = topicMatrix(mixedList)
writeMatrix(fp, mixedMtr)
#plotSingleMatrix(matrixList)
plotMixedMatrix()
embed_pol = getEmbedByTopic(index_pol)
embed_health = getEmbedByTopic(index_health)
embed_work = getEmbedByTopic(index_work)
embed_fly = getEmbedByTopic(index_fly)
embed_movie = getEmbedByTopic(index_movie)

m_pol, max_embed_pol = allProduct(embed_pol, 0.6, 5)
m_health, max_embed_health = allProduct(embed_health, 0.3, 5)
m_work, max_embed_work = allProduct(embed_work, 0.4, 5)
m_fly, max_embed_fly = allProduct(embed_fly, 0.5, 5)
m_movie, max_embed_movie = allProduct(embed_movie, 0.6, 5)
max_pol = matrixMax(max_embed_pol)
max_list = [
matrixMax(max_embed_pol),
matrixMax(max_embed_health),
matrixMax(max_embed_work),
matrixMax(max_embed_fly),
matrixMax(max_embed_movie)
]
plotSingleMatrix(max_list, 5)