import sensitiveness, pickle

PATH_TOPIC = "src/topic_ds/"
title = ["politics", "health", "job", "travel", "general"]
path = []
for i in title: path.append(PATH_TOPIC+i+"/")
for i in range(5):
    print(title[i])
    classificatore = sensitiveness.sensitiveness(path[i]+title[i]+"200.csv", 10, 'roc_auc', path[i]+"RF.txt", path[i]+"misure_testing.txt", path[i], title[i])
    pickle.dump(classificatore, open(path[i]+title[i]+".dump", "wb"))

#sensitiveness on DS
PATH = "src/sensitiveness_class/"
print("ds200")
classificatore = sensitiveness.sensitiveness('src/ds200.csv', 10, 'roc_auc', PATH+"RF.txt", PATH+"training/misure_testing.txt", PATH, "ds200")
pickle.dump(classificatore, open(PATH+"ds200.dump", "wb"))