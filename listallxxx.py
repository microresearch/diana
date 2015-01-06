import nltk, pickle
import re
import sys
import random, itertools
from nltk.corpus import brown

def recallpickle(where):
    out = open(where, 'rb')
    text=pickle.load(out) 
    out.close()
    return text

ttt=recallpickle("pickle/customcrashsentenced.pickle")

listof=[]

lastnoun=" "
lastlastnoun=" "
nounlist = []
for sent in ttt:
    sentence=""
    for i in sent:
        if "VBD" in i[1] or "VBN" in i[1]:        
            if i[0] not in listof:
                listof.append(i[0])
print " ".join(listof)
