#THIS IS noun delay

import nltk, pickle
import re
import sys
import random, itertools
from nltk.corpus import brown
from textclean.textclean import textclean

def reader():
#    ttt = open('/root/collect2012-3/diana/documents/paget2.txt','r')
#    ttt = open('shortpaget','r')
#    ttt = open('crash.txt','r')
    ttt = open('/root/diana/chapters/3_glass-crash/texts/crashchap1','r')
#    ttt = open('wounds/crashwounds','r')
#    uuu=rrr.read()+ttt.read()
    return textclean.clean(ttt.read())

def plaintaggedtree(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
#    sentences = [nltk.pos_tag(sent) for sent in sentences] 
#    sentences = [nltk.ne_chunk(sent) for sent in sentences]
    return sentences

class doc():
  pass
doc.headline = ['this is expected by nltk.sem.extract_rels but not used in this script']

def storepickle(text,where):
    out = open(where, 'wb')
    pickle.dump(text, out)
    out.close()

def recallpickle(where):
    out = open(where, 'rb')
    text=pickle.load(out) 
    out.close()
    return text

patterns = [
    ('injur*|wound*', 'INJ'),
    ('crash*', 'CHR'),
    ('collision*', 'COL')
    ]


text=reader()
# ttt=nltk.word_tokenize(text)
ttt=plaintaggedtree(text)

tag1= nltk.data.load(nltk.tag._POS_TAGGER)
regexp_tagger = nltk.RegexpTagger(patterns,backoff=tag1)
ttt=[regexp_tagger.tag(sent) for sent in ttt]
# #print ttt

# storepickle(ttt,"pagetsentenced.pickle") 
#ttt=recallpickle("pagetsentenced.pickle")+recallpickle("customcrashsentenced.pickle")
#ttt=recallpickle("customcrashsentenced.pickle")

lastnoun=" "
lastlastnoun=" "
nounlist = []
for sent in ttt:
    sentence=""
    for i in sent:
#        print i
        if "NN" in i[1]:        
            lastnoun=i[0]
            sentence+=lastlastnoun+" "
        else:
            if i[0]=="," or i[0]==".":
                sentence= sentence[:-1] + i[0]+" "
            else:
                sentence+=i[0]+" "
        lastlastnoun=lastnoun
    print sentence[:-1],
    
