import nltk, pickle
import re
import sys
import random, itertools
from string import join

def recallpickle(doc,name):
    name=name+".pickle"
    out = open(name, 'rb')
    doc.text=pickle.load(out) 
    out.close()

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

def storeandtok(doc,name):
    doc.text = tokenize_text_and_tag_named_entities(text)
    name=name+".pickle"
    out = open(name, 'wb')
    pickle.dump(doc.text, out)
    out.close()

class doc():
  pass
doc.headline = ['this is expected by nltk.sem.extract_rels but not used in this script']

# ttt = open('/root/diana/chapters/3_glass-crash/texts/crash.txt','r')
# text=ttt.read()
# text=removeNonAscii(text)
# doc.text= tokenize_text_and_tag_named_entities(text)
# storeandtok(doc,"/root/diana/chapters/3_glass-crash/pickle/crash_tagged2")

recallpickle(doc,"/root/diana/chapters/3_glass-crash/pickle/crash_tagged2")

#pairs = nltk.sem.relextract.mk_pairs(doc.text)
pairs = nltk.sem.relextract.tree2semi_rel(doc.text)

diana= ['Diana','Dodi','Queen', 'King','Prince','Princess', 'Goddess', 'Victim', 'Huntress', 'Star','Mary', 'Trinity','Double', 'Bitch', 'Vaughan','Ballard','Catherine','Dr Remington','Henri Paul']

for x in range(100):
    reldicts = nltk.sem.relextract.semi_rel2reldict(pairs, window=(x+1)) #window as key
    for r in reldicts:
        sentence =random.choice(diana)+" "
        xxx=r['rcon']
        sentence=sentence+xxx
        xxx=r['lcon']
        sentence=sentence+" "+xxx+" "+random.choice(diana)+"."
        sentence=sentence.replace(' ,', ',').replace(" .", '.').replace(" 's", "'s")
        print sentence    

# reldicts = nltk.sem.relextract.mk_reldicts(pairs, window=5) #window as key was 5
# for r in reldicts:
#     sentence =random.choice(diana)+" "
#     xxx=r['rcon']
#     sentence=sentence+xxx
#     xxx=r['lcon']
#     sentence=sentence+" "+xxx+" "+random.choice(diana)+"."
#     sentence=sentence.replace(' ,', ',').replace(" .", '.').replace(" 's", "'s")
#     print sentence    

