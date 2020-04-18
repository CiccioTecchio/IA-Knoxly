import pickle
import tensorflow_hub as hub

def dividi(totList, start, n):
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    tr = []
    i = 0
    while i<n: 
        tr.extend(embed([totList[start]]))
        i+=1
        start+=1
    return tr

def concat_Embed(totList, part):
    tr = []
    i, start = 0,0
    size = len(totList)
    n_part = size//part
    reminder = size%part
    while i < n_part:
        tr.extend(dividi(totList,start,part))
        i+=1
        start+=part
        print(str(i)+", "+str(len(tr)))
    if reminder != 0:
        tr.extend(dividi(totList,start,reminder))
        i+=1
        print(str(i)+", "+str(len(tr)))
    return tr