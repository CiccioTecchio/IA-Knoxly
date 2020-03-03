import re
import sys
import time
from textblob import TextBlob

def addLines(r, w):
    regex = '^RT @.*'
    add_cont = 0
    for row in r:
        twt = [row[int(sys.argv[3])]]  # int is col to append
        print(twt[0])
        if len(twt[0]) > 3 and not re.match(regex, twt[0]) and TextBlob(twt[0]).detect_language() == 'en':  # skip retweet
            print("ACCETTATO")
            w.writerow(twt)
            add_cont += 1
            time.sleep(0.5)
        else:
            print("RIFIUTATO")
    return add_cont


def contLines(r):
    tot_line = -1
    for row in r:
        tot_line += 1
    return tot_line
