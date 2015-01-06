# named entities and early permutations- print relations

import nltk, pickle
import re
import sys
import random, itertools
from string import join

def reader():
    text = ''
    for line in sys.stdin:
        text += line
    return text

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

class doc():
  pass
doc.headline = ['this is expected by nltk.sem.extract_rels but not used in this script']


# compile expressions to use to identify relations between named entities
IN = re.compile (r'.*\bin\b')
TO = re.compile (r'.*\bto\b')
OF = re.compile (r'.*\bof\b')
BY = re.compile (r'.*\bby\b')

# a list of verb tags for reference
verbs = ['VB',  'VBG',  'VBD', 'VBN',  'VBP',  'VBZ']

# annotate the source text and store it in doc

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

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

#text=reader()
#print doc.text

ttt = open('/root/diana/chapters/3_glass-crash/texts/crash.txt','r')
text=ttt.read()
text=removeNonAscii(text)
doc.text= tokenize_text_and_tag_named_entities(text)
storeandtok(doc,"/root/diana/chapters/3_glass-crash/pickle/crash_tagged2")

recallpickle(doc,"/root/diana/chapters/3_glass-crash/pickle/crash_tagged2")

def pwalk(chunked):
    listie=[]
    for n in chunked:
        if isinstance(n, nltk.tree.Tree):               
            if n.node == 'PERSON':
                if (''.join(n.leaves())) not in listie:
                    listie.append(''.join(n.leaves()))
                #print ''.join(n.leaves())
    return listie

def lwalk(chunked):
    listie=[]
    for n in chunked:
        if isinstance(n, nltk.tree.Tree):               
#            if n.node == 'LOCATION' or n.node == 'ORGANIZATION':
            if n.node == 'LOCATION':
                if (''.join(n.leaves())) not in listie:
                    listie.append(''.join(n.leaves()))
                #print ''.join(n.leaves())
    return listie

INJ = re.compile (r'.*\bin\b')

for rel in nltk.sem.extract_rels('PERSON','PERSON',doc,corpus='ieer', pattern=INJ):
# doesnt work with CONLL2002
    print nltk.sem.relextract.show_raw_rtuple(rel) 



#locations=lwalk(doc.text)
#people=pwalk(doc.text)

# for person in people:
#     if person in locations:
# #       print "removing", person 
#        locations.remove(person)



# print "Locations",
# print locations
# print "People",
# print people

#extract_people_in_locations()

#pairs = nltk.sem.relextract.mk_pairs(doc.text)
#reldicts = nltk.sem.relextract.mk_reldicts(pairs, window=5) #window as key

# for r in reldicts:
# #    print
# #    print r['subjtext'],
#     print "Diana",
# #    print r['filler'],
#     print r['rcon'],
#     print r['lcon']
# #format for, and '???
# #    print r['objtext'],
# #    print "Dodi."

#for s, tree in pairs:
#    print '("%s", %s)' % (join(s),tree)

# permute as [Diana was], [killed by], [general accident], [with wounds to], [body parts], [in/at], [location]

# TODO: extract locations from crash and paget...
# gen accident/wounds

def permute(inputlist):
    x= [' '.join(s) for s in itertools.product(*inputlist)]
    for sent in x:
#        print sent[:-1]+"."
        print sent+"."

accidentlist=["a deformation of the passenger compartment in a head-on collision", "a deformation of passenger compartment in a read-end collision", "an accident", "a windscreen ejection", "a mechanism of passenger ejection","the telescoping mechanism of the car-body in a front-end collision", "abrasive injuries formed in a roll-over","the amputation of limbs by roof assemblies and door sills during roll-over","injuries sustained in an accident", "facial injuries caused by dashboard and window trim", "scalp and cranial injuries caused by the rear-view mirror and sun-visor", "whiplash injuries in a rear-end collision", "first and second-degree burns in an accident involving the rupture and detonation of fuel tanks", "chest injuries caused by steering column impalements", "abdominal injuries caused by a faulty seat-belt adjustment", "a second-order collision between front-seat and rear-seat passengers", "cranial and spinal injuries caused by ejection through windshields", "graded injuries to the skull caused by variable windshield glasses", "injuries caused by prosthetic limbs", "injuries caused within a car fitted with invalid controls", "the complex self-amplifying injuries of single and double amputees", "injuries caused by specialist automobile accessories such as record players, cocktail cabinets and radiotelephones", "the injuries caused by manufacturers' medallions"]

partslist=["kneecap", "hip-joint", "limbs", "face", "vulva", "breast", "nipples", "genitals", "scalp", "cranium", "chest", "spine", "abdomen"]

#list=["Diana was killed by"], accidentlist, ["sustaining wounds to the"], partslist, ["in"], locations

#list=["Diana was in"], locations

# Diana sustained

# chest injuries caused by steering column impalements 
# [partslist] injuries caused by [NN NN NNS] /or/ [JJ NNS]

# whiplash injuries in rear-end collisions
# [type] injuries in [JJ NNS]

# diana was killed by INJ in COLLISION in CRASH

#permute(list)
