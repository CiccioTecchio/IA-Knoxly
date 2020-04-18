import pandas, os, time, pickle
import metriche, embedding
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import accuracy_score 

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#Carico i dati
colnames = ['text', 'tipo', 'sensibile']
filename = open('src/ds200.csv','r')
pathdump = "src/dump/"
dump_y, dump_embed, dump_classificatore = pathdump, pathdump, pathdump
data = pandas.read_csv(filename, encoding='utf8', skiprows=1, names=colnames)

#Load embed
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

#Creazione dataset
X_text = data.text.tolist()
X_embed = embed(X_text)
y = data.tipo.tolist()
y = np.array(y)

# Split & Random Forest
training_set_data,test_set_data,training_set_labels,test_set_labels = train_test_split(X_embed,y,test_size=0.2,stratify=y)
n_folds=10
classificatore = RandomForestClassifier()
pg = {'n_estimators':[17,37,51,177,213,517], 'min_samples_leaf':[1],'n_jobs':[-1]}
print("Random Forest")
bestRFparam=metriche.grid("RF",classificatore,pg,n_folds, training_set_data,training_set_labels,'roc_auc')
print(bestRFparam)

classificatore=RandomForestClassifier(n_estimators=bestRFparam['n_estimators'],min_samples_leaf=bestRFparam['min_samples_leaf'],n_jobs=-1)
classificatore.fit(training_set_data,training_set_labels)
print("Random Forest")
print("accuracy")
y_pred=classificatore.predict(test_set_data)

print(accuracy_score(test_set_labels,y_pred))
precision, recall, fscore, support = score(test_set_labels, y_pred)
misure = metriche.printMisure(filename, precision, recall, fscore, accuracy_score(test_set_labels,y_pred))
fp = open("src/sensitiveness/training/misure_testing.txt", "a")
fp.write(misure)
fp.close()

#Plot roc_auc

#Print matrici di confusione

