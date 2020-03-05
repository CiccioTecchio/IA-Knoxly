import csv, pandas, sys, time, pickle
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score


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


# SentenceEmbed
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


# Caricamento set di testi
colnames = ['text', 'tipo']
filename = str(sys.argv[1])
print(filename)
data = pandas.read_csv(filename, encoding='utf8', skiprows=1, names=colnames)

# Creazione dataset
X_text = data.text.tolist()

start_time = time.time()
X_embed = concat_Embed(X_text, 500)
y = data.tipo.tolist()
y = np.array(y)
pickle.dump(X_embed, open("src/dump/X_embed","wb"))
pickle.dump(y, open("src/dump/y", "wb"))
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
print("--- %s seconds ---" % round((time.time() - start_time),2))
pickle.dump(classificatore, open("src/dump/classificatore", "wb"))