import sensitiveness

#sensitiveness on DS
PATH = "src/sensitiveness_class/"
sensitiveness.sensitiveness('src/ds200.csv', 10, 'roc_auc', PATH+"RF.txt", PATH+"training/misure_testing.txt")

# politics
#PATH_TOPIC = "src/topic_ds/"
#sensitiveness.sensitiveness(PATH_TOPIC+"politics200.csv", 10, 'roc_auc', PATH_TOPIC+"politics/RF.txt", PATH_TOPIC+"politics/misure_testing.txt")

# health
#sensitiveness.sensitiveness(PATH_TOPIC+"health200.csv", 10, 'roc_auc', PATH_TOPIC+"health/RF.txt", PATH_TOPIC+"health/misure_testing.txt")

# jobs
#sensitiveness.sensitiveness(PATH_TOPIC+"job200.csv", 10, 'roc_auc', PATH_TOPIC+"job/RF.txt", PATH_TOPIC+"job/misure_testing.txt")

# travel
#sensitiveness.sensitiveness(PATH_TOPIC+"travel200.csv", 10, 'roc_auc', PATH_TOPIC+"travel/RF.txt", PATH_TOPIC+"travel/misure_testing.txt")

# general
#sensitiveness.sensitiveness(PATH_TOPIC+"general200.csv", 10, 'roc_auc', PATH_TOPIC+"general/RF.txt", PATH_TOPIC+"general/misure_testing.txt")


#Plot roc_auc

#Print matrici di confusione

