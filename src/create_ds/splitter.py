import sys, csv, fileop

#election_day ha 397628 righe +1 di intestazione

fp = open(str(sys.argv[1]), 'r')
r = csv.reader(fp)
i = 0
start = int(sys.argv[3])
end = start + 99408
while i < start:
	next(r)
	i+=1
fpW = open(str(sys.argv[2]), 'w')
w = csv.writer(fpW, dialect='excel', delimiter=' ', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
for row in r:
	if i <= end: 
		w.writerow([row[int(sys.argv[4])]])
		i+=1
	else: break
fpW.close()
fp.close()
