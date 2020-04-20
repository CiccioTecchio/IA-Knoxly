from sklearn.model_selection import GridSearchCV
#topic_class = 'f1_weighted'
def grid(cl,classifier,param_grid,n_folds,t_s_D,tLab_downsampled, score):
    with open(cl,"w") as f:
        estimator = GridSearchCV(classifier, cv=n_folds, param_grid=param_grid, n_jobs=-1, verbose=1,scoring=score)#scoring='accuracy')
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

def printMisure(filename, precision, recall, fscore, accuracy):
    dato = "dataset usato "+filename+":\n"
    prec = 'precision: {}\n'.format(precision)
    rec = 'recall: {}\n'.format(recall)
    fsc = 'fscore: {}\n'.format(fscore)
    acc = 'accuracy: {}\n'.format(accuracy)
    return dato+acc+prec+rec+fsc