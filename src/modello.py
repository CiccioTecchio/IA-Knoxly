import csv, os, pandas, sys, time, pickle
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#enable log of tf

def grid(cl,classifier,param_grid,n_folds,t_s_D,tLab_downsampled):
    with open("src/training/"+cl+".txt","w") as f:
        estimator = GridSearchCV(classifier, cv=n_folds, param_grid=param_grid, n_jobs=-1, verbose=1,scoring='accuracy')
        estimator.fit(t_s_D, tLab_downsampled)
        means = estimator.cv_results_['mean_test_score']
        stds = estimator.cv_results_['std_test_score']
        best=[]
        max=0
        for meana, std, params in zip(means, stds, estimator.cv_results_['params']):
            if meana>max:
                max=meana
                best=params
            print("%0.3f (+/-%0.03f) for %r" % (meana, std * 2, params))
            f.write("%0.3f (+/-%0.03f) for %r" % (meana, std * 2, params))
            f.write("\n")
        print()
    return best

def dividi(totList, start, n):
    tr = []
    i = 0
    while i<n: 
        tr.extend(embed([totList[start]]))
        i+=1
        start+=1
    return tr

def concat_Embed(totList, part):
    tr = []
    i, start = 0,0
    size = len(totList)
    n_part = size//part
    reminder = size%part
    while i < n_part:
        tr.extend(dividi(totList,start,part))
        i+=1
        start+=part
        print(str(i)+", "+str(len(tr)))
    if reminder != 0:
        tr.extend(dividi(totList,start,reminder))
        i+=1
        print(str(i)+", "+str(len(tr)))
    return tr

def printMisure(filename, precision, recall, fscore):
    dato = "dataset usato "+filename+":\n"
    prec = 'precision: {}'.format(precision)
    rec = '\nrecall: {}'.format(recall)
    fsc = '\nfscore: {}'.format(fscore)
    return dato+prec+rec+fsc


# SentenceEmbed
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


# Caricamento set di testi
colnames = ['text', 'tipo']
filename = str(sys.argv[1])

pathdump = "src/dump/"
dump_y, dump_embed, dump_classificatore = pathdump, pathdump, pathdump
if filename == "src/dataset.csv":
    dump_y+="y"
    dump_embed+="X_embed"
    dump_classificatore+="classificatore"
else:
    dump_y+="y_nosense"
    dump_embed+="X_embed_nosense"
    dump_classificatore+="classificatore_nosense"
print(filename)
data = pandas.read_csv(filename, encoding='utf8', skiprows=1, names=colnames)

# Creazione dataset
X_text = data.text.tolist()
file2 = "src/ds3000.csv"
data2 = pandas.read_csv(file2, encoding='utf8', skiprows=1, names=colnames)
foo_text = data2.text.tolist()
foo_y = data2.tipo.tolist()
start_time = time.time()
X_embed = concat_Embed(X_text, 500)
Foo_embed = concat_Embed(foo_text, 500)
y = data.tipo.tolist()
y = np.array(y)
pickle.dump(X_embed, open(dump_embed,"wb"))
pickle.dump(y, open(dump_y, "wb"))
print("EMBEDDING FATTO!!!")

# Split
training_set_data,test_set_data,training_set_labels,test_set_labels = train_test_split(X_embed,y,test_size=0.2,stratify=y)

n_folds=5
classificatore = RandomForestClassifier()
pg = {'n_estimators':[17,37,51,177,213,517], 'min_samples_leaf':[1],'n_jobs':[-1]}
print("Random Forest")
bestRFparam=grid("RF",classificatore,pg,n_folds, training_set_data,training_set_labels)
print(bestRFparam)


classificatore=RandomForestClassifier(n_estimators=bestRFparam['n_estimators'],min_samples_leaf=bestRFparam['min_samples_leaf'],n_jobs=-1)
classificatore.fit(training_set_data,training_set_labels)
print("Random Forest")
print("accuracy")
y_pred=classificatore.predict(test_set_data)

print(accuracy_score(test_set_labels,y_pred))
precision, recall, fscore, support = score(test_set_labels, y_pred)
misure = printMisure(filename, precision, recall, fscore)
fp = open("src/training/misure.txt", "a")
fp.write(misure)
fp.close()
print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
pickle.dump(classificatore, open(dump_classificatore, "wb"))

print("Random Forest")
print("accuracy")
y_pred=classificatore.predict(Foo_embed)

print(accuracy_score(foo_y,y_pred))
precision, recall, fscore, support = score(foo_y, y_pred)
misure = printMisure(filename, precision, recall, fscore)
fp = open("src/training/misurePred.txt","a")
fp.write(misure)
fp.close()
print("--- %s seconds ---" % round((time.time() - start_time),2))