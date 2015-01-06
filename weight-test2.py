import nltk,random
import math

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

train_txt = open("/root/diana/chapters/3_glass-crash/texts/chap14").read()
train_txt = removeNonAscii(train_txt)

train_sens = nltk.sent_tokenize(train_txt)
train_txt = []
for sen in train_sens:
    train_txt += nltk.pos_tag(nltk.word_tokenize(sen))

fdist1 = nltk.FreqDist(train_txt) 
vocab = fdist1.keys()

def choose_weighted(wlist):
     if isinstance(wlist, list):
         wlist.sort(key=lambda x: x[1])
         choice = random.random() * sum(j for i, j in wlist)
         for i, w in wlist:
             choice -= w
             if choice < 0:
                 return i
     else:
         return wlist[0]

mm = {}

def insertTuple(d, k, tup):
    if k not in d:
        d[k] = tup
    elif type(d[k]) == tuple:
        d[k] = [ d[k], tup ]
    elif not(tup in d[k]):
        d[k].append(tup)

#print fdist1[vocab[0]]

# don't need division?

for tword in train_txt:
    insertTuple(mm, tword[1], ([tword[0]],fdist1[tword]))

for x in range(1):
    print choose_weighted(mm["VBN"]),

#print mm
