# for NLTK 3.0

import nltk, pickle
import re
import sys
import random, itertools
from string import join
from textclean.textclean import textclean

def tokenize_text_and_tag_named_entities(text):
    tokens = []
    # split the source string into a list of sentences
    # for each sentence, split it into words and tag the word with its PoS
    # send the words to the named entity chunker
    # for each chunk containing a Named Entity, build an nltk Tree consisting of the word and its Named Entity tag
    # and append it to the list of tokens for the sentence
    # for each chunk that does not contain a NE, add the word to the list of tokens for the sentence
    for sentence in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
            try:
                chunk.label()
            except AttributeError:
                tokens.append(chunk[0])
            else:
                if chunk.label() != 'GPE':
                    tmp_tree = nltk.Tree(chunk.label(),  [(' '.join(c[0] for c in chunk.leaves()))])
                else:
                    tmp_tree = nltk.Tree('LOCATION',  [(' '.join(c[0] for c in chunk.leaves()))])
                    tokens.append(tmp_tree)
    return tokens

def storepickle(text,where):
    out = open(where, 'wb')
    pickle.dump(text, out)
    out.close()

def storeandtok(doc,name):
    doc.text = tokenize_text_and_tag_named_entities(text)
    name=name+".pickle"
    out = open(name, 'wb')
    pickle.dump(doc.text, out)
    out.close()

def recallpickle(doc,name):
    name=name+".pickle"
    out = open(name, 'rb')
    doc.text=pickle.load(out) 
    out.close()

class doc():
  pass
doc.headline = ['this is expected by nltk.sem.extract_rels but not used in this script']

# redo pickle

# ttt = open('texts/crashchap1','r')
# text=ttt.read()
# text = textclean.clean(text)
# doc.text= tokenize_text_and_tag_named_entities(text)
# storeandtok(doc,"test")

recallpickle(doc,"test")

#print(doc.text)

#pairs = nltk.sem.relextract.mk_pairs(doc.text)
#reldicts = nltk.sem.relextract.mk_reldicts(pairs, window=5) #window as key

pairs = nltk.sem.relextract.tree2semi_rel(doc.text)
#print pairs
reldicts = nltk.sem.relextract.semi_rel2reldict(pairs, window=5) #window as key


for r in reldicts:
    sentence ="Diana "
    xxx=r['rcon']
    sentence=sentence+xxx
    xxx=r['lcon']
    sentence=sentence+" "+xxx+" Dodi."
    sentence=sentence.replace(' ,', ',').replace(" .", '.').replace(" 's", "'s")
    print sentence
