import csv
import fileop
import sys

source_f = open(str(sys.argv[1]), 'r')
r = csv.reader(source_f)
next(r)  # skip CSV headerline
dest_f = open(str(sys.argv[2]), 'a')
w = csv.writer(dest_f, dialect='excel', delimiter=' ', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
add_cont = fileop.addLines(r, w)
dest_f.close()
source_f.close()
dest_f = open(str(sys.argv[2]), 'r')
r = csv.reader(dest_f)
tot_line = fileop.contLines(r)
print(str(sys.argv[1]) + ': ' + str(add_cont) + ' lines added ' + str(tot_line) + ' total lines')
