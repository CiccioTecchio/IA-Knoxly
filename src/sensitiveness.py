import pandas, os, time, pickle
import metriche, embedding
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import auc, accuracy_score, roc_auc_score, roc_curve

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def sensitiveness(ds, n_folds, scoring, path_RF, path_training):
    colnames = ['text', 'tipo', 'sensibile']
    #filename = open('src/ds200.csv','r')
    filename = open(ds ,'r')
    data = pandas.read_csv(filename, encoding='utf8', skiprows=1, names=colnames)
    X_text = data.text.tolist()
    X_embed = embedding.concat_Embed(X_text, 500)
    y = data.sensibile.tolist()
    y = np.array(y)
    start_time = time.time()
    training_set_data,test_set_data,training_set_labels,test_set_labels = train_test_split(X_embed,y,test_size=0.2,stratify=y)
    classificatore = RandomForestClassifier()
    pg = {'n_estimators':[17,37,51,177,213,517, 1013], 'min_samples_leaf':[1],'n_jobs':[-1]}
    print("Random Forest")
    bestRFparam=metriche.grid(path_RF,classificatore,pg,n_folds, training_set_data,training_set_labels,scoring)
    print(bestRFparam)
    classificatore=RandomForestClassifier(n_estimators=bestRFparam['n_estimators'],min_samples_leaf=bestRFparam['min_samples_leaf'],n_jobs=-1)
    classificatore.fit(training_set_data,training_set_labels)
    print("Random Forest")
    print("accuracy")
    y_pred=classificatore.predict(test_set_data)

    print("--- %s seconds ---" % round((time.time() - start_time),2))

    #PRINT MISURE
    print(accuracy_score(test_set_labels,y_pred))
    precision, recall, fscore, support = score(test_set_labels, y_pred)
    misure = metriche.printMisure(ds, precision, recall, fscore, accuracy_score(test_set_labels,y_pred))
    roc_auc = roc_auc_score(test_set_labels,classificatore.predict_proba(test_set_data)[:,1])
    fp = open(path_training, "w")
    fp.write(misure)
    fp.write("roc_auc: "+str(roc_auc))
    fp.close()

    #roc auc
    #https://stackoverflow.com/questions/43043271/roc-curve-for-binary-classification-in-python
    fpr, tpr, auc_plot = dict(), dict(), dict()
    for i in range(2):
        fpr[i], tpr[i], _ = roc_curve(test_set_labels, y_pred)
        auc_plot[i] = auc(fpr[i], tpr[i])
    plt.figure()
    plt.plot(fpr[1], tpr[1], color='darkorange', lw = 2, label='ROC curve (area = %0.2f)' % auc_plot[1])
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc = "lower right")
    plt.show()