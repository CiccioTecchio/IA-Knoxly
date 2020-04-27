import csv, os, pandas, sys, time, pickle
import metriche, embedding
import tensorflow as tf
import numpy as np 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#enable log of tf

# Caricamento set di testi
colnames = ['text', 'tipo']
filename = str(sys.argv[1])

pathdump = "src/dump/multilang/"
dump_y, dump_embed, dump_classificatore = pathdump, pathdump, pathdump
data = pandas.read_csv(filename, encoding='utf8', skiprows=1, names=colnames)

# Creazione dataset
X_text = data.text.tolist()
file2 = "src/ds2000.csv"
data2 = pandas.read_csv(file2, encoding='utf8', skiprows=1, names=colnames)
foo_text = data2.text.tolist()
foo_y = data2.tipo.tolist()
start_time = time.time()
X_embed = embedding.concat_Embed(X_text, 500)
y = data.tipo.tolist()
y = np.array(y)
pickle.dump(X_embed, open(dump_embed+"X_embed","wb"))
pickle.dump(y, open(dump_y+"y", "wb"))
print("EMBEDDING FATTO!!!")

# Split
training_set_data,test_set_data,training_set_labels,test_set_labels = train_test_split(X_embed,y,test_size=0.2,stratify=y)

n_folds=5
classificatore = RandomForestClassifier()
pg = {'n_estimators':[17,37,51,177,213,517], 'min_samples_leaf':[1],'n_jobs':[-1]}
print("Random Forest")
bestRFparam=metriche.grid("src/topic_class/training/multilang/RF.txt",classificatore,pg,n_folds, training_set_data,training_set_labels,'f1_weighted')
print(bestRFparam)


classificatore=RandomForestClassifier(n_estimators=bestRFparam['n_estimators'],min_samples_leaf=bestRFparam['min_samples_leaf'],n_jobs=-1)
classificatore.fit(training_set_data,training_set_labels)
print("Random Forest")
print("accuracy")
y_pred=classificatore.predict(test_set_data)

print(accuracy_score(test_set_labels,y_pred))
precision, recall, fscore, support = score(test_set_labels, y_pred)
misure = metriche.printMisure(filename, precision, recall, fscore, accuracy_score(test_set_labels,y_pred))
fp = open("src/topic_class/training/multilang/misure_testing.txt", "a")
fp.write(misure)
fp.close()
pickle.dump(classificatore, open(dump_classificatore+"topic_class", "wb"))

print("Random Forest")
print("accuracy")
Foo_embed = embedding.concat_Embed(foo_text, 500)
y_pred=classificatore.predict(Foo_embed)

print(accuracy_score(foo_y,y_pred))
precision, recall, fscore, support = score(foo_y, y_pred)
misure = metriche.printMisure(file2, precision, recall, fscore, accuracy_score(foo_y,y_pred))
fp = open("src/topic_class/validation/multilang/misure_wild.txt","a")
fp.write(misure)
fp.close()
print("--- %s seconds ---" % round((time.time() - start_time),2))