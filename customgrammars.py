#### 2014/2015 - node replaced in nltk 3.0 with label()

import nltk, pickle
import re
import sys
import random, itertools
from nltk.corpus import brown

def a(input):
    x = input[random.randint(0,len(input) - 1)]
    return x

def storepickle(text,where):
    out = open(where, 'wb')
    pickle.dump(text, out)
    out.close()

def recallpickle(where):
    out = open(where, 'rb')
    text=pickle.load(out) 
    out.close()
    return text

ttt=recallpickle("/root/diana/chapters/3_glass-crash/pickle/customcrashsentenced.pickle")

grammar="""
IP: {<JJ|NN>?<INJ><MD|R.*|WDT||V.*|JJ.*|CC|P.*|TO|DT|IN|NN.*|INJ|COL|CHR>+} 
CP: {<JJ>?<CHR><DT|V.*|JJ.*|CC|POS|IN|NN.*|TO,>+} 
OP: {<JJ>?<COL><DT|V.*|JJ.*|CC|POS|IN|NN.*|,|.>+} 
"""

# NP: {<COL|INJ|CHR><DT|V.*|JJ.*|CC|POS|IN|NN.*|PRP.*|COL|TO|,>+}  =*****
# injuries caused by INJ VBN IN
#grammar = "IP: {<DT>?<JJ.*>?<N.*>+<IN>+<JJ.*|VB.*>+<N.*>?<CC>?<JJ.*|NN>?<IN>?<NNS>}"
#grammar = "NP: {<JJ.*>?<VBD|N.*>?<IN|VBD>?<NN>?<N.*>}" # dt jj nn = the adjective noun 

cp = nltk.RegexpParser(grammar)
result = [cp.parse(sent) for sent in ttt]

nounphrase=[]
np=""
npp=""
for sent in result:
    for subtree in sent.subtrees():
        np =""
        if subtree.label() == 'IP':
            x=' '.join(nltk.tag.untag(subtree))
            for i in x:
                np += i
            npp += np +" " 
            nounphrase.append(np)

nounphraseo=[]

np=""
for sent in result:
    for subtree in sent.subtrees():
        np =""
        if subtree.label() == 'OP':
            x=nltk.tag.untag(subtree)
            for i in x:
                np += i + " "
            nounphraseo.append(np[:-1])

nounphraseo = list(set(nounphraseo))

pastverb = []
nounphrasei=[]

for sent in result:
    for subtree in sent.subtrees():
        np =""
        if subtree.label() == 'IP':
            for i in subtree:
                if i[1] == "VBD":
                    pastverb.append(i[0])
            x=nltk.tag.untag(subtree)
            for i in x:
                np += i + " "
            nounphrasei.append(np[:-1])

nounphrasei = list(set(nounphrasei))
pastverb = list(set(pastverb))

pastverb = []
for sent in ttt:
    for i in sent:
        if i[1] == "VBD":
            pastverb.append(i[0])
pastverb = list(set(pastverb))

def diana():
    x="Diana "+a(pastverb)+" "+a(nounphrasei)+" "+ a(pastverb)+" "+a(nounphrase)+" "+ a(pastverb)+" "+a(nounphraseo)+"."
#    x="Diana "+ a(pastverb)+" "+a(nounphrasei)+" in a "+a(nounphraseo)+"."
    print x

for x in range(10):
    diana()

# print "injury:"
# print nounphrasei
# print "collision:"
# print nounphraseo
# print "crash:"
# print nounphrase
