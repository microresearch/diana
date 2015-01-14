# generate  ngram text and then match new ballardian NPs

import random, pickle
import nltk

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

class Markov(object):
       
       def __init__(self, open_file):
               self.cache = {}
               self.open_file = open_file
               self.words = self.file_to_words()
               self.word_size = len(self.words)
               self.database()
               
       
       def file_to_words(self):
               self.open_file.seek(0)
               data = self.open_file.read()
               words = data.split()
               return words
               
       
       def triples(self):
               """ Generates triples from the given data string. So if our string were
                               "What a lovely day", we'd generate (What, a, lovely) and then
                               (a, lovely, day).
               """
               
               if len(self.words) < 3:
                       return
               
               for i in range(len(self.words) - 2):
                       yield (self.words[i], self.words[i+1], self.words[i+2])
                       
       def database(self):
               for w1, w2, w3 in self.triples():
                       key = (w1, w2)
                       if key in self.cache:
                               self.cache[key].append(w3)
                       else:
                               self.cache[key] = [w3]
                               
       def generate_markov_text(self, size=10000):
               seed = random.randint(0, self.word_size-3)
               seed_word, next_word = self.words[seed], self.words[seed+1]
               w1, w2 = seed_word, next_word
               gen_words = []
               for i in xrange(size):
                       gen_words.append(w1)
                       w1, w2 = w2, random.choice(self.cache[(w1, w2)])
               gen_words.append(w2)
               return ' '.join(gen_words)


random.seed()
#crash_raw = open("/root/diana/chapters/3_glass-crash/texts/crash.txt").read() 
#crash_raw = removeNonAscii(crash_raw)

#sens = nltk.sent_tokenize(crash_raw)
#crash = []
#for sen in sens:
#	crash += nltk.word_tokenize(sen)

#model = nltk.NgramModel(3, crash)
#ttt = model.generate(100000)
filee=open('/root/diana/chapters/3_glass-crash/texts/crash.txt')
markk = Markov(filee)
ttt=markk.generate_markov_text()
ttt = removeNonAscii(ttt)

#ttt is generated

#now match a POS template or Ballardian noun phrase

grammar="""
IP: {<JJ|NN>?<INJ><MD|R.*|WDT||V.*|JJ.*|CC|P.*|TO|DT|IN|NN.*|INJ|COL|CHR>+} 
CP: {<JJ>?<CHR><DT|V.*|JJ.*|CC|POS|IN|NN.*|TO,>+} 
OP: {<JJ>?<COL><DT|V.*|JJ.*|CC|POS|IN|NN.*|,|.>+} 
TP: {<NN>+} 
"""

patterns = [
    ('injur*|wound*', 'INJ'),
    ('crash*', 'CHR'),
    ('collision*', 'COL')
    ]

ttt=nltk.word_tokenize(ttt)

#print ttt

tag1= nltk.data.load(nltk.tag._POS_TAGGER)
regexp_tagger = nltk.RegexpTagger(patterns,backoff=tag1)
#ttt=[regexp_tagger.tag(sent) for sent in ttt]
ttt=regexp_tagger.tag(ttt)

cp = nltk.RegexpParser(grammar)
#result = [cp.parse(sent) for sent in ttt]
result = cp.parse(ttt)
#print result
nounphrase=[]
npp=""
#for sent in result:
for subtree in result.subtrees():
#    if len(subtree) == 5:
    np=""
#    print subtree
    if subtree.label() == 'IP':
        x=' '.join(nltk.tag.untag(subtree))
        for i in x:
            np += i
        npp += np +" " 
        nounphrase.append(np)
print nounphrase



