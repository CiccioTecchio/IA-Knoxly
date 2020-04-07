import os, csv, regex
from sentence_splitter import SentenceSplitter, split_text_into_sentences

fp = open("amz_new.csv", "r")
splitter = SentenceSplitter(language='it')
r = csv.reader(fp)
fw = open("amz_split.csv", "w")
w = csv.writer(fw,dialect='excel', delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
for row in r:
	txtsplit = splitter.split(text=row[0])
	for i in txtsplit:
		w.writerow([i])
fp.close()
fw.close()

	
