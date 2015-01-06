# see also common_contexts

import nltk, random
from textclean.textclean import textclean

def a(input):
    x = input[random.randint(0,len(input) - 1)]
    return x

def plaintaggedtree(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences] 
    return sentences

#f = open("/root/collect2012-3/diana/documents/paget2.txt")
f = open("/root/diana/chapters/3_glass-crash/texts/crash.txt")
#f = open("crashchap1")
crash=f.read()#+ff.read()
crash = textclean.clean(crash)
tokens = nltk.word_tokenize(crash)
text1 = nltk.Text(tokens)

idx = nltk.text.ContextIndex(tokens)

#text1.similar('crash')

save = [ ]
for word in nltk.word_tokenize("sex"):
    save.append(idx.similar_words(word))
#word=("crash","sex")
#print idx.common_contexts(word)

#text1.common_contexts(["crash","car"])

print save

#[penis]car fingers hands mind chest face mouth wife body hand legs own
#shoulder accident arm arms death eyes head headlamps

#[crash]car accident motorway drive it passengers seat see vaughan window
#woman air airport belt blood body cars chest control door

# how this can be used to generate text

#- run through and replace with similar...
#- 


