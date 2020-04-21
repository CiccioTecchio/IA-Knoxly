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
from sklearn.metrics import confusion_matrix, auc, accuracy_score, roc_auc_score, roc_curve
from matplotlib import cm
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def sensitiveness(ds, n_folds, scoring, path_RF, path_training, path_fig, title):
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
    
    plot_confusion_matrix(test_set_labels, y_pred, title=title, path_matr = path_fig+"mtr_"+title+".png")
    return classificatore

def plot_confusion_matrix(y_true, y_pred, classes=[0, 1],
                          normalize=True,
                          title = None,
                          cmap=cm.Blues,
                          path_matr= None):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    print('conf matrix: {}'.format(cm))
    # Only use the labels that appear in the data
    # classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    fig.savefig(path_matr)
    return ax

    
#https://stackoverflow.com/questions/43043271/roc-curve-for-binary-classification-in-python
def plot_roc_auc(y_true, y_pred,path_fig):
    fpr, tpr, auc_plot = dict(), dict(), dict()
    for i in range(2):
        fpr[i], tpr[i], _ = roc_curve(y_true, y_pred)
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
    plt.savefig(path_fig+"roc_auc.png")
    #plt.show()
    plt.close()