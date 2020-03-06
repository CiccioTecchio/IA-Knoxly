import csv, os, sys, string

dest_f = open(str(sys.argv[1]), 'a')
limit = int(sys.argv[2])
w = csv.writer(dest_f, dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
#topic = { "elezioniAU.csv": 0, "electionUS.csv": 0, "medici.csv": 1, "amz_new.csv": 2, "aereo.csv": 3 }
topic = {"electionUS.csv": 0, "medici.csv": 1, "amz_new.csv": 2, "aereo.csv": 3, "movie_NOSENSE.csv":4 }
translator = str.maketrans('', '', string.punctuation)
#skip = int(sys.argv[3])
#i = 0

for src in os.listdir("."):#extract the file in this 
	if src == "aereo.csv" or src == "amz_new.csv" or src == "electionUS.csv" or src == "medici.csv" or src == "movie_NOSENSE.csv":
		source_f = open(src, 'r')
		print(src)
		r = csv.reader(source_f)

		for row in zip(r, range(limit)):# first limit tweet
		#for row in r:
			#if i < skip:
			#	next(r)
			#else:
			row = str(row[0]).translate(translator)
			w.writerow([row]+[topic[src]])
			#i+=1
		#i = 0
		source_f.close()
dest_f.close()