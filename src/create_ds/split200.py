import csv

r = csv.reader(open("ds200.csv", "r"))
next(r)

w_p = csv.writer(open("topic/politics200.csv", "w"), dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
w_p.writerow(["text","tipo","sensibile"])

w_h = csv.writer(open("topic/health200.csv", "w"), dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
w_h.writerow(["text","tipo","sensibile"])

w_j = csv.writer(open("topic/job200.csv","w"), dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
w_j.writerow(["text","tipo","sensibile"])

w_t = csv.writer(open("topic/travel200.csv","w"), dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
w_t.writerow(["text","tipo","sensibile"])

w_g = csv.writer(open("topic/general200.csv","w"), dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
w_g.writerow(["text","tipo","sensibile"])

for row in r:
	topic = int(row[1])
	to_cpy = [row[0], topic, int(row[2])]
	if topic == 0: w_p.writerow(to_cpy)
	elif topic == 1: w_h.writerow(to_cpy)
	elif topic == 2: w_j.writerow(to_cpy)
	elif topic == 3: w_t.writerow(to_cpy)
	elif topic == 4: w_g.writerow(to_cpy)

