import csv

fp_r = open('ds200Test.csv','r')
r = csv.reader(fp_r)
next(r)# skip headerline
fp_w = open('ds200Quote.csv','w')
w = csv.writer(fp_w, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
w.writerow(["text","tipo","sensibile"])
i = 0
for row in r:
	to_cpy = [row[0], int(row[1]), int(row[2])]
	w.writerow(to_cpy)
