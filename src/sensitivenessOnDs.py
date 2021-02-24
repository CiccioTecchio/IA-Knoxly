import sensitiveness, pickle

PATH_TOPIC = "src/topic_ds/multilang/"
title = ["politics", "health", "job", "travel", "general", "racism", "religion", "sexual_orientation"]
path = []
for i in title: path.append(PATH_TOPIC+i+"/")
for i in range(8):
    print(title[i])
    classificatore = sensitiveness.sensitiveness(path[i]+title[i]+"200.csv", 16, 'roc_auc', path[i]+"RF.txt", path[i]+"misure_testing.txt", path[i], title[i])
    pickle.dump(classificatore, open(path[i]+title[i]+".dump", "wb"))

#sensitiveness on DS

PATH = "src/sensitiveness_class/multilang/"
print("ds200")
classificatore = sensitiveness.sensitiveness('src/ds200.csv', 16, 'roc_auc', PATH+"RF.txt", PATH+"training/misure_testing.txt", PATH, "ds200")
pickle.dump(classificatore, open(PATH+"ds200.dump", "wb"))
